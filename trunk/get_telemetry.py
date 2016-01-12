import csv

from process_telemetry import process_telemetry

import replay_globals as g

def get_telemetry(telemetryDirectory, telemetryFile='tele.csv'):
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
				for p in enumerate(row[6:]):
					if len(p[1]):
						g.participantData.append(p)
			elif int(row[1]) & 3 == 2:
				for p in enumerate(row[3:], row[2]):
					if len(p[1]):
						g.participantData.append(p)
			else:
				raise ValueError("ValueError: Unrecognized packet type ("+str(int(row[1]) & 3)+")")

		g.participantData = {x for x in g.participantData}

		#Because I'm a dirty savescummer, we need to find the last race, since
		#the earlier ones are savescum scum. Save.
		raceStart = -1
		raceEnd = -1

		for i, data in reversed(list(enumerate(g.telemetryData))):
			if (int(data[9]) & int('111', 2) == 3) and (raceEnd == -1):
				raceEnd = i+1
			
			if (int(data[9]) & int('111', 2) == 0) and (raceEnd != -1) and (raceStart == -1):
				raceStart = i+1

		if raceStart == -1 or raceEnd == -1:
			raise ValueError("valueError: Couldn't detect raceStart and raceEnd you savescumming scum. Pass t values manually.")

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
		
	except ValueError:
		print >> sys.stderr, e.message
