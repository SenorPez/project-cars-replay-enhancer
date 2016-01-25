from importlib import import_module
import os.path
import re
import sys

if len(sys.argv) != 2: 
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
elif len(sys.argv) == 2 and not os.path.isfile(sys.argv[1]):
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
else:
	paths = os.path.split(os.path.abspath(sys.argv[1]))
	sys.path.insert(0, paths[0])
	g = import_module(os.path.splitext(paths[1])[0])

	try:
		print("This program updates the configuration in {}".format(os.path.relpath(sys.argv[1])))
		print("This program updates the 'racestart' value to synchronize")
		print("    telemetry with the video.\n")
		print("Entering a number sets the 'racestart' value.")
		print("Preface that number with a + or - to adjust the 'racestart' value.\n")
		print("Press CTRL+c to exit at any time and return to previous values.\n")
		print("Press ENTER to accept the default value, as indicated in")
		print("    parentheses.\n")

		while True:
			print("Current racestart value: {}".format(g.racestart))
			print("Enter a number or adjustment.")

			newracestart = input("--> ")
			racestart = float(g.racestart)

			try:
				if newracestart[0] == "+":
					racestart += float(newracestart[1:])
				elif newracestart[0] == "-":
					racestart -= float(newracestart[1:])
				else:
					racestart = float(newracestart)
			except ValueError:
				print("Bad value detected. Racestart can be a decimal value.")
			else:
				break

	except KeyboardInterrupt:
		print("\n\nExiting. No data written to {}".format(os.path.relpath(sys.argv[1])))

	else:
		configData = None
		with open(os.path.abspath(sys.argv[1]), 'r') as configFile:
			configData = configFile.read()

		matches = re.findall(r"(^racestart.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "racestart = "+str(racestart))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nracestart = "+str(racestart)+"\n"

		with open(os.path.abspath(sys.argv[1]), 'w') as configFile:
			configFile.write(configData)

		print("\n\nData written to {}".format(os.path.relpath(sys.argv[1])))
