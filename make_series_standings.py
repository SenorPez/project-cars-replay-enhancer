from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, where
import os.path
import PIL.Image as plim
from PIL import ImageDraw
import sys

paths = os.path.split(os.path.abspath(sys.argv[1]))
sys.path.insert(0, paths[0])
g = import_module(os.path.splitext(paths[1])[0])

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
	classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in g.participantData if i in leadLapIndexes)
	classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in g.participantData if i in lappedIndexes)

	#Renumber
	classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(classification, 1)]

	sectorTimes = [list() for x in range(len(classification))]
	lapTimes = [list() for x in range(len(classification))]
	personalBestLaps = ['' for x in range(len(classification))]

	for p, n, t, c, i, l in classification[:16]:
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
		personalBestLaps[i] = min([x for x in lapTimes[i]])

	columnHeadings = [("Rank", "Driver", "Team", "Car", "Series Points")]
	
	if len(g.pointStructure) < 17:
		g.pointStructure += [0] * (17-len(g.pointStructure))

	if len(g.points) < 17:
		g.points += [0] * (17-len(g.points))

	columnData = [(n, t, c, str(g.points[i]+g.pointStructure[p]+g.pointStructure[0] if min([x for x in personalBestLaps if isinstance(x, float)]) == personalBestLaps[i] else g.points[i]+g.pointStructure[p])) for p, n, t, c, i, l in classification[:16]]
	columnData = sorted(columnData, key=lambda x: (-int(x[3]), str(x[0]).split(" ")[-1]))
	for i, x in enumerate(columnData):
		if i == 0:
			columnData[i] = (str(1),)+x
		elif columnData[i][-1] == columnData[i-1][-1]:
			columnData[i] = (str(columnData[i-1][0]),)+x
		else:
			columnData[i] = (str(i+1),)+x

	columnHeadings = [tuple([x if len([y[i] for y in columnData if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
	columnData = columnHeadings + columnData

	widths = [max([g.font.getsize(x[i])[0] for x in columnData]) for i in range(len(columnData[0]))]
	widths.append(sum(widths))

	heights = [max([g.font.getsize(x[i])[1] for x in columnData]) for i in range(len(columnData[0]))]
	dataHeight = max(heights)
	heights = [dataHeight for x in columnData]
	heights.append(g.headingfont.getsize(g.headingtext)[1])
	heights.append(g.font.getsize(g.subheadingtext)[1])

	headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2

	text_width = max(widths[-1]+g.columnMargin*(len([x for x in widths[:-1] if x != 0])-1), g.headingfont.getsize(g.headingtext)[0]+g.columnMargin+headerHeight, g.font.getsize(g.subheadingtext)[0]+g.columnMargin+headerHeight)
	text_height = sum(heights)+g.margin*len(heights)-1

	topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), g.headingcolor)
	serieslogo = plim.open(g.serieslogo).resize((topMaterial.height, topMaterial.height))
	topMaterial.paste(serieslogo, (topMaterial.width-serieslogo.width, 0))

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
	yPos += g.font.getsize(g.subheadingtext)[1]+int(g.margin*1.5)

	columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(columnWidths[0:i]) if columnWidths[i-1] != 0 else g.margin+g.columnMargin*(i-1)+sum(columnWidths[0:(i-1)]) for i, w in enumerate(columnWidths)]

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

def make_champion():
	_, standings, *rest = series_data()

	heading_width = g.headingfont.getsize(g.headingtext)[0]+g.margin*2
	text_width = max([max([g.headingfont.getsize(n)[0] if r == '1' else g.font.getsize(n)[0], g.font.getsize(t)[0]+g.columnMargin, g.font.getsize(c)[0]+g.columnMargin]) for r, n, t, c, *rest in standings[1:4]]+[g.headingfont.getsize("Champion")[0]]+[g.font.getsize("Runner Up")[0]])+g.margin*2

	heading_height = g.headingfont.getsize(g.headingtext)[1]+g.margin*2
	text_height = max([300, sum([g.headingfont.getsize(n)[1]+g.font.getsize(t)[1]+g.font.getsize(c)[1] if r == '1' else g.font.getsize(n)[1]+g.font.getsize(t)[1]+g.font.getsize(c)[1] for r, n, t, c, *rest in standings[1:4]]+[g.headingfont.getsize("Champion")[1]]+[g.font.getsize("Runner Up")[1]*2])+g.margin*4])

	width = max((heading_width, 300+text_width))
	height = heading_height+text_height

	topMaterial = plim.new('RGBA', (width, heading_height), g.headingcolor)
	seriesLogo = plim.open(g.serieslogo).resize((300, 300))

	material = plim.new('RGBA', (width, height), (255, 255, 255))
	material.paste(topMaterial, (0, 0))
	material.paste(seriesLogo, (0, heading_height))

	draw = ImageDraw.Draw(material)

	draw.text((g.margin, g.margin), g.headingtext, fill='white', font=g.headingfont)

	xPos = 300+g.margin
	yPos = heading_height+g.margin

	for r, n, t, c, *rest in standings[1:4]:
		if r == '1':
			draw.text((xPos, yPos), "Champion", fill='black', font=g.headingfont)
			yPos += g.headingfont.getsize("Champion")[1]
			draw.text((xPos, yPos), n, fill='black', font=g.headingfont)
			yPos += g.headingfont.getsize(n)[1]
		else:
			draw.text((xPos, yPos), "Runner Up", fill='black', font=g.font)
			yPos += g.font.getsize("Runner Up")[1]
			draw.text((xPos, yPos), n, fill='black', font=g.font)
			yPos += g.font.getsize(n)[1]
		draw.text((xPos+g.columnMargin, yPos), t, fill='black', font=g.font)
		yPos += g.font.getsize(t)[1]
		draw.text((xPos+g.columnMargin, yPos), c, fill='black', font=g.font)
		yPos += g.font.getsize(c)[1]+g.margin

	return PIL_to_npimage(material)
