"""
Zeros of Generalized Toric Codes
Galois Fields
fields.py 

Cameron Tuckerman
"""

from elements import *

prime_gen = {2:1,3:2,5:2,7:3,11:2,4:"a",8:"a"}
add_table = {2:[[0,1],[1,0]],3:[[0,1,2],[1,2,0],[2,0,1]],5:[[0,1,2,3,4],[1,2,3,0,3],[2,4,3,1,0],[3,0,1,4,2],[4,3,0,2,1]],7:[[0,1,2,3,4,5,6],[1,3,5,2,0,6,4],[2,5,4,6,3,0,1],[3,2,6,5,1,4,0],[4,0,3,1,6,2,5],[5,6,0,4,2,1,3],[6,4,1,0,5,3,2]],11:[[0,1,2,3,4,5,6,7,8,9,10],[1,2,9,5,7,10,0,6,4,3,8],[2,9,3,10,6,8,1,0,7,5,4],[3,5,10,4,1,7,9,2,0,8,6],[4,7,6,1,5,2,8,10,3,0,9],[5,10,8,7,2,6,3,9,1,4,0],[6,0,1,9,8,3,7,4,10,2,5],[7,6,0,2,10,9,4,8,5,1,3],[8,4,7,0,3,1,10,5,9,6,2],[9,3,5,8,0,4,2,1,6,10,7],[10,8,4,6,9,0,5,3,2,7,1]],4:[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],8:[[0,1,2,3,4,5,6,7],[1,0,6,4,3,7,2,5],[2,6,0,7,5,4,1,3],[3,4,7,0,1,6,5,2],[4,3,5,1,0,2,7,6],[5,7,4,6,2,0,3,1],[6,2,1,5,7,3,0,4],[7,5,3,2,6,1,4,0]]}


class GF:
	"""
	Galois Field
	"""

	def __init__(self,q):
		if q in [2,3,5,7,9,11]:
			self._p = q
			self._n = 1
		elif q == 4:
			self._p = 2
			self._n = 2
		elif q == 8:
			self._p = 2
			self._n = 3
		a = prime_gen[self.q]
		self._add_table = add_table[self._p**self._n]
		self._e = [FE(self,0,0)]+[FE(self,a,i) for i in range(self.q-1)]

	@property
	def p(self):
		return self._p

	@property
	def n(self):
		return self._n

	@property
	def q(self):
		return self.p**self.n
	
	def __repr__(self):
		return "GF("+str(self.n)+")"

	def __hash__(self):
		return self.q

	def __iter__(self):
		return iter(self._e)

	def __len__(self):
		return self.q

	def __getitem__(self,key):
		return self._e[key]

	def mul(self,x,y):
		if x.a == 0 or y.a == 0:
			return self[0]
		else:
			return self[1:][(x.n+y.n)%(self.q-1)]

	def pow(self,x,n):
		if x.a == 0:
			return self[0]
		else:
			return self[1:][(x.n*int(n))%(self.q-1)]

	def add(self,x,y):
		if x.a == 0:
			return y
		elif y.a == 0:
			return x
		else:
			return self[self._add_table[(x.n+1)][y.n+1]]


if __name__ == "__main__":
	f = GF(7)
	print(f[4],f[3])
	print(f[4].n,f[4].n)
	
