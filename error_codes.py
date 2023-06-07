import numpy as np

def get_error_code_equations(x, k):

	H = np.hstack( ( np.zeros((272, 456-272)), np.eye(272) )).astype(int) 
	G = np.vstack( ( np.eye(184), np.zeros((456 - 184, 184)) )).astype(int) 

	g = np.zeros(456, dtype=int)

	inner = np.bitwise_xor( (G @ x), g )
	c = np.bitwise_xor(inner, k)

	c = np.bitwise_xor(c, g)
	c = H @ c
	return c