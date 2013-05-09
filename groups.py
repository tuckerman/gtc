"""
Zeros of Generalized Toric Codes
Groups
groups.py 

Cameron Tuckerman
"""
from itertools import product

from elements import *



def Z(n):
	"""
	Additive group of integers mod n
	"""

	return [EC(i,n) for i in range(n)]



def U(r):
	"""
	Multiplicative group of integers mod n
	"""

	return [EC(i,r) for i in range(r) if gcd(i,r) == 1]



def GL(n,m):
	"""
	General linear group of n x n matrices over classes of integers mod m
	"""
	all_arrays = [list(i) for i in product(Z(m), repeat=n**2)]
	all_2d_arrays = [[i[j:j+n] for j in range(0, n*n, n)]  for i in all_arrays]
	all_matrices = [M(i) for i in all_2d_arrays]
	return [i for i in all_matrices if i.det() in U(m)]




def AGL(n,m,g=None):
	"""
	Semidirect product of the nth direct power of classes of integers mod m with GL(n,m)
	"""
	if g is None:
		g = [list(i) for i in product(Z(m), repeat=n)]
		gl = GL(n,m)
		return [[M([i]),j] for i in g for j in gl]
	else:
		gl = GL(n,m)
		return [[i,j] for i in g for j in gl]


if __name__ == "__main__":
	x = M([[3,4]])
	print(x)
	print(-1*x)
