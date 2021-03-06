# Quantum Ripple Carry Adder (2-bit)

from openql import openql as ql
import os

curdir = os.path.dirname(__file__)
output_dir = os.path.join(curdir, 'cqasm_files')
ql.set_option('output_dir', output_dir)
ql.set_option('write_qasm_files', 'yes')

config_fn  = os.path.join(curdir, 'config_qx.json')
platform   = ql.Platform('platform_none', config_fn)

num_qubits = 7	# MSQ [c2 b1 a1 c1 b0 a0 c0] LSQ
p = ql.Program('exercise_qasm_005', platform, num_qubits)

def sum(k,a0,b0,s0):	# S0 = (A0+B0) MOD 2
	k.gate('cnot', [a0,s0])
	k.gate('cnot', [b0,s0])

def carry(k,c0,a0,b0,c1):
	k.gate('toffoli', [a0,b0,c1])
	k.gate('cnot', [a0,b0])
	k.gate('toffoli', [c0,b0,c1])

def rcarry(k,c0,a0,b0,c1):
	k.gate('toffoli', [c0,b0,c1])
	k.gate('cnot', [a0,b0])
	k.gate('toffoli', [a0,b0,c1])

k1 = ql.Kernel("initialize", platform, num_qubits)
for i in range(0, num_qubits):
	k1.gate('prep_z', [i])	# Initialize all qubits to |0>
k1.gate('x', [2])	# a = 10
k1.gate('x', [4])	# b = 01
k1.display()
p.add_kernel(k1)

k2 = ql.Kernel("adder", platform, num_qubits)

carry(k2,0,1,2,3)
carry(k2,3,4,5,6)
k2.gate('cnot',[4,5])
sum(k2,4,3,5)
rcarry(k2,0,1,2,3)
sum(k2,1,0,2)

k2.display()
p.add_kernel(k2)

p.compile()

qasm = p.qasm()			# Get the cqasm generated by OpenQL
print(qasm)