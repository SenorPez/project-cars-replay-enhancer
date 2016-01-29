import csv
from importlib import import_module
import os.path
import sys

from process_telemetry import process_telemetry

def get_telemetry(telemetryDirectory, telemetryFile='tele.csv'):
	paths = os.path.split(os.path.abspath(sys.argv[1]))
	sys.path.insert(0, paths[0])
	g = import_module(os.path.splitext(paths[1])[0])

	try:
		f = open(telemetryDirectory+telemetryFile, 'r')
	except FileNotFoundError:
		process_telemetry(telemetryDirectory)
		f = open(telemetryDirectory+telemetryFile, 'r')
	finally:
		csvdata = csv.reader(f)

	try:
		for row in csvdata:
			if int(row[1]) & 3 == 0:
				g.telemetryData.append(row)
			elif int(row[1]) & 3 == 1:
				for p in enumerate(row[6:-1]):
					if len(p[1]):
						g.participantData.append(p)
			elif int(row[1]) & 3 == 2:
				for p in enumerate(row[3:-1], int(row[2])):
					if len(p[1]):
						g.participantData.append(p)
			else:
				raise ValueError("ValueError: Unrecognized packet type ("+str(int(row[1]) & 3)+")")

		g.participantData = [(i, n, t, c) for (i, n), t, c in zip(list(sorted({x for x in g.participantData})), g.teamData, g.carData)]

		try:
			raceEnd = [i for i, data in reversed(list(enumerate(g.telemetryData))) if int(data[9]) & int('111', 2) == 3][0] + 1
		except IndexError:
			raceEnd = len(g.telemetryData)

		try:
			raceFinish = [i for i, data in reversed(list(enumerate(g.telemetryData[:raceEnd]))) if int(data[9]) & int('111', 2) == 2][0] + 1
		except IndexError:
			raceFinish = len(g.telemetryData)

		try:
			raceStart = [i for i, data in reversed(list(enumerate(g.telemetryData[:raceFinish]))) if int(data[9]) & int('111', 2) == 0][0] + 1
		except IndexError:
			raceStart = 0

		#For some reason, the telemetry doesn't immediately load the stadndings before a race. Step through until we do have them.
		while sum([int(g.telemetryData[raceStart][182+i*9]) & int('01111111', 2) for i in range(56)]) == 0:
			raceStart += 1

		g.telemetryData = g.telemetryData[raceStart:raceEnd]

		#Add cumulative time index to end of data structure.
		lastTime = 0
		addTime = 0
		for i, data in enumerate(g.telemetryData):
			if float(data[13]) == -1:
				g.telemetryData[i] = data+[-1]
			else:
				if float(data[13]) < lastTime:
					addTime = lastTime + addTime
				g.telemetryData[i] = data+[float(data[13])+addTime]
				lastTime = float(data[13])
		
	except ValueError as e:
		print("{}".format(e), file=sys.stderr)
	finally:
		f.close()
