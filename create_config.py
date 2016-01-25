from importlib import import_module
import os.path
import re
import sys

def finish_array(array, prevarray=None):
	if prevarray == None:
		try:
			array += [array[-1]]*(len(g.participantData)-len(array))
		except IndexError:
			array = [None for x in range(len(g.participantData))]
	else:
		array = array+prevarray[len(array):]

	return array

def add_data(array, index, value, prevarray=None, failvalue=""):
	if len(str(value)) == 0:
		if prevarray != None:
			array.insert(index, prevarray[index])
		else:
			try:
				array.insert(index, array[index-1])
			except IndexError:
				array.insert(index, failvalue)
	else:
		array.insert(index, value)
	
	return array

if len(sys.argv) < 2: 
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
elif len(sys.argv) == 2 and not os.path.isfile(sys.argv[1]):
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
elif len(sys.argv) == 3 and (not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2])):
	print("Usage: 'python'"+sys.argv[0]+" <configfile> [<previousconfigfile>]'")
else:
	from get_telemetry import get_telemetry

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
		print("This program updates the source video, source telemetry, output")
		print("    video, and point structure for the project, and the car, team,")
		print("    and previous points earned for each driver.\n")
		print("Press CTRL+c to exit at any time and return to previous values.\n")
		print("Press ENTER to accept the default value, as indicated in")
		print("    parentheses.\n")
		print("Input -1 to use the default value for car, team, or points for")
		print("    the remaining participants.")

		showCar = True
		showPoint = True

		while True:
			print("Include team data?")
			showTeam = input('[Y/n]--> ')
			if len(showTeam) == 0 or str.lower(showTeam) == 'y':
				showTeam = True
				writeTeam = True
				teams = list()
				break;
			elif str.lower(showTeam) == 'n':
				showTeam = False
				writeTeam = False
				break;
		
		while True:
			print("Enter source video file name:") 
			prompt = "({})".format(d.sourcevideo) if prevfile else ""
			sourcevideo = input(prompt+"--> ")

			if len(sourcevideo) == 0 and prevfile:
				sourcevideo = d.sourcevideo
				break
			elif os.path.isfile(os.path.abspath(sourcevideo)):
				break
			else:
				print("Not a file. Please try again.")

		while True:
			print("Enter output video file name:")
			prompt = "({})".format(d.outputvideo) if prevfile else ""
			outputvideo = input(prompt+"--> ")

			if len(outputvideo) == 0 and prevfile:
				outputvideo = d.outputvideo
				break
			elif os.path.isdir(os.path.split(os.path.abspath(outputvideo))[0]):
				break
			else:
				print("Output video location invalid. Please try again.")
				print("Directories must be created before running script.")

		while True:
			print("Enter source telemetry directory:")
			prompt = "({})".format(d.sourcetelemetry) if prevfile else ""
			sourcetelemetry = input(prompt+"--> ")

			if len(sourcetelemetry) == 0 and prevfile:
				sourcetelemetry = d.sourcetelemetry
				break
			elif os.path.isdir(os.path.abspath(sourcetelemetry)):
				if sourcetelemetry[-1] != os.sep:
					sourcetelemetry += os.sep
				break
			else:
				print("Not a directory. Please try again.")

		pointStructure = list()
		while True:
			print("Enter bonus points for fastest lap in race:")
			prompt = "({})".format(str(d.pointStructure[0])) if prevfile else ""
			newPoint = input(prompt+"--> ")
			if len(newPoint) == 0 and prevfile:
				pointStructure.insert(0, int(d.pointStructure[0]))
				break;
			else:
				try:
					pointStructure.insert(0, int(newPoint))
					break;
				except ValueError:
					print("Points should be entered as integers.")

		while True:
			position = len(pointStructure)
			print("Enter 0 to finish points structure.")
			if prevfile:	
				print("Enter -1 to use previous values for remaining positions.")
			print("Enter points scored for finish position {}".format(position))
			try:
				prompt = "({})".format(str(d.pointStructure[position])) if prevfile else ""
			except IndexError:
				prompt = ""

			newPoint = input(prompt+"--> ")
			if newPoint == "0":
				break;
			elif newPoint == "-1" and prevfile:
				pointStructure = finish_array(pointStructure, d.pointStructure)
				break;
			elif len(newPoint) == 0 and prevfile:
				if d.pointStructure[position] == 0:
					break;
				else:
					pointStructure.insert(position, int(d.pointStructure[position]))
			else:
				try:
					pointStructure.insert(position, int(newPoint))
				except ValueError:
					print("Points should be entered as integers.")

		cars = list()
		points = list()
		get_telemetry(sourcetelemetry)
		
		for i, name in sorted([(int(x), str(n)) for x, n, *rest in g.participantData]):
			if showCar:
				print("Enter car for {}:".format(name))
				try:
					prompt = "({})".format(d.carData[i] if prevfile else cars[i-1])
				except IndexError:
					prompt = ""
				car = input(prompt+"--> ")

				if car == "-1":
					showCar = False
					if prevfile:
						cars = finish_array(cars, d.carData)
					else:
						cars = finish_array(cars)
				else:
					if prevfile:
						cars = add_data(cars, i, car, d.carData)
					else:
						cars = add_data(cars, i, car)

			if showTeam:
				print("Enter team for {}:".format(name))
				try:
					prompt = "({})".format(d.teamData[i] if prevfile else teams[i-1])
				except IndexError:
					prompt = ""
				team = input(prompt+"--> ")

				if team == "-1":
					showTeam = False
					if prevfile:
						teams = finish_array(teams, d.teamData)
					else:
						teams = finish_array(teams)
				else:
					if prevfile:
						teams = add_data(teams, i, team, d.teamData)
					else:
						teams = add_data(teams, i, team)

			if showPoint:
				while True:
					print("Enter points earned in previous series races for {}:".format(name))
					try:
						prompt = "({})".format(str(d.points[i]) if prevfile else str(points[i-1]))
					except IndexError:
						prompt = ""
					point = input(prompt+"--> ")

					if point == "-1":
						showPoint = False
						if prevfile:
							points = finish_array(points, d.points)
						else:
							points = finish_array(points)
						break;
					else:
						try:
							if prevfile:
								if len(point) == 0:
									points = add_data(points, i, point, d.points, 0)
								else:	
									point = int(point)
									points = add_data(points, i, point, d.points, 0)
								break;
							else:
								if len(point) == 0:
									points = add_data(points, i, point, None, 0)
								else:	
									point = int(point)
									points = add_data(points, i, point, None, 0)
								break;
						except ValueError:
							print("Points should be entered as an integer number.")
			
	except KeyboardInterrupt:
		print("\n\nExiting. No data written to {}".format(os.path.relpath(sys.argv[1])))
	else:
		configData = None
		with open(os.path.abspath(sys.argv[1]), 'r') as configFile:
			configData = configFile.read()

		#For each type, rewrite the first line found, delete the rest.
		matches = re.findall(r"(^sourcevideo.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "sourcevideo = "+str("\""+sourcevideo+"\""))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nsourcevideo = "+str("\""+sourcevideo+"\"")+"\n"

		matches = re.findall(r"(^sourcetelemetry.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "sourcetelemetry = "+str("\""+sourcetelemetry+"\""))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\nsourcetelemetry = "+str("\""+sourcetelemetry+"\"")+"\n"

		matches = re.findall(r"(^outputvideo.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "outputvideo = "+str("\""+outputvideo+"\""))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\noutputvideo = "+str(outputvideo)+"\n"

		matches = re.findall(r"(^pointStructure.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "pointStructure = "+str(pointStructure))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\npointStructure = "+str(pointStructure)+"\n"

		matches = re.findall(r"(^carData.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "carData = "+str(cars))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\ncarData = "+str(cars)+"\n"

		matches = re.findall(r"(^teamData.*$)", configData, re.M)
		if len(matches):
			if writeTeam:
				configData = configData.replace(matches[0], "teamData = "+str(teams))
				for x in matches[1:]:
					configData = configData.replace(x, "")
			else:
				configData = configData.replace(matches[0], "teamData = [None for x in range(64)]")

				for x in matches[1:]:
					configData = configData.replace(x, "")
		else:
			configData += "\nteamData = "+str(teams)+"\n"

		matches = re.findall(r"(^points.*$)", configData, re.M)
		if len(matches):
			configData = configData.replace(matches[0], "points = "+str(points))
			for x in matches[1:]:
				configData = configData.replace(x, "")
		else:
			configData += "\npoints = "+str(points)

		with open(os.path.abspath(sys.argv[1]), 'w') as configFile:
			configFile.write(configData)

		print("\n\nData written to {}".format(os.path.relpath(sys.argv[1])))
