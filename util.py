import time 
from gauss_solver import solve
import numpy as np

import random

def framePrep(fnum):
   if(fnum > 2715647 or fnum < 0):
      return Exception("Invalid frame number")
   #11 spots, equivalent to a max representation of 2047 which also gives the logical amount of possible numbers above
   t1 = fnum // 1326
   #5 spots
   t2 = fnum % 26
   #6 spots
   t3 = fnum % 51
   return [int(digit) for digit in bin(t1)[2:].zfill(11) + bin(t2)[2:].zfill(5) + bin(t3)[2:].zfill(6)]

#Gives a random TDMA frame numbers
def randomTDMA():
   #There are 2715648 possible numbers
   return random.randint(0, 2715647)

def randomSeededTDMA(seed):
   random.seed(seed)
   return random.randint(0, 2715647)

def majority(a, b, c):
   return (a * b) ^ (a * c) ^ (b * c)

def right_shift_register(register):
   if isinstance(register, list):
      return register[-1:] + register[:-1]
   else:
      return np.roll(register, 1, axis=0)

def triangle(n):
   return n * (n + 1) // 2

def formula(a, b, n):
   if b > a:
      b, a = a, b
   return a + (triangle(n - 1) - (n - 1)) - triangle((n-1) - b - 1) - 1

# Given the dependencies equations and the values, this function will solve for the register variables and the linearized variables
def reverse_setup_registers(eqs, x):
   out = []

   for line in eqs:
      for v in line:
         out.append(v)

   x = np.array(x)
   eqs = np.array(eqs)
   M = np.hstack((eqs, x.reshape(-1,1)))

   registers_listed = solve(M)

   II = 19 + (19*18 // 2)
   III = 19 + (19*18 // 2) + 22 + (22*21 // 2)

   R1 = registers_listed[0:19]
   R2 = registers_listed[II   : II + 22]
   R3 = registers_listed[III  : III + 23]

   L1 = registers_listed[19:II]
   L2 = registers_listed[II + 22:III]
   L3 = registers_listed[III + 23:]
   
   return R1, R2, R3, L1, L2, L3


#Check R1;15 for 1, R2;16 for 1, R3;18 for 1, R4;10 for 1
def check_for_ones(r1, r2, r3, r4):
   if r1[15] != 1: raise Exception('r1[15]')
   if r2[16] != 1: raise Exception('r2[16]')
   if r3[18] != 1: raise Exception('r3[18]')
   if r4[10] != 1: raise Exception('r4[10]')

def generateTranslate(n):
   trans = {}
   for a in range(n):
      for b in range(n):
         if a == b: 
            continue
         trans[formula(a, b, n)] = [a,b]
   return trans

#Check linearized variables compared to ordinary variables
def check_linearized(r1, linr1, r2, linr2, r3, linr3):
   t1 = generateTranslate(19)
   t2 = generateTranslate(22)
   t3 = generateTranslate(23)
   errorList = []
   #r1
   for i, val in enumerate(linr1):
      v1, v2 = t1[i]
      actualval = r1[v1] * r1[v2]
      if actualval != val:
         errorList.append(f'Linearized variable {(v1,v2)} at index {i} in R1 was {val} but should be {actualval}' )
   #r2
   for i, val in enumerate(linr2):
      v1, v2 = t2[i]
      actualval = r2[v1] * r2[v2]
      if actualval != val:
         errorList.append(f'Linearized variable {(v1,v2)} at index {i} in R1 was {val} but should be {actualval}' )
   #r3
   for i, val in enumerate(linr3):
      v1, v2 = t3[i]
      actualval = r3[v1] * r3[v2]
      if actualval != val:
         errorList.append(f'Linearized variable {(v1,v2)} at index {i} in R1 was {val} but should be {actualval}' )
   return errorList


def gen_R4(i):
    assert 0 <= i < 2**16
    R4 = [int(digit) for digit in bin(i)[2:].zfill(16)]

    R4.insert(10, 1)
    
    return R4

