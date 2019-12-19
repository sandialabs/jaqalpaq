from qscout.core import ScheduledCircuit
# from qscoutlib import MSGate, QasmGate, IonUnroller
from qiskit.converters import dag_to_circuit
from qscout import QSCOUTError
#from sympy.core.evalf import N

QISKIT_NAMES = {'i': 'I', 'r': 'R', 'sx': 'Sx', 'sy': 'Sy', 'x': 'Px', 'y': 'Py', 'rz': 'Rz'}

def qscout_circuit_from_dag_circuit(dag):
	return qscout_circuit_from_qiskit_circuit(dag_to_circuit(dag))

def qscout_circuit_from_qiskit_circuit(circuit):
	n = sum([qreg.size for qreg in circuit.qregs])
	qsc = ScheduledCircuit(True) # TODO: Allow user to supply a different native gateset.
	baseregister = qsc.reg('baseregister', n)
	offset = 0
	for qreg in circuit.qregs:
		qsc.map(qreg.name, qreg.size, baseregister, slice(offset, offset + qreg.size))
		offset += qreg.size
	qsc.gate('prepare_all')
	# We're going to divide the circuit up into blocks. Each block will contain every gate
	# between one barrier statement and the next. If the circuit is output with no further
	# processing, then the gates in each block will be run in sequence. However, if the
	# circuit is passed to the scheduler, it'll try to parallelize as many of the gates
	# within each block as possible, while keeping the blocks themselves sequential.
	block = qsc.block(parallel = None)
	for instr in circuit.data:
		if instr[0].name == 'measure': # TODO: Support intermediate measure_all/prepare_all pairs.
			pass # Ignore whatever measurements the qiskit circuit object tells us to make, because we'll just measure every qubit at the end of the circuit.
		elif instr[0].name == 'reset':
			raise QSCOUTError("Physical hardware does not currently support resetting ions!")
		elif instr[0].name == 'barrier':
			block = qsc.block(parallel = None) # Use barriers to inform the scheduler, as explained above.
		elif instr[0].name == 'snapshot':
			raise QSCOUTError("Physical hardware does not support snapshot instructions.")
		elif instr[0].name in QISKIT_NAMES:
			target = instr[1][0]
			if target.register.name in qsc.registers:
				block.append(qsc.build_gate(QISKIT_NAMES[instr[0].name], qsc.registers[target.register.name][target.index], *[float(param) for param in instr[0].params]))
			else:
				raise QSCOUTError("Gate register %s invalid!" % target.register.name)
		elif instr[0].name == 'ms':
			targets = instr[1]
			if targets[0].register.name in qsc.registers:
				if targets[1].register.name in qsc.registers:
					block.append(qsc.build_gate('MS', *[qsc.registers[target.register.name][target.index] for target in targets], *[float(param) for param in instr[0].params]))
				else:
					raise QSCOUTError("Gate register %s invalid!" % targets[1].register.name)
			else:
				raise QSCOUTError("Gate register %s invalid!" % targets[0].register.name)
		else: # TODO: Check native gateset and determine allowed gates accordingly.
			raise QSCOUTError("Instruction %s not available on trapped ion hardware; try unrolling first." % instr[0].name)
	qsc.gate('measure_all')
	return qsc
