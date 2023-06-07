#!/usr/bin/python3

from A52_cipher import A52_cipher
from A52_equation import A52_equation
from util import *
from kc_reverse import findKc

from error_codes import get_error_code_equations


def solve_for_719_unknowns(Kc, f): 
	print("--- Starting solve for 719 unknowns. Including finding Kc ---")
	a52_cipher_instance = A52_cipher(Kc, f)
	R1, R2, R3, R4 = a52_cipher_instance.setup()

	eqNeeded = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2)
	x = a52_cipher_instance.generate_keystream(eqNeeded)

	a52_equation_instance = A52_equation(R4)
	eqs = a52_equation_instance.get_interval_values(eqNeeded)

	reversed_R1, reversed_R2, reversed_R3, reversed_L1, reversed_L2, reversed_L3 = reverse_setup_registers(eqs, x)
	
	print("reversed R1", reversed_R1)
	print("actual   R1", R1)
	print("reversed == actual:",  reversed_R1 == R1)

	print("reversed R2", reversed_R2)
	print("actual   R2", R2)
	print("reversed == actual:",  reversed_R2 == R2)

	print("reversed R3", reversed_R3)
	print("actual   R3", R3)
	print("reversed == actual:",  reversed_R3 == R3)


	reversed_Kc = solve_kc_given_setup_register(R1, R2, R3, R4, f)

	check_for_ones(reversed_R1, reversed_R2, reversed_R3, R4)

	info = check_linearized(reversed_R1, reversed_L1, reversed_R2, reversed_L2, reversed_R3, reversed_L3)
	assert len(info) == 0

	print("linearization check and 1 constant check successful")

	print("actual   Kc:", Kc)
	print("Reversed Kc:", reversed_Kc)
	print("reversed = Kc:", Kc == reversed_Kc)


def solve_kc_given_setup_register(R1, R2, R3, R4, f):
	return findKc(R1, R2, R3, R4, f)


def brute_force(Kc, f):

	print("--- Starting brute force attempts, showing 10 random R4 will not work ---")
	a52_cipher_instance = A52_cipher(Kc, f)
	R1, R2, R3, R4 = a52_cipher_instance.setup()

	eqNeeded = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2) 
	x = a52_cipher_instance.generate_keystream(eqNeeded)


	R4_tries = []
	for i in range(10):
		R4_tries.append(gen_R4(i))

	R4_tries.append(R4)
	for i, R4_test in enumerate(R4_tries):

		
		a52_equation_instance = A52_equation(R4_test)
		eqs = a52_equation_instance.get_interval_values(eqNeeded)

		reversed_R1, reversed_R2, reversed_R3, reversed_L1, reversed_L2, reversed_L3 = reverse_setup_registers(eqs, x)
		if i == 10:
			print("trying with actual R4. expecting to work now")

		print("Brute force attempt:", i+1)

		print("actual   registers:", R1, R2, R3)
		print("Reversed registers:", reversed_R1, reversed_R2, reversed_R3)
		

		try:
			check_for_ones(reversed_R1, reversed_R2, reversed_R3, R4)
		except:
			print("1 constant check failed")


		info = check_linearized(reversed_R1, reversed_L1, reversed_R2, reversed_L2, reversed_R3, reversed_L3)
		try:
			assert len(info) == 0
		except:
			print("linearization check failed")

def solve_for_655_unknowns():	
	print("--- Starting solve for 655 unknowns ---")
	ori_R1 = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
	ori_R2 = [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1]
	ori_R3 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
	ori_R4 = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

	ori_R1[15] = ori_R2[16] = ori_R3[18] = 1 

	eq = A52_equation(ori_R4)

	eqNeeded = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2) 

	unknown_vars = eq.get_interval_values((eqNeeded - 3))
	ci = A52_cipher(None, 	None)

	ci.customRegisters(ori_R1, ori_R2, ori_R3, ori_R4)

	values = np.array(ci.generate_keystream(eqNeeded - 3), dtype=int)

	M = np.hstack((unknown_vars, values.reshape(-1,1)))

	II = 19 + (19*18 // 2)
	III = 19 + (19*18 // 2) + 22 + (22*21 // 2)

	M = np.vstack([M, np.zeros(eqNeeded + 1, dtype=int), 
		np.zeros(eqNeeded + 1, dtype=int), 
		np.zeros(eqNeeded + 1, dtype=int)])

	M[-1, 15] = 1
	M[-1, -1] = 1

	M[-2, II + 16] = 1
	M[-2, -1] = 1

	M[-3, III + 18] = 1
	M[-3, -1] = 1

	def map(r):
		if r == 1:
			offset = 19
			normalVarOffset = 0
			n = 19
			k = 15
		elif r == 2:
			offset = 19 + (19*18 // 2) + 22
			normalVarOffset = 19 + (19*18 // 2)
			n = 22
			k = 16
		elif r == 3:
			offset = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23
			normalVarOffset = 19 + (19*18 // 2) + 22 + (22*21 // 2)
			n = 23
			k = 18

		out = []
		for i in range(n):
			if i == k:
				continue
			out.append( {"index":offset + formula(k, i, n),
			"name": normalVarOffset + i
			} )

		return out

	for r_index in [1,2,3]:
		out = map(r_index)
		for fix in out:
			index = fix.get('index') #lineared variable
			var = fix.get('name') #normal variable

			for i in range(len(M)):
				M[i, var] =  M[i, var] ^ M[i, index]
				M[i, index] = 0


	dat = []

	for i in range(720):
		if list((M[:,i])) == [0] * 719:
			pass
		else:
			dat.append(M[:,i])

	M = np.array(dat).T
	for i in range(61):
		M = np.delete(M, (0), axis=0)

	print("Equation matrix height is:", M.shape[1])
	deciphered = list(solve(M))

	R1 = (deciphered[0:19])
	R2 = (deciphered[19 + 18*17 // 2: 19 + 18*17 // 2 + 22])
	R3 = (deciphered[19 + 18*17 // 2 + 22 + 21 * 20 // 2: 19 + 18*17 // 2 + 22 + 21 * 20 // 2 + 23])

	print("reversed R1", R1)
	print("actual   R1", ori_R1)
	print("reversed == actual:",  ori_R1 == R1)

	print("reversed R2", R2)
	print("actual   R2", ori_R2)
	print("reversed == actual:",  ori_R2 == R2)

	print("reversed R3", R3)
	print("actual   R3", ori_R3)
	print("reversed == actual:",  ori_R3 == R3)

	try:
	    check_for_ones(R1, R2, R3, ori_R4)
	except Exception as e:
	    print('Found a required 1 as 0 in ', str(e))


def error_code_test(kc, f):

	print("--- Starting solve with error_codes ---")

	a52_cipher_instance = A52_cipher(Kc, f)
	R1, R2, R3, R4 = a52_cipher_instance.setup()

	a52_equation_instance = A52_equation(R4)

	eqs = a52_equation_instance.get_interval_values(456 * 3)
	keystream = a52_cipher_instance.generate_keystream(456 * 3)


	threeMatrixes = [None] * 3
	relevant_keystream = np.array([], dtype=int)

	for i in range(3):
		
		plain_text = (np.random.rand(1000) < 0.5).astype(int)

		x = np.array(plain_text[i*184: (i+1) * 184])
		k = np.array(keystream[i*456: (i+1) * 456])

		err_codes = get_error_code_equations(x, k)

		threeMatrixes[i] = eqs[(i+1) * 456 - 272: (i+1) * 456]

		relevant_keystream = np.concatenate((relevant_keystream,  err_codes))


	eqs_data = np.vstack( ( threeMatrixes[0], threeMatrixes[1], threeMatrixes[2]))

	reversed_R1, reversed_R2, reversed_R3, reversed_L1, reversed_L2, reversed_L3 = reverse_setup_registers(eqs_data, relevant_keystream)

	print("reversed R1", reversed_R1)
	print("actual   R1", R1)
	print("reversed == actual:",  reversed_R1 == R1)

	print("reversed R2", reversed_R2)
	print("actual   R2", R2)
	print("reversed == actual:",  reversed_R2 == R2)

	print("reversed R3", reversed_R3)
	print("actual   R3", R3)
	print("reversed == actual:",  reversed_R3 == R3)


Kc = [0,1,1,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,0,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,1,1]
f  = framePrep(100)


solve_for_719_unknowns(Kc, f)
print()
solve_for_655_unknowns()
print()
brute_force(Kc, f)
print()
error_code_test(Kc, f)

