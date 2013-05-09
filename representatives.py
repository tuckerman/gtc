"""
Zeros of Generalized Toric Codes
Representative Configurations
representatives.py 

Cameron Tuckerman
"""

from itertools import product
from itertools import combinations
from os import system
import sys
from operator import mul
from functools import reduce

from elements import *
from groups import *
from configurations import *

nCk = lambda n,k: int(round(
    reduce(mul, (float(n-i)/(i+1) for i in range(k)), 1)
))

def generate_all_configurations(q,l,d):
	print("Generating all possible configurations... ",end="")
	all_points = [list(i) for i in product(range(q-1),repeat=d)]
	zero = all_points[0]
	all_l_combinations = [[zero] + list(i) for i in combinations(all_points[1:],l-1)]
	print("Done!")
	return sorted([Config(q,i) for i in all_l_combinations])

def gen_configs(q,l,d):
	all_points = [list(i) for i in product(range(q-1),repeat=d)]
	zero = all_points[0]
	for i in combinations(all_points[1:],l-1):
		yield Config(q, [zero] + list(i))

def gen_reps(q,l,d,order=True):
	gl = GL(d,q-1)
	configs = gen_configs(q,l,d)
	generated_orbits = []
	total_size_configs = int(nCk((q-1)**d-1,l-1))
	current_size_configs = 0
	for i in configs:
		found = False
		for orbit in generated_orbits:
			try:
				orbit.remove(i)
				found = True
				break
			except ValueError:
				pass
		if found:
			continue
		else:
			o = i.orbit(gl)
			current_size_configs += len(o)
			generated_orbits.append(o)
			rep = o[0]
			if order:
				for j in o:
					if j.size_convex_hull() < rep.size_convex_hull():
						rep = j
			yield rep
			if current_size_configs == total_size_configs:
				break

		
def generate_representatives(q,l,d,order=True):
	configs = generate_all_configurations(q,l,d)
	print("Generating General Linear Group... ",end="")
	gl = GL(d,q-1)
	print("Done!")
	while len(configs) > 0:
		c = configs[0]
		o = c.orbit(gl)
		configs = list(set(configs).difference(o))
		rep = o[0]
		if order:
			for i in o:
				if i.size_convex_hull() < rep.size_convex_hull():
					rep = i
		yield rep

def generate_representatives_2(q,l,d):
	configs = generate_all_configurations(q,l,d)

	gl = GL(d,q-1)
	print("GL Done")
	while len(configs) > 0:
		c = configs[0]
		o = c.orbit(gl)
		rep = o[0]
		repsize = rep.size_convex_hull()
		for i in o:
			if i.size_convex_hull() < repsize:
				rep = i
				repsize = rep.size_convex_hull()
			configs.remove(i)
		yield rep





if __name__ == "__main__":
	t1 = 0
	for i in gen_reps(5,7,2):
		print(i,i.size_convex_hull(),len(i._orbit))
		t1 = t1 + len(i._orbit)
	print("t1:",t1)
	# t2 = 0
	# for i in generate_representatives(5,7,2):
	# 	print(i,i.size_convex_hull(),len(i._orbit))
	# 	t2 = t2 + len(i._orbit)
	# print("t2:",t2)
	