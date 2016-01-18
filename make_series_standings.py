from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, where
import PIL.Image as plim
from PIL import ImageDraw
import sys

g = import_module(".".join(sys.argv[1][:-3].split('/')[1:]))

def series_data():
	#Find out who is lapped at the finish.
	#This is neccessary because PCARS shuffles the finish order as they cross
	#the line, not respecting laps-down.
	raceFinish = [i for i, data in reversed(list(enumerate(g.telemetryData))) if int(data[9]) & int('111', 2) == 2][0] + 1
	data = g.telemetryData[raceFinish]

	leadLapIndexes = [i for i, *rest in g.participantData if int(data[184+i*9]) >= int(data[10])]
	lappedIndexes = [i for i, *rest in g.participantData if int(data[184+i*9]) < int(data[10])]

	#Get lead lap classification, then append lapped classifications.
	data = g.telemetryData[-1]
	classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t, c, i, int(data[10])) for i, n, t, c in g.participantData if i in leadLapIndexes)
	classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t, c, i, int(data[183+i*9])) for i, n, t, c in g.participantData if i in lappedIndexes)

	#Renumber
	classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(classification, 1)]

	sectorTimes = [list() for x in range(len(classification))]
	lapTimes = [list() for x in range(len(classification))]

	for p, n, t, c, i, l in classification:
		lapFinish = raceFinish
		if p != 1:
			try:
				while (g.telemetryData[raceFinish][183+i*9] == g.telemetryData[lapFinish][183+i*9]):
					lapFinish += 1
			except IndexError:
				lapFinish = len(g.telemetryData)-1

		sectorTimes[i] = [float(g.telemetryData[x][186+i*9]) for x in where(diff([int(y[185+i*9]) & int('111', 2) for y in g.telemetryData[:lapFinish+1]]) != 0)[0].tolist() if float(g.telemetryData[x][186+i*9]) != -123.0]+[float(g.telemetryData[lapFinish][186+i*9])]
		sectorTimes[i] = sectorTimes[i][:divmod(len(sectorTimes[i]), 3)[0]*3]

		lapTimes[i] = [sum(sectorTimes[i][x:x+3]) for x in range(0, len(sectorTimes[i]), 3)]
		personalBestLaps = [sum(x) for x in lapTimes]

	columnHeadings = [("Rank", "Driver", "Team", "Car", "Series Points")]
	
	columnData = [(n, t, c, str(g.points[i]+g.pointStructure[p]+g.pointStructure[0] if min(personalBestLaps) == personalBestLaps[i] else g.points[i]+g.pointStructure[p])) for p, n, t, c, i, l in classification]
	columnData = [(str(i),)+x for i, x in enumerate(sorted(columnData, key=lambda x: int(x[3]), reverse=True), 1)]
	columnData = columnHeadings + columnData

	widths = [max([g.font.getsize(x[i])[0] for x in columnData]) for i in range(len(columnData[0]))]
	widths.append(sum(widths))

	heights = [max([g.font.getsize(x[i])[1] for x in columnData]) for i in range(len(columnData[0]))]
	dataHeight = max(heights)
	heights = [dataHeight for x in columnData]
	heights.append(g.headingfont.getsize(g.headingtext)[1])
	heights.append(g.font.getsize(g.subheadingtext)[1])

	text_width = widths[-1]+g.columnMargin*(len(widths)-1)
	text_height = sum(heights)+g.margin*len(heights)-1

	headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2
	bodyHeight = text_height-headerHeight

	topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), (255, 0, 0))
	material = plim.new('RGBA', (text_width+g.margin*2, text_height))
	material.paste(topMaterial, (0, 0))
	
	yPos = headerHeight
	for i, r in enumerate(columnData):
		if i % 2:
			materialColor = (255, 255, 255)
		else:
			materialColor = (192, 192, 192)

		dataMaterial = plim.new('RGBA', (text_width+g.margin*2, dataHeight+g.margin), materialColor)
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+g.margin

	return material, columnData, dataHeight, widths

def make_series_standings():
	material, standings, dataHeight, columnWidths = series_data()

	draw = ImageDraw.Draw(material)
	yPos = g.margin

	draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
	yPos += g.headingfont.getsize(g.headingtext)[1]

	draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
	yPos += g.font.getsize(g.headingtext)[1]+int(g.margin*1.5)

	columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]

	for r, n, t, c, pts in [list(zip(x, columnPositions)) for x in standings]:
		draw.text((r[1], yPos), str(r[0]), fill='black', font=g.font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
		draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
		draw.text((pts[1]+(columnWidths[4]-g.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=g.font)
		yPos += dataHeight+g.margin

	return PIL_to_npimage(material)

def make_series_standings_mask():
	material, *rest = series_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
