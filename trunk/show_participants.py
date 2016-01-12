from importlib import import_module
from natsort import natsorted
import sys

from get_telemetry import get_telemetry
#import replay_globals as g
g = import_module(sys.argv[2][:-3])

if len(sys.argv) != 2:
	print("Usage: 'python'"+sys.argv[0]+" <packetdirectory>'")

else:
	get_telemetry(sys.argv[1])
	#string = "\n".join("{0:>2}: {1}".format(sorted([(int(i), str(n)) for (i, n) in g.participantData])))
	string = "\n".join(["{0:>2}: {1}".format(x, y) for (x, y) in sorted([(int(i), str(n)) for (i, n) in g.participantData])])
	#string = "\n".join(natsorted(["{0:>2}: {1}".format(int(i), n) for (i, n) in g.participantData]))
	print(string)
