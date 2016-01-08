from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
from PIL import ImageDraw
from round_rectangle import round_rectangle

import replay_globals as g

sectorStatus = [['current', 'none', 'none'] for x in range(64)]
sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]
lastLapSectors = [[-1, -1, -1] for x in range(64)]
lastLapTimes = [-1 for x in range(64)]

def sector_rectangles(data, height):
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
		if sector == 'current':
			fillColor = currentColor
		elif sector == 'racebest':
			fillColor = raceBestColor
		elif sector == 'personalbest':
			fillColor = personalBestColor
		elif sector == 'none':
			fillColor = baseColor
		else:
			fillColor = (255, 0, 0)

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
	   et 6: float Elapsed time
	   lc 7: int Laps completed
	'''

	standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1], float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]) & int('0111', 2)) for (i, n) in participantData})

	widths = [(font.getsize(str(p))[0], font.getsize(str(n))[0], int(margin*1.5), font.getsize(str("{:.2f}".format(0.00)))[0]) for p, n, _, _, _, _, _, _ in standings]
	heights = [max(font.getsize(str(p))[1], font.getsize(str(n))[1], font.getsize(str("{:.2f}".format(0.00)))[1]) for p, n, _, _, _, _, _, _ in standings]
	dataHeight = max(heights)
	heights = [dataHeight for x in standings]

	columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
	text_width = sum(columnWidths)+margin*(len(widths[0])-1)
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

	'''
	Standings Data Structure
		p 0: int Race Position (sorted)
		n 1: string Name
		r 2: float Percentage of lap completed
		i 3: int Participant index
		s 4: int Current sector
		l 5: float Last sector time (-123 if none)
	   et 6: float Elapsed time
	   lc 7: int Laps completed
	'''
	material, standings, dataHeight, columnWidths = standings_data(t)
	materialWidth = material.size[0]
	lineLength = materialWidth-margin*2

	draw = ImageDraw.Draw(material)

	columnPositions = [margin*(i+1)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]
	yPos = margin/2

	for p, n, r, i, s, l, et, lc in standings:
		if s == 1:
			#If we're in the first sector, we need to check to see if we've set a record in sector 3.
			#sectorStatus[i][1] = 'none'

			if l != -123:
				sectorStatus[i][0] = 'current'

				if lastLapSectors[i][0] != l:
					lastLapSectors[i][0] = l

				if sectorBests[2] == -1 or sectorBests[2] >= l:
					sectorBests[2] = l
					personalBests[i][2] = l
					sectorStatus[i][2] = 'racebest'
				elif personalBests[i][2] == -1 or personalBests[i][2] >= l:
					personalBests[i][2] = l
					sectorStatus[i][2] = 'personalbest'
				else:
					sectorStatus[i][2] = 'none'

				#While we're here, let's get the last lap time.
				lastLapTimes[i] = sum(lastLapSectors[i])
		elif s == 2:
			#Secotr 2 checks sector 1 records
			#sectorStatus[i][2] = 'none'

			if l != -123:
				sectorStatus[i][1] = 'current'

				if lastLapSectors[i][1] != l:
					lastLapSectors[i][1] = l

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
			#sectorStatus[i][0] = 'none'

			if l != -123:
				sectorStatus[i][2] = 'current'

				if lastLapSectors[i][2] != l:
					lastLapSectors[i][2] = l

				if sectorBests[1] == -1 or sectorBests[1] >= l:
					sectorBests[1] = l
					personalBests[i][1] = l
					sectorStatus[i][1] = 'racebest'
				elif personalBests[i][1] == -1 or personalBests[i][1] >= l:
					personalBests[i][1] = l
					sectorStatus[i][1] = 'personalbest'
				else:
					sectorStatus[i][1] = 'none'


		for p, n, ss, ll, r in [list(zip((p, n, s, l, r), columnPositions+[0]))]:
			draw.text((p[1], yPos), str(p[0]), fill='black', font=font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=font)

			if lastLapTimes[i] == -1:
				lastLapTime = "--.--"
			else:
				lastLapTime = "{:.2f}".format(lastLapTimes[i])
			draw.text((ll[1], yPos), str(lastLapTime), fill='black', font=font)

			draw.line([(margin, yPos+dataHeight), (margin+lineLength*r[0], yPos+dataHeight)], fill=(255, 0, 0), width=2)
			draw.line([(margin+lineLength*r[0], yPos+dataHeight), (materialWidth-margin, yPos+dataHeight)], fill=(255, 192, 192), width=2)

			material.paste(sector_rectangles(sectorStatus[i], dataHeight), (ss[1]-2, int(yPos)))

			draw.ellipse([(margin+lineLength*r[0]-2, yPos+dataHeight-2), (margin+lineLength*r[0]+2, yPos+dataHeight+2)], fill=(255, 0, 0))

		yPos += dataHeight+margin

	return PIL_to_npimage(material.convert('RGB'))
	
def make_standings_mask(t):
	material, _, _, _ = standings_data(t)
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
