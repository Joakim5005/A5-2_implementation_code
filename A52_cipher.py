from util import majority, right_shift_register

class A52_cipher:
	def __init__(self, Kc, f):
		self.clear()
		self.Kc = Kc
		self.f = f
		self.isSetupDone = False

	def clear(self):
		self.R1 = [0] * 19
		self.R2 = [0] * 22
		self.R3 = [0] * 23
		self.R4 = [0] * 17
		self.isSetupDone = False

	def customRegisters(self, R1, R2, R3, R4):
		self.R1 = R1
		self.R2 = R2
		self.R3 = R3
		self.R4 = R4
		self.isSetupDone = True

	def shift_register(self, index):
		if index == 1: 
			carry = self.R1[13] ^ self.R1[16] ^ self.R1[17] ^ self.R1[18]
			self.R1 = right_shift_register(self.R1)
			self.R1[0] = carry
		elif index == 2:
			carry = self.R2[20] ^ self.R2[21]
			self.R2 = right_shift_register(self.R2)
			self.R2[0] = carry
		elif index == 3:
			carry = self.R3[7] ^ self.R3[20] ^ self.R3[21] ^ self.R3[22]
			self.R3 = right_shift_register(self.R3)
			self.R3[0] = carry
		elif index == 4:
			carry = self.R4[11] ^ self.R4[16]
			self.R4 = right_shift_register(self.R4)
			self.R4[0] = carry

	def clock_all_registers(self):
		self.shift_register(1)
		self.shift_register(2)
		self.shift_register(3)
		self.shift_register(4)

	def tick_clocking_unit(self):
		majority_bit = majority(self.R4[10], self.R4[3], self.R4[7])

		if majority_bit == self.R4[10]:
			self.shift_register(1)
		if majority_bit == self.R4[3]:
			self.shift_register(2)
		if majority_bit == self.R4[7]:
			self.shift_register(3)
		self.shift_register(4)

	def get_output_stream_bit(self):
		return (self.R1[-1] ^ self.R2[-1] ^ self.R3[-1] 
			^ majority(self.R1[12], 1 ^ self.R1[14], self.R1[15]) 	
			^ majority(self.R2[9], self.R2[13], 1 ^ self.R2[16])  	   
			^ majority(1 ^ self.R3[13], self.R3[16], self.R3[18]))

	def setup(self):
		self.clear()
		for i in range(64):
			self.clock_all_registers()
			self.R1[0] ^= self.Kc[i]
			self.R2[0] ^= self.Kc[i]
			self.R3[0] ^= self.Kc[i]
			self.R4[0] ^= self.Kc[i]

		for i in range(22):
			self.clock_all_registers()
			self.R1[0] ^= self.f[i]
			self.R2[0] ^= self.f[i]
			self.R3[0] ^= self.f[i]
			self.R4[0] ^= self.f[i]

		self.R1[15] = 1
		self.R2[16] = 1
		self.R3[18] = 1
		self.R4[10] = 1

		self.isSetupDone = True
		return self.R1, self.R2, self.R3, self.R4

	def generate_keystream(self, n):

		if self.isSetupDone == False:
			self.setup()

		keystream = [0] * n

		for _ in range(100):
			self.tick_clocking_unit()

		for k in range(n):
			self.tick_clocking_unit()
			keystream[k] = self.get_output_stream_bit()
		
		return keystream