from importlib import import_module
import os.path
import re
import sys

if len(sys.argv) < 2: 
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
elif len(sys.argv) == 2 and not os.path.isfile(sys.argv[1]):
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
elif len(sys.argv) == 3 and (not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2])):
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
else:
	paths = os.path.split(os.path.abspath(sys.argv[1]))
	sys.path.insert(0, paths[0])
	g = import_module(os.path.splitext(paths[1])[0])
	if len(sys.argv) == 3:
		prevfile = True
		paths = os.path.split(os.path.abspath(sys.argv[2]))
		sys.path.insert(0, paths[0])
		d = import_module(os.path.splitext(paths[1])[0])
	else:
		prevfile = False

	try:
		print("This program updates the configuration in {}".format(os.path.relpath(sys.argv[1])))
		if prevfile:
			print("Default values will be taken from {}".format(os.path.relpath(sys.argv[2])))
		print("This program updates the video processing and detection parameters.\n")
		print("Press CTRL+c to exit at any time and return to previous values.\n")
		print("Press ENTER to accept the default value, as indicated in")
		print("    parentheses.\n")

		while True:
			print("Enter source video for these parameters.")
			sourcevideo = input("--> ")

			if len(sourcevideo) == 0 or not os.path.isfile(os.path.abspath(sourcevideo)):
				print("Invalid file. Please try again.")
			else:
				break

		while True:
			print("Enter blackframe detection threshold.")
			prompt = "({})".format(str(d.threshold)) if prevfile else "("+str(1)+")"

			threshold = input(prompt+"--> ")
			if len(threshold) == 0:
				if prevfile:
					threshold = d.threshold
					break
				else:
					threshold = 1
					break
			else:
				try:
					if int(threshold) < 1:
						raise ValueError
					else:
						threshold = int(threshold)
						break
				except ValueError:
					print("Threshold should be a positive integer.")

		while True:
			print("Enter time between fades for scene definition.")
			prompt = "({})".format(str(d.gaptime)) if prevfile else "("+str(1)+")"

			gaptime = input(prompt+"--> ")
			if len(gaptime) == 0:
				if prevfile:
					gaptime = d.gaptime
					break
				else:
					gaptime = 1
					break
			else:
				try:
					if int(gaptime) < 1:
						raise ValueError
					else:
						gaptime = int(gaptime)
						break
				except ValueError:
					print("Entry should be a positive integer.")

		while True:
			print("Enter number of scenes to skip at start of video.")
			prompt = "({})".format(str(d.skipstart)) if prevfile else "("+str(0)+")"

			skipstart = input(prompt+"--> ")
			if len(skipstart) == 0:
				if prevfile:
					skipstart = d.skipstart
					break
				else:
					skipstart = 0
					break
			else:
				try:
					if int(skipstart) < 0:
						raise ValueError
					else:
						skipstart = int(skipstart)
						break
				except ValueError:
					print("Scenes to skip should be an integer of 0 or more.")

		while True:
			print("Enter number of scenes to skip at end of video.")
			prompt = "({})".format(str(d.skipend)) if prevfile else "("+str(0)+")"

			skipend = input(prompt+"--> ")
			if len(skipend) == 0:
				if prevfile:
					skipend = d.skipend
					break
				else:
					skipend = 0
					break
			else:
				try:
					if int(skipend) < 0:
						raise ValueError
					else:
						skipend = int(skipend)
						break
				except ValueError:
					print("Scenes to skip should be an integer of 0 or more.")

		while True:
			print("Enter cache file.")
			prompt = "({})".format(str(d.cachefile)) if prevfile else ""

			cachefile = input(prompt+"--> ")

			if len(cachefile) == 0 and prevfile:
				cachefile = d.cachefile
				break
			elif os.path.isdir(os.path.abspath(cachefile)):
				try:
					if cachefile[-1] != os.sep:
						cachefile += os.sep
				except IndexError:
					cachefile = os.curdir+os.sep
				cachefile += "file.cache"
				break
			elif os.path.isdir(os.path.split(os.path.abspath(cachefile))[0]):
				break
			else:
				print("Location invalid. Please try again.")
				print("Directories must be created before running script.")

	except KeyboardInterrupt:
		print("\n\nExiting. No data written to {}".format(os.path.relpath(sys.argv[1])))

	else:
		configData = None
		with open(os.path.abspath(sys.argv[1]), 'r') as configFile:
			configData = configFile.read()

		#For each type, rewrite the first line found, delete the rest.
		matches = re.findall(r"(^threshold.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "threshold = "+str(threshold))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nthreshold = "+str("\""+threshold+"\"")+"\n"

		matches = re.findall(r"(^gaptime.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "gaptime = "+str(gaptime))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\ngaptime = "+str("\""+gaptime+"\"")+"\n"

		matches = re.findall(r"(^skipstart.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "skipstart = "+str(skipstart))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nskipstart = "+str(skipstart)+"\n"

		matches = re.findall(r"(^skipend.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "skipend = "+str(skipend))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nskipend = "+str(skipend)+"\n"

		matches = re.findall(r"(^cachefile.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "cachefile = \""+str(cachefile)+"\"")
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\ncachefile = "+str(cachefile)+"\n"

		with open(os.path.abspath(sys.argv[1]), 'w') as configFile:
			configFile.write(configData)

		try:
			with open(os.path.abspath(cachefile), 'r') as cacheFile:
				cacheData = cacheFile.read()

			matches = re.findall(r"(^"+re.escape(os.path.abspath(sourcevideo))+".*$)", cacheData, re.M)
			if len(matches):
				for x in matches:
					cacheData = cacheData.replace(x, "")

			with open(os.path.abspath(cachefile), 'w') as cacheFile:
				cacheFile.write(cacheData)
		except FileNotFoundError:
			pass

		print("\n\nData written to {}".format(os.path.relpath(sys.argv[1])))
