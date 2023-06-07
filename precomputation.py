import time
import numpy as np
from A52_cipher import A52_cipher
from A52_equation import A52_equation
from util import *
from kc_reverse import findKc
import math
import time
import subprocess

def toBytes(eqs):
	out = bytearray()

	for line in eqs:
		out += (bytearray([int("".join(map(str, line[i:i+8])), 2) for i in range(0, len(line), 8)]))
	return out

def pre_compute():
	for chunk in range(65):
		file_name = str(chunk).zfill(3) + ".bin"
		file = open(file_name, 'wb')
		file_data = bytearray()
		print("chunk", chunk)
		chunkSize = 1_000
		for i in range(chunkSize):
			
			R4 = gen_R4(i + chunk * chunkSize) 
			a52_equation_instances = A52_equation(R4)
			eqNeeded = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2)
			eqs = a52_equation_instance.get_interval_values(eqNeeded)
			file_data += toBytes(eqs)
		print("writing to file", file_name)

		file.write(file_data)
		time.sleep(1)
		subprocess.run(["gzip", file_name]) 

def test_load_time(file_name):
	eqNeeded = 19 + (19*18 // 2) + 22 + (22*21 // 2) + 23 + (23*22 // 2)
	f = open(file_name, 'rb')
	for i in range(eqNeeded // 8 + 1):

		currentData = f.read((i+1) * math.ceil(eqNeeded / 8))
		print("reading file done")
		a = time.time()
		lines = []
		for b in currentData[0: eqNeeded // 8]:
			lines += ( [int(bt) for bt in bin(b)[2:].zfill(8) ]  )

		b = currentData[eqNeeded // 8]		
		lines += ( [int(bt) for bt in bin(b)[2:].zfill(7) ]  )
		print(len(np.array(lines)))

		print("load done", time.time() -a)
		break
	return

test_load_time('000.bin')