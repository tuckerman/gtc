"""
Zeros of Generalized Toric Codes
Configurations in K_q^n
configurations.py 

Cameron Tuckerman
"""

from elements import *
from groups import *
from polynomials import *
import convexhull

class V:
	"""
	Position vector of a point in a configuration
	"""

	def __init__(self,q,p):
		self._q = q
		if isinstance(p,M):
			self._v = p
			self._p = [i.i for i in p[0]]
		else:
			self._p = p
			self._v = M([[EC(i,q-1) for i in p]])

	def __repr__(self):
		return "<V " + str(self._v) + ">"

	def __hash__(self):
		return hash(tuple(self._p))

	def __str__(self):
		toreturn = ""
		for i in self:
				toreturn = toreturn + str(i) + ","
		return "(" + toreturn[:-1] + ")"

	def __iter__(self):
		return iter(self._v[0])

	def __getitem__(self, key):
		return self._v[0][key]

	def __len__(self):
		return len(self._v[0])

	def __eq__(self, other):
		return (self._v == other._v)

	def __lt__(self, other):
		if len(self) < len(other):
			default = True
			l = len(self)
		else:
			default = False
			l = len(other)
		for i in range(l):
			if self[i] < other[i]:
				return True
			elif self[i] > other[i]:
				return False
		return default

	def __rmul__(self, other):
		return V(self._q,other[0] + (self._v * other[1]))

class Config:
	"""
	Configuration of points
	"""

	def __init__(self,q,P):
		self._q = q
		if isinstance(P[0],V):
			self._V = sorted(P)
			self._P = [v._p for v in self._V]
		else:
			self._P = sorted(P)
			self._V = [V(q,p) for p in self._P]
		self._d = len(self._P[0])

	def __repr__(self):
		return "<Config " + str(self._V) + ">"

	def __hash__(self):
		return hash(tuple(iter(self)))

	def __str__(self):
		toreturn = ""
		for i in self:
			toreturn = toreturn + str(i) + ","
		return "{" + toreturn[:-1] + "}"

	def __iter__(self):
		return iter(self._V)

	def __getitem__(self,key):
		return self._V[key]

	def __len__(self):
		return len(self._V)

	def __eq__(self,other):
		return (self._V == other._V)

	def __lt__(self, other):
		if len(self) < len(other):
			default = True
			l = len(self)
		else:
			default = False
			l = len(other)
		for i in range(l):
			if self[i] < other[i]:
				return True
			elif self[i] > other[i]:
				return False
		return default

	def __rmul__(self,other):
		return Config(self._q,[other*v for v in self])

	def orbit(self,gl=None):
		if hasattr(self,"_orbit"):
			return self._orbit

		if gl is None:
			gl = GL(self._d,self._q-1)
		translations_to_zero = [-1*(i._v) for i in self]
		ZAGL = [[i*j,j] for i in translations_to_zero for j in gl]
		self._orbit = sorted(list(set([g*self for g in ZAGL])))
		#for c in self._orbit: c._orbit = self._orbit
		return self._orbit

	def aglorbit(self):
		if hasattr(self,"_aglorbit"):
			return self._aglorbit

		agl = AGL(self._d,self._q-1)
		self._aglorbit = sorted(list(set([g*self for g in agl])))
		for c in self._aglorbit: c._aglorbit = self._aglorbit
		return self._aglorbit

	def aglorbit_gen(self):
		agl = AGL(self._d,self._q-1)
		for g in agl:
			yield g*self

	def missing_points(self):
		if self._d == 2:
			return convexhull.points(self._P)[1]
		else:
			return None

	def complete_configuration(self):
		if self._d == 2:
			return Config(self._q,convexhull.points(self._P)[0])
		else:
			return None

	def always_generalized(self):
		if self._d != 2: return None

		if len(self.missing_points()) == 0:
			return False
		for i in self.aglorbit_gen():
			if len(i.missing_points()) == 0:
				return False
		return True

	def size_convex_hull(self):
		return len(self._P) + len(self.missing_points())

	def svg(self):
		if (self._d != 2): return ""
		step = int(200/(self._q-2))
		maxsize = step*(self._q-2)
		s = ""
		for y in range(0,201,step):
			s = s + "<line x1=\"0\" x2=\""+str(maxsize)+"\" y1=\""+str((200-y))+"\" y2=\""+str(200-y)+"\" style=\"stroke: black;\" />" + "\n"
		for x in range(0,201,step):
			s = s + "<line y1=\"0\" y2=\""+str(maxsize)+"\" x1=\""+str(x)+"\" x2=\""+str(x)+"\" style=\"stroke: black;\" />" + "\n"
		for p in self._P:
			s = s + "<circle cx=\""+str(step*p[0])+"\" cy=\""+str(200-step*p[1])+"\" r=\"5\" style=\"stroke:black;fill:black;\"/>" + "\n"
		for p in self.missing_points():
			s = s + "<circle cx=\""+str(step*p[0])+"\" cy=\""+str(200-step*p[1])+"\" r=\"5\" style=\"stroke:black;fill:red;\"/>" + "\n"
		svg_intro = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"200\" height=\"200\" viewBox=\"0 0 220 220\">"
		trans_intro = "<g transform=\"translate(10,10)\">"
		trans_end = "</g>"
		svg_end = "</svg>"
		return svg_intro + trans_intro + s + trans_end + svg_end

	def z(self,regen=False):
		if hasattr(self,"_zeros") and not regen:
			return self._zeros
		polynomial = Polynomial(self._q,self._P)
		self._zeros = polynomial.max_zeros()
		return self._zeros





if __name__ == "__main__":
	q = 8
	c = Config(q,[[0,0],[1,1],[2,2]])
	p = Polynomial(q,c._P)
	print(c.z())
	print(c.z())
	
