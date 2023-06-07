import numpy as np
from util import formula, majority, right_shift_register


# Product function that calcualte the XOR AND / multiplacation between two dependency vectors
# xor_with_one is needed if any 1 constants are in the input.
def product(a: np.ndarray, b: np.ndarray, xor_with_one=0):
	assert a.shape == b.shape
	registerSize = a.shape[0]

	variables = np.zeros(registerSize + ((registerSize * (registerSize - 1)) // 2), dtype=int)
	for i in range(registerSize):
		if a[i] == 0:
			continue
		for j in range(registerSize):
			if b[j] == 0:
				continue
			if i == j:		
				variables[j] = 1
			else:
				variables[formula(i, j, registerSize) + registerSize] ^= 1
	
	if xor_with_one == 1:
		for i in range(len(b)):
			if b[i] == 1:
				variables[i] ^= 1

	elif xor_with_one == 2:
		for i in range(len(a)):
			if a[i] == 1:
				variables[i] ^= 1
	

	return variables

# majority function is dependency vector
def majority_with_equations(a, b, c, xor_constants=[0,0,0]):
	a = (
		(product(a, b, xor_with_one=xor_constants[0]) 
			^ product(a, c, xor_with_one=xor_constants[1])
			^ product(b, c, xor_with_one=xor_constants[2])))
	return a

class A52_equation:
	def __init__(self, R4):
		self.R1 = np.eye(19, k=0, dtype=int)
		self.R2 = np.eye(22, k=0, dtype=int)
		self.R3 = np.eye(23, k=0, dtype=int)
		self.R4 = np.array(R4)

	def r1_tick(self):
		carry = self.R1[13] ^ self.R1[16] ^ self.R1[17] ^  self.R1[18]
		self.R1 = right_shift_register(self.R1)
		self.R1[0] = carry

	def r2_tick(self):
		carry = self.R2[20] ^ self.R2[21]
		self.R2 = right_shift_register(self.R2)
		self.R2[0] = carry

	def r3_tick(self):
		carry = self.R3[7] ^ self.R3[20] ^ self.R3[21] ^ self.R3[22]
		self.R3 = right_shift_register(self.R3)
		self.R3[0] = carry

	def r4_tick(self):
		carry = self.R4[11] ^ self.R4[16]
		self.R4 = right_shift_register(self.R4)
		self.R4[0] = carry

	def get_r1_vector(self):
		a = np.concatenate((self.R1[-1], np.zeros((19*18) // 2)))
		b = majority_with_equations(self.R1[12], self.R1[14], self.R1[15], xor_constants=[2, 0, 1])
		return np.logical_xor(a, b)

	def get_r2_vector(self):
		a=np.concatenate((self.R2[-1], np.zeros((22*21) // 2)))
		b=majority_with_equations(self.R2[9], self.R2[13], self.R2[16], xor_constants=[0, 2, 2])
		return np.logical_xor(a, b)

	def get_r3_vector(self):
		return np.logical_xor(np.concatenate((self.R3[-1], np.zeros((23*22) // 2))), majority_with_equations(self.R3[13], self.R3[16], self.R3[18], xor_constants=[1, 1, 0]))

	def get_interval_values(self, n):
		out = np.zeros((n, 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2)), dtype=int)
		
		for _ in range(100):
			self.tick_clocking_unit()
		
		for k in range(n):
			self.tick_clocking_unit()
			out[k] = np.concatenate((self.get_r1_vector(), self.get_r2_vector(), self.get_r3_vector()), axis=0)
		return out

	def tick_clocking_unit(self):
		majority_bit = majority(self.R4[10], self.R4[3], self.R4[7])

		if majority_bit == self.R4[10]:
			self.r1_tick()
		if majority_bit == self.R4[3]:
			self.r2_tick()
		if majority_bit == self.R4[7]:
			self.r3_tick()
		self.r4_tick()