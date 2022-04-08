# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
import abc

from numpy.random import choice

from jaqalpaq.core.locus import Locus
from jaqalpaq.core.block import BlockStatement
from jaqalpaq.core.result import ExecutionResult, Readout
from jaqalpaq.core.result import ProbabilisticSubcircuit
from jaqalpaq.core.algorithm.walkers import walk_circuit

from jaqalpaq.run.backend import IndependentSubcircuitsBackend, AbstractBackend


class ExtensibleBackend(AbstractBackend):
    """Abstract mixin providing an interface for extending a backend.

    Every gate to be emulated should have a corresponding gate_{name} and
      gateduration_{name} method defined.
    """

    def __init__(self, n_qubits, stretched_gates=None, **kwargs):
        """(abstract) Perform part of the construction of a noisy model.

        :param n_qubits: The number of qubits to simulate
        :param stretched_gates: (default False)  Add stretched gates to the model:
          - If None, do not modify the gates.
          - If 'add', add gates with '_stretched' appended that take an extra parameter,
            a stretch factor.
          - Otherwise, stretched_gates must be the numerical stretch factor that is
            applied to all gates (no extra stretched gates are added
        """
        self.n_qubits = n_qubits
        self.stretched_gates = stretched_gates
        model, durations = self.build_model()
        super().__init__(model=model, gate_durations=durations, **kwargs)

    def get_n_qubits(self, circ):
        """Returns the number of qubits the backend will be simulating.

        :param circ: The circuit object being emulated/simulated.
        """
        circuit_qubits = super().get_n_qubits(circ)
        if circuit_qubits > self.n_qubits:
            raise ValueError(f"{self} emulates fewer qubits than {circ} uses")
        return self.n_qubits

    def set_defaults(self, kwargs, **defaults):
        """Set parameters from a list of defaults and function kwargs.

        For every value passed as a keyword argument (into **defaults), set it in the
          object's namespace.  Values in kwargs overrided the default.  Values used from
          kwargs are removed from kwargs.

        :param kwargs: a dictionary of your function's keyword arguments, mutated to
          only contain unused values.
        """
        for k, v in defaults.items():
            setattr(self, k, kwargs.pop(k, v))

    @staticmethod
    def _curry(params, *ops):
        """Helper function to make defining related gates easier.
        Curry every function in ops, using the signature description in params.  For
          every non-None entry of params, pass that value to the function.

        :param params: List of parameters to pass to each op in ops, with None allowing
          passthrough of values in the new function
        :param ops: List of functions to curry
        :return List[functions]: A list of curried functions
        """

        def _inner(op):
            def newop(self, *args, **kwargs):
                args = iter(args)
                argv = [next(args) if param is None else param for param in params]
                argv.extend(args)
                return op(self, *argv, **kwargs)

            return newop

        newops = []
        for op in ops:
            newops.append(_inner(op))

        return newops

    def collect_gate_models(self):
        """Return a dictionary of tuples of gate models and gate durations.

        This combs through the class's definition for all parameters named gate_*, and
          adds a corresponding entry in the returned dictionary, keyed by the associated
          gate name, of the gate model (i.e., the noisy process model) and the duration
          that the gate operates.
        : return dict: A dictionary of the models of the gates
        """
        gate_models = {}

        for gate_name in type(self).__dict__:
            if not gate_name.startswith("gate_"):
                continue

            name = gate_name[5:]
            gate_models[name] = (
                getattr(self, gate_name),
                getattr(self, f"gateduration_{name}"),
            )

        return gate_models


class EmulatedIndependentSubcircuitsBackend(IndependentSubcircuitsBackend):
    """Abstract emulator backend for subcircuits that are independent"""

    @abc.abstractmethod
    def _make_subcircuit(job, index, trace, circ):
        """(internal) Produce a subcircuit given a trace"""

    def _make_readout(self, subcircuit, qubits, readout_index, results):
        nxt = choice(2**qubits, p=subcircuit.probability_by_int)
        mr = Readout(nxt, readout_index)
        subcircuit.accept_readout(mr)
        results.append(mr)

    def _execute_job(self, job):
        """(internal) Execute the job on the backend"""
        subcircs = [
            self._make_subcircuit(job, *tr, job.expanded_circuit)
            for tr in enumerate(job.traces)
        ]
        results = []
        qubits = self.get_n_qubits(job.circuit)

        for readout_index, index in enumerate(
            walk_circuit(job.expanded_circuit, [t.start for t in job.traces])
        ):
            # The subcircuit directive is not handled separately from the block
            # that it contains, so we handle it manually here.
            start = Locus.from_address(
                job.expanded_circuit, job.traces[index].start
            ).object
            if isinstance(start, BlockStatement):
                assert start.subcircuit
                iterations = start.iterations
            else:
                iterations = 1
            for _ in range(iterations):
                self._make_readout(subcircs[index], qubits, readout_index, results)

        return ExecutionResult(subcircs, results)
