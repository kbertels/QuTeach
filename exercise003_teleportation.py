# Quantum Teleportation

from openql import openql as ql
import os

curdir = os.path.dirname(__file__)
output_dir = os.path.join(curdir, 'cqasm_files')
ql.set_option('output_dir', output_dir)
ql.set_option('write_qasm_files', 'yes')

config_fn  = os.path.join(curdir, 'config_qx.json')
platform   = ql.Platform('platform_none', config_fn)

num_qubits = 3
p = ql.Program('exercise_qasm_003', platform, num_qubits)
k1 = ql.Kernel("initialize", platform, num_qubits)

for i in range(0, num_qubits):
	k1.prepz(i)				# Initialize all qubits to |0>

k1.gate('x', [0])		# Set data qubit to 0, 1 or any other state

k1.display()
p.add_kernel(k1)

k2 = ql.Kernel("entangle", platform, num_qubits)

k2.gate('h', [1])
k2.gate('cnot', [1,2])

k2.display()
p.add_kernel(k2)

k3 = ql.Kernel("teleport", platform, num_qubits)

k3.gate('cnot', [0,1])
k3.gate('h', [0])

k3.display()
p.add_kernel(k3)

# .encode  
#    measure q0
#    measure q1
# .decode
#    cx b1,q2
#    cz b0,q2

p.compile()

qasm = p.qasm()			# Get the cqasm generated by OpenQL
print(qasm)