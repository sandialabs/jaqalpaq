# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
import numpy

from jaqalpaq.error import JaqalError
from jaqalpaq.core.algorithm.walkers import TraceSerializer, Trace
from jaqalpaq.run.cursor import SubcircuitCursor, State
from jaqalpaq.core.result import Subcircuit, ReadoutTreeNode, validate_probabilities
from jaqalpaq.emulator.backend import EmulatedIndependentSubcircuitsBackend
from ._import import get_ideal_action


class UnitarySerializedEmulator(EmulatedIndependentSubcircuitsBackend):
    """Serialized emulator using unitary matrices

    This object should be treated as an opaque symbol to be passed to run_jaqal_circuit.
    """

    def _make_subcircuit(self, job, index, start, end):
        """Generate the ProbabilisticSubcircuit associated with the trace of circuit
            being process in job.

        :param job: the job object controlling the emulation
        :param int index: the index of the trace in the circuit
        :param Trace trace: the trace of the subcircuit
        :return: A ProbabilisticSubcircuit.
        """

        circ = job.expanded_circuit

        cursor = SubcircuitCursor.terminal_cursor(end)
        trace = Trace(list(start.address), list(end.address))

        n_qubits = self.get_n_qubits(circ)

        hilb_dim = 2**n_qubits
        gatedefs = circ.native_gates

        # vec = U * inp
        # We don't need to initialize inp yet
        inp = numpy.empty(hilb_dim, dtype=complex)
        vec = numpy.zeros(hilb_dim, dtype=complex)
        vec[0] = 1

        # We serialize the subcircuit, obtaining a list of gates.
        # The plan is to apply the associated unitary to vec for each gate.
        s = TraceSerializer(trace)

        first = True
        must_be_last = False

        for gate in s.visit(circ):
            if must_be_last:
                raise JaqalError("Invalid gate in subcircuit")

            # This captures the classical arguments to the gate
            argv = []
            # This capture the quantum arguments to the gate --- the qubit index
            qind = []
            gatedef = gatedefs[gate.name]

            try:
                ideal_unitary = get_ideal_action(gatedef)
            except KeyError:
                if first:
                    first = False
                    continue
                must_be_last = True
                # maybe add other checks?
                continue
            first = False

            if ideal_unitary is None:
                # This includes things like idle gates
                continue

            for param, val in zip(gatedef.parameters, gate.parameters.values()):
                if param.classical:
                    argv.append(val)
                else:
                    qind.append(val.alias_index)

            # This is the dense submatrix
            dsub = ideal_unitary(*argv)

            # now we need to sparse-multiply:
            # vec = U * imp
            # But! U isn't just dsub

            # The current state-vector becomes the input to the matrix multiplication
            inp, vec = vec, inp
            # (Notice that this initializes inp, from above)
            vec[:] = 0

            # For every column in the output matrix, we need to compute the sum
            # over the nonzero rows of U.

            # However, this corresponds to a sum only over rows of dsub, with
            # a particular mapping between the rows and columns.
            for i in range(hilb_dim):
                # Because we are only dealing with qubits, the binary representation
                # of the row is precisely the standard basis label corresponding to that
                # row.

                # We need to re-map the qubits that are being acted on by dsub to
                # the *column* of dsub.  Additionally, the qubits that are not being
                # acted on by dsub are unaffected, and therefore are the same in both
                # the input and output.

                # mask is precisely these bystander qubits --- the affected qubits are
                # set to zero, and shuffled into another variable, dsub_row
                mask = i

                # We initialize dsub_row to zero, and then build it up via bit-twiddling
                dsub_row = 0

                # Which bit (stored as a bitmask) is up to be changed?
                dsub_bit = 1
                for i_k in qind:
                    # We iterate over all the qubits acted on by dsub

                    # Is this specific qubit high (for this row)?
                    n_high = mask & (1 << i_k)

                    # If it is high, lower it in the mask
                    # (notice this is equivalent to subtraction)
                    mask ^= n_high

                    # If it is high, raise it in the row to be passed to dsub
                    # (notice this is equivalent to addition)
                    if n_high:
                        dsub_row |= dsub_bit

                    # Advance the bit mask by one
                    dsub_bit <<= 1

                # We now have the row in dsub that corresponds to the row in U

                # Next, we need to iterate over the column of U, and simultaneously the
                # column of inp --- this mapping is the same as the above, backwards.
                for dsub_col in range(dsub.shape[0]):
                    j = mask
                    dsub_bit = 1
                    for j_k in qind:
                        if dsub_col & dsub_bit:
                            j |= 1 << j_k
                        dsub_bit <<= 1

                    # Suitably armed with the associated row and column, we
                    # do the standard matrix accumulation sum step.

                    vec[i] += inp[j] * dsub[dsub_row, dsub_col]

        probs = numpy.abs(vec) ** 2

        p = validate_probabilities(probs)

        tree = ReadoutTreeNode(cursor)
        tree.simulated_statevector = vec

        for k, v in enumerate(p):
            nxt_cursor = cursor.copy()
            nxt_cursor.next_measure()
            node = tree.subsequent[k] = ReadoutTreeNode(nxt_cursor)
            node.simulated_probability = v

        ret = Subcircuit(index, start, end, tree=tree)

        return ret
