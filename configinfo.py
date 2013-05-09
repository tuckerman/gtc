import argparse
import pickle

from configurations import *
from representatives import *
import convexhull

parser = argparse.ArgumentParser(description='Analyzing a single configuration')
parser.add_argument('-q', default=False, nargs=1, metavar="q", help='GF(q)')
parser.add_argument('-p', default=False, nargs="+", metavar="[x,y]", help='points')
args = vars(parser.parse_args())
q = int(args['q'][0])
points = []
for p in args['p']:
	ints = [int(i) for i in p[1:-1].split(",")]
	points.append(ints)
c = Config(q,points)
print(c)
while(True):
	print("size_orbit, orbit, size_aglorbit, aglorbit, missing_points, always_generalized, size_convex_hull, svg, z")
	action = input(">")
	if action == "orbit":
		o = c.orbit()
		for x in o:
			print(str(x))
	if action == "size_orbit":
		print(len(c.orbit()))
	if action == "aglorbit":
		o = c.aglorbit()
		for x in o:
			print(str(x))
	if action == "size_aglorbit":
		print(len(c.aglorbit()))
	if action == "missing_points":
		print(c.missing_points())
	if action == "always_generalized":
		print(c.always_generalized())
	if action == "size_convex_hull":
		print (c.size_convex_hull())
	if action == "svg":
		print (c.svg())
	if action == "z":
		print (c.z())
	if action == "hull":
		print (convexhull.vertices_convex_hull(c._P))
