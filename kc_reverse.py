import numpy as np

from gauss_solver import solve
from util import right_shift_register

def shift_all_registers(R1, R2, R3, R4):
		
		carry = R1[13] ^ R1[16] ^ R1[17] ^ R1[18]
		R1 = right_shift_register(R1)
		R1[0] = carry

		carry = R2[20] ^ R2[21]
		R2 = right_shift_register(R2)
		R2[0] = carry

		carry = R3[7] ^ R3[20] ^ R3[21] ^ R3[22]
		R3 = right_shift_register(R3)
		R3[0] = carry

		carry = R4[11] ^ R4[16]
		R4 = right_shift_register(R4)
		R4[0] = carry

		return R1, R2, R3, R4


def findKc(r1_vals, r2_vals, r3_vals, r4_vals, frameNumber):
	R1 = np.zeros( (19, 65), dtype=int)
	R2 = np.zeros( (22, 65), dtype=int)
	R3 = np.zeros( (23, 65), dtype=int)
	R4 = np.zeros( (17, 65), dtype=int)

	identity_matrix = np.eye(65, dtype=int)

	for i in range(64):
		R1, R2, R3, R4 = shift_all_registers(R1, R2, R3, R4)
		R1[0] ^= identity_matrix[i]
		R2[0] ^= identity_matrix[i]
		R3[0] ^= identity_matrix[i]
		R4[0] ^= identity_matrix[i]

	for i in range(len(frameNumber)):
		R1, R2, R3, R4 = shift_all_registers(R1, R2, R3, R4)
		R1[0][64] ^= frameNumber[i]
		R2[0][64] ^= frameNumber[i]
		R3[0][64] ^= frameNumber[i]
		R4[0][64] ^= frameNumber[i]

	#Xor found register vals with the constant column
	R1[:, 64] ^= r1_vals
	R2[:, 64] ^= r2_vals
	R3[:, 64] ^= r3_vals
	R4[:, 64] ^= r4_vals

	#Set equations for the key bits that are forced as 1 to all 0 and solve equations
	R1[15]=np.zeros(65)
	R2[16]=np.zeros(65)
	R3[18]=np.zeros(65)
	R4[10]=np.zeros(65)
	
	M = np.vstack((R1, R2, R3, R4))

	out = solve(M)

	return out[0:64]
