from qscout.core.circuit import ScheduledCircuit
from qscout import QSCOUTError
from cirq import XXPowGate, XPowGate, YPowGate, ZPowGate, PhasedXPowGate
import numpy as np

CIRQ_NAMES = {
	XXPowGate: (lambda g: ('MS', 0, g.exponent * np.pi / 2)),
	XPowGate: (lambda g: ('R', 0, g.exponent * np.pi)),
	YPowGate: (lambda g: ('R', np.pi/2, g.exponent * np.pi)),
	ZPowGate: (lambda g: ('Rz', g.exponent * np.pi)),
	PhasedXPowGate: (lambda g: ('R', g.phase_exponent * np.pi, g.exponent * np.pi))
}

def qscout_circuit_from_cirq_circuit(ccirc):
	"""Converts a Cirq Circuit to a Jaqal-PUP :class:`ScheduledCircuit`.

	:param cirq.Circuit ccirc: The Circuit to convert.
	:returns qscout.core.ScheduledCircuit: The same quantum circuit, converted to Jaqal-PUP.
	:raises QSCOUTError: if the input contains any instructions other than cirq.XXPowGate, cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate, or cirq.PhasedXPowGate.
	"""
	qcirc = ScheduledCircuit(True)
	try:
		n = 1 + max([qb.x for qb in ccirc.all_qubits()])
		line = True
	except:
		cqubits = ccirc.all_qubits()
		n = len(cqubits)
		qubitmap = {cqubits[i]: i for i in range(n)}
		line = False
	allqubits = qcirc.reg('allqubits', n)
	qcirc.gate('prepare_all')
	for moment in ccirc:
		for op in moment:
			if op.gate:
				if type(op.gate) in CIRQ_NAMES:
					if line:
						qcirc.gate(*CIRQ_NAMES[type(op.gate)](op.gate), *[allqubits[qb.x] for qb in op.qubits])
					else:
						qcirc.gate(*CIRQ_NAMES[type(op.gate)](op.gate), *[allqubits[qubitmap[qb]] for qb in op.qubits])
				else:
					raise QSCOUTError("Convert circuit to ion gates before compiling.")
			else:
				raise QSCOUTError("Cannot compile operation %s." % op) # TODO: Support non-gate instructions.
	qcirc.gate('measure_all')
	return qcirc
