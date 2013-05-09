try:
	import argparse
except ImportError:
	import argparse_backup as argparse
import pickle

from configurations import *
from representatives import *

def makehtml(R):
	if R[0]._d != 2: return "<html>Not d=2</html>"
	s = "<table border=1><tr><td>n</td><td>Configuration</td><td>Max Zeros</td><td>Code</td></tr>\n"
	title = "<h1>GTCZ: Configurations of size "+str(len(R[0]))+" over GF("+str(R[0]._q)+")</h1>"
	n = 0
	for i in R:
		strz = "N/A"
		strcode = "N/A"
		if hasattr(i,"_zeros"):
			zz = i._zeros
			strz = str(zz[0])+"<br>"+str(zz[1])
			strcode = "["+str((i._q-1)**i._d)+","+str(len(i))+","+str((i._q-1)**i._d-zz[0])+"]"
		row = "<tr><td>"+str(n)+"</td><td>"+i.svg()+"<br><center>"+str(i)+"</center></td><td>"+strz+"</td><td>"+str(strcode)+"</td></tr>\n"
		s = s + row
		n = n+1
	return "<html>"+title+s+"</html>"



parser = argparse.ArgumentParser(description='Analyzing Generalized Toric Codes')
parser.add_argument('-c', default=False, nargs=1, metavar="file", help='Create a new file')
parser.add_argument('-i', default=False, nargs=1, metavar="file", help='Import and modify previously created configurations')
args = vars(parser.parse_args())

check_create = args['c']
check_import = args['i']
if (not check_create) and (not check_import):
	print("Error. Run with -h flag for help.")
	exit(0)

if check_create and check_import:
	print("You cannot both create a new configuration and import a new one. Please select one or another.")

badcheck = False
try:
	if check_create:
		badcheck = True
		filename = args['c'][0]
		picklefile = filename+".pickle"
		htmlfile = filename+".html"

		print("Configurations of length \"l\" in dimension \"d\" over GF(\"q\")")
		q = int(input("q: "))
		d = int(input("d: "))
		l = int(input("l: "))
		paction = input("Precompute all configurations? [Y] [N]: ")
		oaction = input("Order by [S]ize of convex hull or [L]exicographically?: ")
		if oaction[0] in ["L","l"]:
			order = False
		else:
			order = True
		if paction[0] in ["Y","y"]:
			repgen = generate_representatives(q,l,d,order)
		else:
			repgen = gen_reps(q,l,d,order)
		badcheck = False
		try:
			reps = []
			for c in repgen:
				print(c)
				reps.append(c)
		except KeyboardInterrupt:
			with open(htmlfile,"w") as f: f.write(makehtml(reps))
			with open(picklefile,"wb") as f: pickle.dump(reps,f)


		print("Representative generation complete!\n\n")
		with open(htmlfile,"w") as f: f.write(makehtml(reps))

	if check_import:
		picklefile = args['i'][0]
		htmlfile = picklefile+".html"
		picklefile = picklefile + ".pickle"
		with open(picklefile,"rb") as f: reps = pickle.load(f)


	print(" [P]rint all representatives\n [N]umber of Representaives\n [S]elect a representative by number\n [Z]eros\n [H]tml generate\n [Q]uit (^C)\n [?] displays these commands")
	while(True):
		
		action = input("> ")
		if action == "?":
			print(" [P]rint all representatives\n [N]umber of Representaives\n [S]elect a representative by number\n [Z]eros\n [H]tml generate\n [Q]uit (^C)\n [?] displays these commands")
		if action in ["q","Q"]:
			break
		if action in ["p","P"]:
			n = 0
			for r in reps:
				print("   ",n, r)
				n = n + 1
		if action in ["n","N"]:
			print("   ",len(reps))
		if action in ["z","Z"]:
			for r in reps:
				print("   ",r,r.z())
				with open(htmlfile,"w") as f: f.write(makehtml(reps))
				with open(picklefile,"wb") as f: pickle.dump(reps,f)
		if action in ["h","H"]:
			with open(htmlfile,"w") as f: f.write(makehtml(reps))
			print("   ","Writing html... Done!")
		if action in ["s","S"]:
			config_n = int(input("# "))
			if config_n >= len(reps):
				continue
			print("  [P]rint configuration\n  [Z]eros of configuration\n  [N]umber of elements in ZAGL orbit\n  [O]rbit\n  [M]issing points\n  [C]onvex Hull\n  [B]ack\n  [?] displays these commands")
			c = reps[config_n]
			notcomplete = None
			while(True):
				action2 = input(">> ")
				if action2 == "?":
					print("  [P]rint configuration\n  [Z]eros of configuration\n  [N]umber of elements in ZAGL orbit\n  [O]rbit\n  [M]issing points\n  [C]onvex Hull\n  [B]ack\n  [?] displays these commands")
				if action2 in ["b","B"]:
					if notcomplete is None:
						break
					else:
						c = notcomplete
						print("   ","Changing selection to",c)
						notcomplete = None
				if action2 in ["n","N"]:
					print("   ",len(c.orbit()))
				if action2 in ["z","Z"]:
					print("   ",c.z())
					with open(htmlfile,"w") as f: f.write(makehtml(reps))
				if action2 in ["p","P"]:
					print("   ",c)
				if action2 in ["o","O"]:
					for x in c.orbit():
						print("   ",x)
				if action2 in ["m","M"]:
					print("   ",c.missing_points())
				if action2 in ["c","C"]:
					if notcomplete is None:
						notcomplete = c
						c = c.complete_configuration()
						print("   ","Changing selection to",c)
					else:
						print("   ","Already viewing convex hull.")
	
	print("Saving progress...")
	with open(htmlfile,"w") as f: f.write(makehtml(reps))
	with open(picklefile,"wb") as f: pickle.dump(reps,f)

except KeyboardInterrupt:
	print()
	if not badcheck:
		print("Saving progress...")
		with open(picklefile,"wb") as f: pickle.dump(reps,f)
	print("Done. Goodbye.")

