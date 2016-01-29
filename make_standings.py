from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, where
import os.path
import PIL.Image as plim
from PIL import ImageDraw
import sys

from format_time import format_time

paths = os.path.split(os.path.abspath(sys.argv[1]))
sys.path.insert(0, paths[0])
g = import_module(os.path.splitext(paths[1])[0])

sectorStatus = [['current', 'none', 'none'] for x in range(64)]
lastLapValid = [True for x in range(64)]
lastLapSectors = [[-1, -1, -1] for x in range(64)]

currentLaps = [1 for x in range(64)]
lastLapSplits = [-1 for x in range(64)]
leaderET = -1
leaderLapsCompleted = 0

maxLapTime = -1

standings = list()

changeGroup = False
nextChangeTime = -1
currentGroup = 10

def sector_rectangles(data, height):
	invalidColor = (255, 0, 0)
	currentColor = (255, 255, 0)
	raceBestColor = (128, 0, 128)
	personalBestColor = (0, 128, 0)
	baseColor = (255, 255, 255)
	borderColor = (0, 0, 0)
	xPos = 0

	output = plim.new('RGB', (int(g.margin*1.5)+4, height))
	draw = ImageDraw.Draw(output)

	for sector in data:
		if sector == 'invalid':
			fillColor = invalidColor
		elif sector == 'current':
			fillColor = currentColor
		elif sector == 'racebest':
			fillColor = raceBestColor
		elif sector == 'personalbest':
			fillColor = personalBestColor
		elif sector == 'none':
			fillColor = baseColor
		else:
			fillColor = (0, 0, 255)

		draw.rectangle([(xPos, 0), (xPos+int(g.margin/2)+1, height-1)], fill=fillColor, outline=borderColor)
		xPos += int(g.margin/2)+1

	return output

def write_data(material, standings, dataHeight, columnWidths):
	materialWidth = material.size[0]
	lineLength = materialWidth-g.margin*2

	draw = ImageDraw.Draw(material)

	columnPositions = [g.margin*(i+1)+sum(columnWidths[0:i]) if i == 0 else g.margin+g.columnMargin*(i)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]
	yPos = g.margin/2

	for p, n, r, i, s, l, et, lx, cl in standings[:10]+standings[currentGroup:currentGroup+6]:
		for pp, nn, ss, ll, rr in [list(zip((p, n, s, l, r), columnPositions+[0]))]:
			draw.text((pp[1], yPos), str(pp[0]), fill='black', font=g.font)
			draw.text((nn[1], yPos), str(nn[0]), fill='black', font=g.font)


			if isinstance(lastLapSplits[i], int) and lastLapSplits[i] < 0:
				lastLapTime = "{}".format('')
			elif isinstance(lastLapSplits[i], int):
				suffix = " laps" if lastLapSplits[i] > 1 else " lap"
				lastLapTime = "{:+d}".format(lastLapSplits[i])+suffix
			elif isinstance(lastLapSplits[i], float) and lastLapSplits[i] > 0:
				lastLapTime = format_time(lastLapSplits[i])
			elif isinstance(lastLapSplits[i], float):
				lastLapTime = "+"+format_time(lastLapSplits[i]*-1)

			timeWidth = g.font.getsize(lastLapTime)[0]

			tPos = int(materialWidth-g.margin-timeWidth)

			draw.text((tPos, yPos), str(lastLapTime), fill='black', font=g.font)

			draw.line([(g.margin, yPos+dataHeight), (g.margin+lineLength*rr[0], yPos+dataHeight)], fill=(255, 0, 0), width=2)
			draw.line([(g.margin+lineLength*rr[0], yPos+dataHeight), (materialWidth-g.margin, yPos+dataHeight)], fill=(255, 192, 192), width=2)

			material.paste(sector_rectangles(sectorStatus[i], dataHeight), (ss[1]-2, int(yPos)))

			draw.ellipse([(g.margin+lineLength*rr[0]-2, yPos+dataHeight-2), (g.margin+lineLength*rr[0]+2, yPos+dataHeight+2)], fill=(255, 0, 0))

		yPos += dataHeight+g.margin

	return material

def make_material(t, bgOnly=False):
	global maxLapTime

	standings = update_data(t)

	if maxLapTime == 0:
		#Who has the slowest lap?
		splitData = [[float(g.telemetryData[y+1][186+i*9]) for y in where(diff([float(x[186+i*9]) for x in g.telemetryData]) != 0)[0].tolist()] for i in range(56)]
		maxLapTime = max([sum(x[i:i+3]) for x in splitData for i in range(0, len(x), 3)])

	maxMinutes, maxSeconds = divmod(maxLapTime, 60)
	maxHours, maxMinutes = divmod(maxMinutes, 60)

	if maxHours > 0:
		sizeString = "+24:00:00.00"
	elif maxMinutes > 0:
		sizeString = "+60:00.00"
	else:
		sizeString = "+00.00"

	widths = [(g.font.getsize(str(p))[0], g.font.getsize(str(n))[0], int(g.margin*1.5), max([g.font.getsize(str(sizeString))[0], g.font.getsize("+00 laps")[0]])) for p, n, *rest in standings]
	heights = [max(g.font.getsize(str(p))[1], g.font.getsize(str(n))[1], g.font.getsize(str("{:.2f}".format(0.00)))[1]) for p, n, *rest in standings]
	dataHeight = max(heights)

	heights = [dataHeight for x in standings[:16]]

	columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
	text_width = sum(columnWidths)+g.columnMargin*(len(widths[0])-1)
	text_height = sum(heights)+g.margin*(len(heights)-1)

	material = plim.new('RGBA', (text_width+g.margin*2, text_height+g.margin))
	yPos = 0

	for i, r in enumerate(standings[:16]):
		if i % 2:
			materialColor = (255, 255, 255, 128)
		else:
			materialColor = (192, 192, 192, 128)

		dataMaterial = plim.new('RGBA', (text_width+g.margin*2, dataHeight+g.margin), materialColor)
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+g.margin
	
	return material if bgOnly else write_data(material, standings, dataHeight, columnWidths)

def update_data(t):
	global leaderLapsCompleted
	global leaderET

	global changeGroup
	global nextChangeTime
	global currentGroup

	if t > g.racestart:
		try:
			data = [x for x in g.telemetryData if x[-1] > t-g.racestart][0]
		except IndexError:
			raceFinish = [i for i, data in reversed(list(enumerate(g.telemetryData))) if int(data[9]) & int('111', 2) == 2][0] + 1
			data = g.telemetryData[raceFinish]
	else:
		data = g.telemetryData[0]
	'''
	Standings Data Structure
		p 0: int Race Position (sorted)
		n 1: string Name
		r 2: float Percentage of lap completed
		i 3: int Participant index
		s 4: int Current sector
		l 5: float Last sector time (-123 if none)
	   et 6: float Elapsed time
	   lx 7: int Laps completed and valid lap
	   cl 8: int Current lap
	'''
	
	standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1] if len(n.split(" ")) > 1 else n, float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]), int(data[184+i*9])) for i, n, *rest in g.participantData})

	if nextChangeTime == -1:
		nextChangeTime = t+5
	elif t > nextChangeTime:
		currentGroup = currentGroup+6 if currentGroup+6 < len(standings) else 10
		nextChangeTime = t+5

	for p, n, r, i, s, l, et, lx, cl in standings:
		if s == 1:
			#If we're in the first sector, we need to check to see if we've set a record in sector 3.
			if l != -123:
				sectorStatus[i][0] = 'current'

				if lastLapSectors[i][0] != l:
					lastLapSectors[i][0] = l

				if lx & int('10000000', 2) and r > 0:
					sectorStatus[i][1] = 'invalid'
					sectorStatus[i][2] = 'invalid'
					lastLapValid[i] = False
				elif sectorStatus[i][2] != 'invalid':
					if g.sectorBests[2] == -1 or g.sectorBests[2] >= l:
						g.sectorBests[2] = l
						g.personalBests[i][2] = l
						sectorStatus[i][2] = 'racebest'
					elif g.personalBests[i][2] == -1 or g.personalBests[i][2] >= l:
						g.personalBests[i][2] = l
						sectorStatus[i][2] = 'personalbest'
					else:
						sectorStatus[i][2] = 'none'

				#Test to see if we've just started a new lap.
				if currentLaps[i] != cl:
					g.elapsedTimes[i] += float(sum(lastLapSectors[i]))
					currentLaps[i] = cl

					#Do we have a valid last lap? If so, compare records.
					#If not, set Sector 3 to invalid (to hold it at red until
					#we get back there and reset the flag.
					if lastLapValid[i] and -1 not in lastLapSectors[i]:
						lastLapTime = float(sum(lastLapSectors[i]))
						if g.bestLap == -1 or g.bestLap > lastLapTime:
							g.bestLap = lastLapTime
							g.personalBestLaps[i] = lastLapTime
						elif g.personalBestLaps[i] == -1 or g.personalBestLaps[i] >= lastLapTime:
							g.personalBestLaps[i] = lastLapTime
					else:
						sectorStatus[i][2] = 'invalid'
						lastLapValid[i] = True

					if p == 1:
						leaderLapsCompleted = cl
						leaderET = g.elapsedTimes[i]
						lastLapSplits[i] = float(sum(lastLapSectors[i]))
					#Test to see if you're down a lap.
					elif leaderLapsCompleted > cl:
						lastLapSplits[i] = int(leaderLapsCompleted-cl)
					#Just a laggard.
					elif lx & int('01111111', 2) != 0:
						lastLapSplits[i] = float(leaderET-g.elapsedTimes[i])
		elif s == 2:
			#Sector 2 checks sector 1 records
			if l != -123:
				sectorStatus[i][1] = 'current'

				if lastLapSectors[i][1] != l:
					lastLapSectors[i][1] = l

				if lx & int('10000000', 2) and r > 0:
					sectorStatus[i][0] = 'invalid'
					sectorStatus[i][2] = 'invalid'
					lastLapValid[i] = False
				elif sectorStatus[i][0] != 'invalid':
					if g.sectorBests[0] == -1 or g.sectorBests[0] >= l:
						g.sectorBests[0] = l
						g.personalBests[i][0] = l
						sectorStatus[i][0] = 'racebest'
					elif g.personalBests[i][0] == -1 or g.personalBests[i][0] >= l:
						g.personalBests[i][0] = l
						sectorStatus[i][0] = 'personalbest'
					else:
						sectorStatus[i][0] = 'none'
		elif s == 3:
			#Sector 3 checks sector 2 records.
			if l != -123:
				sectorStatus[i][2] = 'current'

				if lastLapSectors[i][2] != l:
					lastLapSectors[i][2] = l

				if lx & int('10000000', 2) and r > 0:
					sectorStatus[i][0] = 'invalid'
					sectorStatus[i][1] = 'invalid'
					lastLapValid[i] = False
				elif sectorStatus[i][1] != 'invalid':
					if g.sectorBests[1] == -1 or g.sectorBests[1] >= l:
						g.sectorBests[1] = l
						g.personalBests[i][1] = l
						sectorStatus[i][1] = 'racebest'
					elif g.personalBests[i][1] == -1 or g.personalBests[i][1] >= l:
						g.personalBests[i][1] = l
						sectorStatus[i][1] = 'personalbest'
					else:
						sectorStatus[i][1] = 'none'

		lastLapTime = lastLapSplits[i]
	return standings
	
def make_mask(t):
	return PIL_to_npimage(make_material(t, bgOnly=True).split()[-1].convert('RGB'))
