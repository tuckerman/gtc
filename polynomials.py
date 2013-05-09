"""
Zeros of Generalized Toric Codes
Polynomials
polynomials.py 

Cameron Tuckerman
"""

from elements import *
from groups import *
from fields import *
from itertools import *

class Polynomial:
	def __init__(self,q,powers):
		self._q = q
		self._powers = powers
		self._field = GF(q)
		self._l = len(powers)
		self._d = len(powers[0])

	def eval(self,point,c):
		field = self._field
		result = field[0]
		for i in range(self._l):
			m = c[i]
			for j in range(self._d):
				m = m * (point[j]**self._powers[i][j])
			result = result +  m
		return result

	def max_zeros(self):
		field = self._field
		zero = field[0]

		coefficients = list(product(list(field),repeat=self._l))[1:]
		torus = list(product(list(field)[1:],repeat=self._d))

		max_num_zeros = 0
		max_cos = []
		max_roots = []

		for c in coefficients:
			num_zeros = 0
			roots = []
			for p in torus:
				if self.eval(p,c) == zero:
					num_zeros = num_zeros + 1
					roots.append(p)

			if num_zeros > max_num_zeros:
				max_num_zeros = num_zeros
				max_cos = c
				max_roots = roots

		return(max_num_zeros,max_cos,max_roots)

