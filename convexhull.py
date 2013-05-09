"""
Zeros of Generalized Toric Codes
Configurations in K_q^n
convexhull.py 

Acknowledgements: Algorithms based on those used by polymake. 

Cameron Tuckerman
"""

def compare(a,b):
	if a < b: return -1
	elif a > b: return 1
	else: return 0

def between(a,b,x):
	"""
	Returns True if a-x-b
	"""

	check_slope = (b[0] - a[0]) * (x[1] - a[1]) == (x[0] - a[0]) * (b[1] - a[1])
	check_x = abs(compare(a[0], x[0]) + compare(b[0], x[0])) <= 1
	check_y = abs(compare(a[1], x[1]) + compare(b[1], x[1])) <= 1
	return (check_slope and check_x and check_y)

def right_turn(p,q,r):
	if (q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - q[0]*p[1] - r[0]*q[1] - p[0]*r[1]) < 0:
		return True
	else:
		return False

def vertices_convex_hull(P):
	points = sorted(P)
	upper = [points[0], points[1]]
	for p in points[2:]:
		upper.append(p)
		while len(upper) > 2 and not right_turn(*upper[-3:]):
			del upper[-2]

	points = points[::-1]
	lower = [points[0], points[1]]
	for p in points[2:]:
		lower.append(p)
		while len(lower) > 2 and not right_turn(*lower[-3:]):
			del lower[-2]

	return upper + lower[1:-1]

def contained_in_polygon(x,V):
	if len(V) == 2:
		return between(V[0],V[1],x)

	for i in range(len(V[:-1])):
		a, b = V[i], V[i+1]
		if between(a,b,x):
			break
		if not right_turn(a,b,x):
			return False
	a, b = V[-1], V[0]
	if between(a,b,x):
		return True
	if not right_turn(a,b,x):
		return False

	return True

def convex_polytope(V):
	xs = sorted([p[0] for p in V])
	ys = sorted([p[1] for p in V])
	minx, maxx = xs[0], xs[-1]+1
	miny, maxy = ys[0], ys[-1]+1
	possible_points = [[x,y] for x in range(minx,maxx) for y in range(miny,maxy)]
	return [p for p in possible_points if contained_in_polygon(p,V)]

def points(P):
	V = vertices_convex_hull(P)
	hull = convex_polytope(V)
	missing = [i for i in hull]
	for p in P:
		missing.remove(p)
	return [hull,missing]










if __name__ == "__main__":
	P = [[1],[2],[3]]
	V = vertices_convex_hull(P)
	print(V)
	print(len(convex_polytope(V)))
	print(missing_points(P))