from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, where
import PIL.Image as plim
from PIL import ImageDraw
from round_rectangle import round_rectangle
import sys

g = import_module(sys.argv[1][:-3])

sectorStatus = [['current', 'none', 'none'] for x in range(64)]
sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]
lastLapSectors = [[-1, -1, -1] for x in range(64)]
lastLapTimes = [-1 for x in range(64)]

elapsedTimes = [-1 for x in range(64)]

currentLaps = [1 for x in range(64)]
lastLapSplits = [-1 for x in range(64)]
leaderET = -1
leaderLapsCompleted = 0

maxLapTime = -1

def sector_rectangles(data, height):
	invalidColor = (255, 0, 0)
	currentColor = (255, 255, 0)
	raceBestColor = (128, 0, 128)
	personalBestColor = (0, 128, 0)
	baseColor = (255, 255, 255)
	borderColor = (0, 0, 0)
	xPos = 0

	margin = g.margin

	output = plim.new('RGB', (int(margin*1.5)+4, height))
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

		draw.rectangle([(xPos, 0), (xPos+int(margin/2)+1, height-1)], fill=fillColor, outline=borderColor)
		xPos += int(margin/2)+1

	return output

def standings_data(t):
	telemetryData = g.telemetryData
	participantData = g.participantData

	font = g.font
	margin = g.margin

	racestart = g.racestart

	if t >= racestart:
		try:
			data = [x for x in telemetryData if x[-1] > t-racestart][0]
		except IndexError:
			data = telemetryData[-1]
	else:
		data = telemetryData[0]

	'''
	Standings Data Structure
		p 0: int Race Position (sorted)
		n 1: string Name
		r 2: float Percentage of lap completed
		i 3: int Participant index
		s 4: int Current sector
		l 5: float Last sector time (-123 if none)
	   et 6: float Last lap time (leader), split time (trailers)
	   lc 7: int Laps completed and valid lap
	   cl 8: int Current lap
	'''

	standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1], float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]), int(data[184+i*9])) for i, n, *rest in participantData})

	global maxLapTime
	if maxLapTime == -1:
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

	widths = [(font.getsize(str(p))[0], font.getsize(str(n))[0], int(margin*1.5), max([font.getsize(str(sizeString))[0], font.getsize("+00 laps")[0]])) for p, n, *rest in standings]
	heights = [max(font.getsize(str(p))[1], font.getsize(str(n))[1], font.getsize(str("{:.2f}".format(0.00)))[1]) for p, n, *rest in standings]
	dataHeight = max(heights)
	heights = [dataHeight for x in standings]

	columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
	text_width = sum(columnWidths)+g.columnMargin*(len(widths[0])-1)
	text_height = sum(heights)+margin*(len(heights)-1)

	material = plim.new('RGBA', (text_width+margin*2, text_height+margin))

	dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, (255, 255, 255, 128), [1, 1, 0, 0])
	material.paste(dataMaterial, (0, 0))
	
	yPos = dataHeight+margin
	for i, r in enumerate(standings[1:-1]):
		if i % 2:
			materialColor = (255, 255, 255, 128)
		else:
			materialColor = (192, 192, 192, 128)

		dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 0, 0])
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+margin

	i += 1
	if i % 2:
		materialColor = (255, 255, 255, 128)
	else:
		materialColor = (192, 192, 192, 128)
	dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 1, 1])
	material.paste(dataMaterial, (0, yPos))
	
	return material, standings, dataHeight, columnWidths

def make_standings(t):
	margin = g.margin
	font = g.font

	global leaderLapsCompleted
	global leaderET

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
	material, standings, dataHeight, columnWidths = standings_data(t)
	materialWidth = material.size[0]
	lineLength = materialWidth-margin*2

	draw = ImageDraw.Draw(material)

	columnPositions = [margin*(i+1)+sum(columnWidths[0:i]) if i == 0 else margin+g.columnMargin*(i)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]
	yPos = margin/2

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
				else:
					if sectorBests[2] == -1 or sectorBests[2] >= l:
						sectorBests[2] = l
						personalBests[i][2] = l
						sectorStatus[i][2] = 'racebest'
					elif personalBests[i][2] == -1 or personalBests[i][2] >= l:
						personalBests[i][2] = l
						sectorStatus[i][2] = 'personalbest'
					else:
						sectorStatus[i][2] = 'none'

				#Test to see if we've just started a new lap.
				if currentLaps[i] != cl:
					elapsedTimes[i] += float(sum(lastLapSectors[i]))
					currentLaps[i] = cl

					if p == 1:
						leaderLapsCompleted = cl
						leaderET = elapsedTimes[i]
						lastLapSplits[i] = float(sum(lastLapSectors[i]))
					#Test to see if you're down a lap.
					elif leaderLapsCompleted > cl:
						lastLapSplits[i] = int(leaderLapsCompleted-cl)
					#Just a laggard.
					elif lx & int('01111111', 2) != 0:
						lastLapSplits[i] = float(leaderET-elapsedTimes[i])
		elif s == 2:
			#Sector 2 checks sector 1 records
			if l != -123:
				sectorStatus[i][1] = 'current'

				if lastLapSectors[i][1] != l:
					lastLapSectors[i][1] = l

				if lx & int('10000000', 2) and r > 0:
					sectorStatus[i][0] = 'invalid'
					sectorStatus[i][2] = 'invalid'
				else:
					if sectorBests[0] == -1 or sectorBests[0] >= l:
						sectorBests[0] = l
						personalBests[i][0] = l
						sectorStatus[i][0] = 'racebest'
					elif personalBests[i][0] == -1 or personalBests[i][0] >= l:
						personalBests[i][0] = l
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
				else:
					if sectorBests[1] == -1 or sectorBests[1] >= l:
						sectorBests[1] = l
						personalBests[i][1] = l
						sectorStatus[i][1] = 'racebest'
					elif personalBests[i][1] == -1 or personalBests[i][1] >= l:
						personalBests[i][1] = l
						sectorStatus[i][1] = 'personalbest'
					else:
						sectorStatus[i][1] = 'none'

		for pp, nn, ss, ll, rr in [list(zip((p, n, s, l, r), columnPositions+[0]))]:
			draw.text((pp[1], yPos), str(pp[0]), fill='black', font=font)
			draw.text((nn[1], yPos), str(nn[0]), fill='black', font=font)

			lastLapTime = lastLapSplits[i]

			if isinstance(lastLapSplits[i], int) and lastLapSplits[i] < 0:
				lastLapTime = "{}".format('')
				timeWidth = 0
			elif isinstance(lastLapSplits[i], int):
				suffix = " laps" if lastLapSplits[i] > 1 else " lap"
				lastLapTime = "{:+d}".format(lastLapSplits[i])+suffix
				timeWidth = font.getsize(lastLapTime)[0]
			elif isinstance(lastLapSplits[i], float) and lastLapSplits[i] > 0:
				lastLapTime = "{:.2f}".format(lastLapSplits[i])
				timeWidth = font.getsize(lastLapTime)[0]
			elif isinstance(lastLapSplits[i], float):
				lastLapTime = "{:+.2f}".format(lastLapSplits[i]*-1)
				timeWidth = font.getsize(lastLapTime)[0]

			tPos = int(materialWidth-margin-timeWidth)

			draw.text((tPos, yPos), str(lastLapTime), fill='black', font=font)

			draw.line([(margin, yPos+dataHeight), (margin+lineLength*rr[0], yPos+dataHeight)], fill=(255, 0, 0), width=2)
			draw.line([(margin+lineLength*rr[0], yPos+dataHeight), (materialWidth-margin, yPos+dataHeight)], fill=(255, 192, 192), width=2)

			material.paste(sector_rectangles(sectorStatus[i], dataHeight), (ss[1]-2, int(yPos)))

			draw.ellipse([(margin+lineLength*rr[0]-2, yPos+dataHeight-2), (margin+lineLength*rr[0]+2, yPos+dataHeight+2)], fill=(255, 0, 0))

		yPos += dataHeight+margin

	return PIL_to_npimage(material.convert('RGB'))
	
def make_standings_mask(t):
	material, *rest = standings_data(t)
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
