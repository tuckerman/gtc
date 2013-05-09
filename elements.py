"""
Zeros of Generalized Toric Codes
Group/Field Elements
elements.py 

Cameron Tuckerman
"""

from fractions import gcd


class EC:
	"""
	Equivalence class of integers mod n
	"""

	def __init__(self, i, n):
		self._i = i
		self._n = n

	@property
	def i(self):
		return self._i % self._n

	@property
	def n(self):
		return self._n

	def __repr__(self):
		return "<EC " + str(self.i) + " mod " + str(self.n) + ">"

	def __hash__(self):
		return hash(int(self))

	def __str__(self):
		return str(self.i)

	def __int__(self):
		return self.i

	def __eq__(self, other):
		if type(other) is type(self):
			if (self.n == other.n):
				if (self.i == other.i):
					return True
				else:
					return False
			else:
				return NotImplemented
		else:
			return NotImplemented

	def __lt__(self, other):
		if type(other) is type(self):
			if (self.n == other.n):
				if (self.i < other.i):
					return True
				else:
					return False
			else:
				return NotImplemented
		else:
			return NotImplemented

	def __add__(self, other):
		if type(other) is type(self):
			if self.n == other.n:
				return EC(int(self)+int(other), self.n)
			else:
				return
		else:
			return EC(int(self)+int(other), self.n)

	def __radd__(self, other):
		return self+other

	def __sub__(self, other):
		if type(other) is type(self):
			if self.n == other.n:
				return EC(int(self)-int(other), self.n)
			else:
				return
		else:
			return EC(int(self)-int(other), self.n)

	def __mul__(self, other):
		if type(other) is type(self):
			if self.n == other.n:
				return EC(int(self)*int(other), self.n)
			else:
				return
		else:
			return EC(int(self)*int(other), self.n)

	def __rmul__(self, other):
		return self*other

	def __pow__(self, other):
		return EC(pow(self.i,int(other),self.n),self.n)

	def __neg__(self):
		return EC(-int(self), self.n)



class M:
	"""
	2 dimensional matrix
	"""
	
	def __init__(self,m):
		self._m = m

	@property
	def size(self):
		return (len(self._m),len(self._m[0]))

	@property
	def m(self):
		return self._m

	def __repr__(self):
		return "<Matrix " + str(hash(self)) + ">"

	def __hash__(self):
		t = tuple([tuple(i) for i in self])
		return hash(tuple(t))

	def __str__(self):
		return str(self._m)

	def __iter__(self):
		return iter(self._m)

	def __getitem__(self, key):
		return self._m[key]

	def __len__(self):
		return len(self._m)

	def __eq__(self, other):
		return self.m == other.m

	def __add__(self, other):
		if self.size == other.size:
			matrix = [[self[i][j] + other[i][j] for j in range(self.size[1])] for i in range(self.size[0])]
			return M(matrix)
		else:
			return NotImplemented

	def __mul__(self, other):
		if (type(other) is type(self)) or (type(other) is type([1])):
			if self.size[1] == other.size[0]:
				m = self.size[0]
				n = self.size[1]
				p = other.size[1]
				matrix = [[sum([self[i][k] * other[k][j] for k in range(n)]) for j in range(p)] for i in range(m)]
				return M(matrix)
			else:
				return NotImplemented
		else:
			return NotImplemented

	def __rmul__(self, other):
		return M([[other*j for j in i] for i in self])

	def __neg__(self, other):
		return -1*self

	def det(self):
		if self.size[0] == self.size[1]:
			if self.size[0] == 1:
				return self[0][0]
			elif self.size[1] == 2:
				return self[0][0]*self[1][1] - self[0][1]*self[1][0] 
			if self.size[0] == 3:
				return self[0][0]*(self[1][1]*self[2][2]-self[1][2]*self[2][1]) - self[0][1]*(self[1][0]*self[2][2]-self[1][2]*self[2][0]) + self[0][2]*(self[1][0]*self[2][1]-self[1][1]*self[2][0])
		else:
			return NotImplemented


class FE:
	"""
	Element of a Finite Field
	"""

	def __init__(self,f,a,n):
		self._a = a
		self._n = n
		self._f = f

	@property
	def field(self):
		return self._f

	@property
	def a(self):
		return self._a

	@property
	def n(self):
		return self._n

	def __repr__(self):
		return str(self.a)+"^"+str(self.n)

	def __hash__(self):
		return self.i

	def __int__(self):
		if self.a == 0:
			return self.field[0]
		else:
			return self.field[1:][self.n]

	def __eq__(self,other):
		return (self.field == other.field) and (self.a == other.a) and (self.n == other.n)

	def __add__(self,other):
		return self.field.add(self,other)

	def __mul__(self,other):
		return self.field.mul(self,other)

	def __pow__(self,other):
		return self.field.pow(self,other)

if __name__ == "__main__":
	m1 = M([[2,0]])
	m2 = M([[2,3],[3,2]])
	print(m1*m2)
