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

def makeET(rawET):
	maxMinutes, maxSeconds = divmod(rawET, 60)
	maxHours, maxMinutes = divmod(maxMinutes, 60)

	if maxHours > 0:
		return "{:d}:{:02d}:{:05.2f}".format(int(maxHours), int(maxMinutes), float(maxSeconds))
	elif maxMinutes > 0:
		return "{:d}:{:05.2f}".format(int(maxMinutes), float(maxSeconds))
	else:
		return "{:.2f}".format(float(maxSeconds))

def results_data():
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

	sectorBests = [[-1, -1, -1] for x in range(len(classification))]
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

		sectorBests[i][0] = min([float(x[186+i*9]) for x in g.telemetryData if int(x[185+i*9]) & int('111', 2) == 2 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
		sectorBests[i][1] = min([float(x[186+i*9]) for x in g.telemetryData if int(x[185+i*9]) & int('111', 2) == 3 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
		sectorBests[i][2] = min([float(x[186+i*9]) for x in g.telemetryData if int(x[185+i*9]) & int('111', 2) == 1 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])

	columnHeadings = [("Pos.", "Driver", "Team", "Car", "Laps", "Time", "Best Lap", "Best S1", "Best S2", "Best S3", "Points")]
	
	if len(g.pointStructure) < 17:
		g.pointStructure += [0] * (17-len(g.pointStructure))

	columnData = [(str(p), n, t, c, str(l), makeET(sum(lapTimes[i])), "{:.2f}".format(float(min(lapTimes[i]))), "{:.2f}".format(float(sectorBests[i][0])), "{:.2f}".format(float(sectorBests[i][1])), "{:.2f}".format(float(sectorBests[i][2])), str(g.pointStructure[p]+g.pointStructure[0] if min([x for x in personalBestLaps if isinstance(x, float)]) == personalBestLaps[i] else g.pointStructure[p])) for p, n, t, c, i, l in classification[:16]]
	columnHeadings = [tuple([x if len([y[i] for y in columnData if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
	columnData = columnHeadings+columnData

	widths = [max([g.font.getsize(x[i])[0] for x in columnData]) for i in range(len(columnData[0]))]
	widths.append(sum(widths))

	heights = [max([g.font.getsize(x[i])[1] for x in columnData]) for i in range(len(columnData[0]))]
	dataHeight = max(heights)
	heights = [dataHeight for x in columnData]
	heights.append(g.headingfont.getsize(g.headingtext)[1])
	heights.append(g.font.getsize(g.subheadingtext)[1])

	text_width = widths[-1]+g.columnMargin*(len([x for x in widths[:-1] if x != 0])-1)
	text_height = sum(heights)+g.margin*len(heights)-1

	headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2

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

def make_results():
	material, classification, dataHeight, columnWidths = results_data()

	draw = ImageDraw.Draw(material)

	yPos = g.margin

	draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
	yPos += g.headingfont.getsize(g.headingtext)[1]

	draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
	yPos += g.font.getsize(g.subheadingtext)[1]+g.margin
	yPos += g.margin/2

	columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(columnWidths[0:i]) if columnWidths[i-1] != 0 else g.margin+g.columnMargin*(i-1)+sum(columnWidths[0:(i-1)]) for i, w in enumerate(columnWidths)]

	for p, n, t, c, l, et, bl, bs1, bs2, bs3, pts in [list(zip(x, columnPositions)) for x in classification]:
		draw.text((p[1], yPos), str(p[0]), fill='black', font=g.font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
		if t != "":
			draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
		draw.text((l[1]+(columnWidths[4]-g.font.getsize(str(l[0]))[0])/2, yPos), str(l[0]), fill='black', font=g.font)
		draw.text((et[1]+(columnWidths[5]-g.font.getsize(str(et[0]))[0])/2, yPos), str(et[0]), fill='black', font=g.font)
		draw.text((bl[1]+(columnWidths[6]-g.font.getsize(str(bl[0]))[0])/2, yPos), str(bl[0]), fill='black', font=g.font)
		draw.text((bs1[1]+(columnWidths[7]-g.font.getsize(str(bs1[0]))[0])/2, yPos), str(bs1[0]), fill='black', font=g.font)
		draw.text((bs2[1]+(columnWidths[8]-g.font.getsize(str(bs2[0]))[0])/2, yPos), str(bs2[0]), fill='black', font=g.font)
		draw.text((bs3[1]+(columnWidths[9]-g.font.getsize(str(bs3[0]))[0])/2, yPos), str(bs3[0]), fill='black', font=g.font)
		draw.text((pts[1]+(columnWidths[10]-g.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=g.font)
		yPos += dataHeight+g.margin

	return PIL_to_npimage(material)
	
def make_results_mask():
	material, *rest = results_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
