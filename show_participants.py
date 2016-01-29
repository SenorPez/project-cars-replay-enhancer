from importlib import import_module
import os.path
import sys

if len(sys.argv) != 2:
	print("Usage: 'python3 "+sys.argv[0]+" <configfile>'")

else:
	from get_telemetry import get_telemetry
	paths = os.path.split(os.path.abspath(sys.argv[1]))
	sys.path.insert(0, paths[0])
	g = import_module(os.path.splitext(paths[1])[0])
	get_telemetry(g.sourcetelemetry)
	string = "\n".join(["{0:>2}: {1}".format(x, y) for (x, y) in sorted([(int(i), str(n)) for i, n, *rest in g.participantData])])
	print(string)
