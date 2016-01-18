from importlib import import_module
from natsort import natsorted
import sys

from get_telemetry import get_telemetry
#import replay_globals as g

if len(sys.argv) != 2:
	print("Usage: 'python'"+sys.argv[0]+" <configfile'")

else:
	g = import_module(".".join(sys.argv[1][:-3].split('/')[1:]))
	get_telemetry(g.sourcetelemetry)
	string = "\n".join(["{0:>2}: {1}".format(x, y) for (x, y) in sorted([(int(i), str(n)) for i, n, *rest in g.participantData])])
	print(string)
