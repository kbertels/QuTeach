# OpenQL Syntax 

from openql import openql as ql		# Import the openql library
import os							# For pathname access

curdir = os.path.dirname(__file__)						# Get the path of this python code file
output_dir = os.path.join(curdir, 'cqasm_files')		# From pathname of cqasm output from OpenQL on compilation
ql.set_option('output_dir', output_dir)					# Set output directory pathname in OpenQL
ql.set_option('write_qasm_files', 'yes')				# Set option to generate qasm output (Default: no)
# ql.set_option('optimize', 'no')						# Not so useful for us currently
# ql.set_option('scheduler', 'ASAP')					# Not so useful for us currently
# ql.set_option('log_level', 'LOG_INFO')				# Not so useful for us currently
# ql.set_option('use_default_gates', 'yes')				# Not so useful for us currently
		
config_fn  = os.path.join(curdir, 'config_qx.json')		# From pathname of hardware specification
platform   = ql.Platform('platform_none', config_fn)	# Set hardware specification (should be minimalistic for QX simulator)

num_qubits = 3											# You need to know number of qubits before initiating the program/kernel
p = ql.Program('exercise_qasm_001', platform, num_qubits)	# Declare the program on the platform
k1 = ql.Kernel("kernel_1", platform, num_qubits)				# Declare a kernel on the platform

# NOTE: The final result does not matter for this experiment. This is just to get famalier with the syntax of using different gates.


k1.prepz(0)				# Initialize qubit 0 to |0> (Default is also |0> state, so strictly not required, just for good practice)

q_num = 1
k1.prepz(q_num)			# Initialize a specific qubit (thus can be initialized in a loop)

k1.gate('prep_z', [2])	# Alternative syntax (recommended, not compatible with old version though)

# Single Qubit gates

k1.gate('x', [0])		# Pauli-X
k1.gate('y', [1])		# Pauli-Y
k1.gate('z', [2])		# Pauli-Z

k1.gate('h', [0])		# Hadamard
k1.gate('hadamard', [0])# Alternate syntax

k1.gate('i', [0])
k1.gate('identity', [0])

k1.gate('s', [0])
k1.gate('sdag', [0])

k1.gate('t', [0])
k1.gate('tdag', [0])

k1.gate('rx', [0], 0, 0.15)	# Arbitrary rotation about X (angle in radian, last argument)
k1.gate('ry', [0], 0, 0.15)	# Arbitrary rotation about Y (angle in radian, last argument)
k1.gate('rz', [0], 0, 0.15)	# Arbitrary rotation about Z (angle in radian, last argument)

# k1.gate('rx90', [0])	# Not so useful for algorithms
# k1.gate('ry90', [0])	# Not so useful for algorithms
# k1.gate('mrx90', [0])	# Not so useful for algorithms
# k1.gate('mry90', [0])	# Not so useful for algorithms

# 2 Qubit gates

k1.gate('swap', [0, 1])	# Swap gate

k1.gate('cz', [0, 1])	# CZ with qubit 0 and qubit 1
k1.gate('cphase', [0, 1])	# Alternate syntax

q_control = 0
q_target = 1
k1.gate('cnot', [q_control, q_target])		# CNOT with qubit 0 as control and qubit 1 as target

# 3 Qubit gates

q_c1 = 0
q_c2 = 1
q_tgt = 2
toffoli_arg = [q_c1, q_c2, q_target]
k1.gate('toffoli', toffoli_arg)				# Toffoli (CC-NOT) with qubit 0 and 1 as control and qubit 2 as target. You can directly pass the argument vector.

k1.display()				# Display the internal state vector

k2 = ql.Kernel("kernel_2", platform, num_qubits)				# Declare a kernel on the platform

k2.measure(0)
k2.measure(1)
k2.gate('measure', [2])		# Alternate syntax (recommended, not compatible with old version though)

k2.display()				# The superposition is destroyed on measurement

# p.set_sweep_points(sweep_points)
        
p.add_kernel(k1)			# Add the kernel to the program
p.add_kernel(k2)			# Add the kernel to the program
# p.add_kernel(k2)			# Add the kernel to the program again (since the superposition has already collapsed, there will be no change in output)

p.compile()					# Compile the program (this generates the cqasm files if the option is set)

qasm = p.qasm()				# Get the cqasm generated by OpenQL
print(qasm)