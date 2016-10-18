import json
import sys

config1 = json.load(open(sys.argv[1]))
config2 = json.load(open(sys.argv[2]))

for key in sorted(config1.keys()):
    try:
        if config2[key] != config1[key]:
            print("--->DIFF : {}".format(key))
        else:
            print("    EQUAL: {}".format(key))
    except KeyError:
        print("--->NOKEY: {}".format(key))
