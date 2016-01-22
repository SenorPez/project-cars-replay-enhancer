import csv
import curses
import sys
import time

def displayPosition(stdscr, tData, pData):
	startTime = -1

	for data in tData:
		stdscr.redrawwin()
		#Race not yet started.
		if int(data[9]) & int('111', 2) == 1:
			#stdscr.clear()
			stdscr.addstr(0, 0, "Waiting...")
			stdscr.refresh()
		#Race underway
		elif int(data[9]) & int('111', 2) == 2:
			if startTime == -1:
				startTime = time.time()
				stdscr.clear()
				stdscr.addstr(0, 0, "Press any key to begin race!")
				stdscr.refresh()
				stdscr.getkey()
				stdscr.clear()

				sectorBests = [-1, -1, -1]
				personalBests = [[-1, -1, -1] for x in range(64)]
				bestLap = -1
				personalBestLaps = [-1 for x in range(64)]
				lastLaps = [[-1, -1, -1] for x in range(64)]
				curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
				curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

			standings = sorted({(int(data[182+i*9]), n, int(data[184+i*9]), i) for (i, n) in pData})
			#stdscr.clear()
			stdscr.addstr(0, 0, "Current Lap: {}".format(max(standings, key=lambda x: x[2])[2]))
			stdscr.addstr(1, 0, "Current Time: {:.3f}".format(float(data[13])))
			for i, standing in enumerate(standings, 2):
				stdscr.addstr(i, 0, "{:>2}: {:<30.30s}".format(int(standing[0]) & int('01111111', 2), standing[1]))
				sector = int(data[185+standing[3]*9]) & int('111', 2)
				stdscr.addstr(i, 15+sector*20, "{:20.20s}".format(' '))
				
				if float(data[186+standing[3]*9]) != -123:
					if sector == 1:
						printSector = 3
						if lastLaps[standing[3]][0] != float(data[186+standing[3]*9]):
							lastLaps[standing[3]][0] = float(data[186+standing[3]*9])

						if bestLap == -1 or bestLap >= sum(lastLaps[standing[3]]):
							bestLap = sum(lastLaps[standing[3]])
							personalBestLaps[standing[3]] = sum(lastLaps[standing[3]])
							stdscr.addstr(i, 15+20*4, "{:^20.3f}".format(float(sum(lastLaps[standing[3]]))), curses.color_pair(1))
						elif personalBestLaps[standing[3]] == -1 or personalBestLaps[standing[3]] >= sum(lastLaps[standing[3]]):
							personalBestLaps[standing[3]] = sum(lastLaps[standing[3]])
							stdscr.addstr(i, 15+20*4, "{:^20.3f}".format(float(sum(lastLaps[standing[3]]))), curses.color_pair(2))
						else:
							stdscr.addstr(i, 15+20*4, "{:^20.3f}".format(float(sum(lastLaps[standing[3]]))))
					else:
						printSector = sector-1

						if sector == 2:
							if lastLaps[standing[3]][1] != float(data[186+standing[3]*9]):
								lastLaps[standing[3]][1] = float(data[186+standing[3]*9])
						else:
							if lastLaps[standing[3]][2] != float(data[186+standing[3]*9]):
								lastLaps[standing[3]][2] = float(data[186+standing[3]*9])

					if sectorBests[printSector-1] == -1 or sectorBests[printSector-1] >= float(data[186+standing[3]*9]):
						sectorBests[printSector-1] = float(data[186+standing[3]*9])
						personalBests[standing[3]][printSector-1] = float(data[186+standing[3]*9])
						stdscr.addstr(i, 15+20*printSector, "{:^20.3f}".format(float(data[186+standing[3]*9])), curses.color_pair(1))
					elif personalBests[standing[3]][printSector-1] == -1 or personalBests[standing[3]][printSector-1] >= float(data[186+standing[3]*9]):
						personalBests[standing[3]][printSector-1] = float(data[186+standing[3]*9])
						stdscr.addstr(i, 15+20*printSector, "{:^20.3f}".format(float(data[186+standing[3]*9])), curses.color_pair(2))
					else:
						stdscr.addstr(i, 15+20*printSector, "{:^20.3f}".format(float(data[186+standing[3]*9])))

			stdscr.addstr(16, 0, "{:>32}".format("Sector Bests:"))
			for n, t in [(x, y) for x, y in enumerate(sectorBests, 1) if y != -1]:
				stdscr.addstr(16, 15+20*n, "{:^20.3f}".format(float(t)))

			if bestLap != -1:
				stdscr.addstr(16, 15+20*4, "{:^20.3f}".format(float(bestLap)))
			
			stdscr.refresh()

	#All done.
	standings = sorted({(int(data[182+i*9]), n, int(data[184+i*9]), i) for (i, n) in pData})
	if sectorBests[2] == -1 or sectorBests[2] >= float(data[186+standings[0][3]*9]):
		sectorBests[2] = float(data[186+standings[0][3]*9])
		personalBests[standings[0][3]][2] = float(data[186+standings[0][3]*9])
		stdscr.addstr(2, 15+20*3, "{:^20.3f}".format(float(data[186+standings[0][3]*9])), curses.color_pair(1))
	elif personalBests[standings[0][3]][2] == -1 or personalBests[standings[0][3]][2] >= float(data[186+standings[0][3]*9]):
		personalBests[standings[0][3]][2] = float(data[186+standings[0][3]*9])
		stdscr.addstr(2, 15+20*3, "{:^20.3f}".format(float(data[186+standings[0][3]*9])), curses.color_pair(2))
	else:
		stdscr.addstr(2, 15+20*3, "{:^20.3f}".format(float(data[186+standings[0][3]*9])))
	
	stdscr.move(1, 0)
	stdscr.clrtoeol()
	stdscr.addstr(1, 0, "Race finished. Press any key to exit!")
	stdscr.refresh()
	stdscr.getkey()
	

if len(sys.argv) == 1:
	print ("Usage: 'python "+sys.argv[0]+" <packetdirectory>'")

else:
	try:
		with open('./'+sys.argv[1]+'tele.csv', 'rb') as f:
			csvdata = csv.reader(f)

			#Split packets into type 0 (telemetry) and types 1 & 2 (participants)
			#tData, pData, aData = zip(*[itertools.izip_longest(t, p, a) for t in csvdata if int(t[1]) & 3 == 0 for x in csvdata if int(x[1]) & 3 == 1 for p in enumerate(x[6:]) if len(p[1]) for y in csvdata if int(y[1]) & 3 == 2 for a in enumerate(y[3:], y[2]) if len(a[1])])

			tData = list()
			pData = list()
			
			for row in csvdata:
				if int(row[1]) & 3 == 0:
					tData.append(row)
				elif int(row[1]) & 3 == 1:
					for p in enumerate(row[6:]):
						if len(p[1]): 
							pData.append(p)
				elif int(row[1]) & 3 == 2:
					for p in enumerate(row[3:], row[2]):
						if len(p[1]):
							pData.append(p)
				else:
					raise ValueError("ValueError: Unrecognized packet type ("+str(int(row[1]) & 3)+")")

		#Because I'm a dirty savescummer, we need to findc the last race, since
		#the earlier ones are savescum scum. Save.
		raceStart = -1
		raceEnd = -1
		for i, data in reversed(list(enumerate(tData))):
			if (int(data[9]) & int('111', 2) == 3) and (raceEnd == -1):
				raceEnd = i+1

			if (int(data[9]) & int('111', 2) == 0) and (raceEnd != -1) and (raceStart == -1):
				raceStart = i+1

		if raceStart == -1 or raceEnd == -1:
			#raise ValueError("ValueError: Couldn't detect raceStart and raceEnd you savescumming scum.")
			raceStart = 0
			raceEnd = -1

		tData = tData[raceStart:raceEnd]
		curses.wrapper(displayPosition, tData, pData)
	
	except ValueError as e:
		print >> sys.stderr, e.message

	except IOError as e:
		print >> sys.stderr, "IOError: %s" % e
