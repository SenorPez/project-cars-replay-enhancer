import binascii
import csv
import glob
from hashfile import hashfile
import hashlib
import moviepy.editor as mpy
from moviepy.video.io.bindings import PIL_to_npimage
import natsort
from numpy import diff, where
import PIL.Image as plim
from PIL import ImageFont, ImageDraw
from round_rectangle import round_rectangle
import string
import struct
import sys

robotoRegular = "/usr/share/fonts/truetype/Roboto/Roboto-Regular.ttf"
robotoMedium  = "/usr/share/fonts/truetype/Roboto/Roboto-Medium.ttf"

font = ImageFont.truetype(robotoRegular, 15)
headingfont = ImageFont.truetype(robotoMedium, 20)

racestart = 3.5

margin = 20
headingtext = "Kart One UK Nationals"
subheadingtext = "Round 1 of 3 - Glencairn East"

sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]
sectorStatus = [['current', 'none', 'none'] for x in range(64)]
lastLapSectors = [[-1, -1, -1] for x in range(64)]
lastLapElapsedTime = [-1 for x in range(64)]
totalElapsedTime = -1
lastLapTimes = ["" for x in range(64)]
leaderEt = 0
leaderLaps = 0

def process_telemetry():
	data = list()
	for a in natsort.natsorted(glob.glob(sys.argv[2]+'pdata*')):
		with open(a, 'rb') as f:
			data.append(f.read())

	telemetryData = list()

	for tele in data:
		if len(tele) == 1367:
			packString  = "HB"
			packString += "B"
			packString += "bb"
			packString += "BBbBB"
			packString += "B"
			packString += "21f"
			packString += "H"
			packString += "B"
			packString += "B"
			packString += "hHhHHBBBBBbffHHBBbB"
			packString += "22f"
			packString += "8B12f8B8f12B4h20H16f4H"
			packString += "2f"
			packString += "2B"
			packString += "bbBbbb"

			for participant in range(56):
				packString += "hhhHBBBBf"
			
			packString += "fBBB"

		elif len(tele) == 1028:
			packString  = "HBB"

			for participant in range(16):
				packString += "64s"

		elif len(tele) == 1347:
			packString  = "HB64s64s64s64s64s"

			for participant in range(16):
				packString += "64s"

		telemetryData.append(struct.unpack(packString, tele))

	with open(sys.argv[2]+'tele.csv', 'w') as f:
		for p in telemetryData:
			#f.write(",".join(string.strip(str(x), '\x00') for x in p)+"\n")
			f.write(",".join(str(x).strip('\x00') for x in p)+"\n")

def sector_rectangles(data, height):
	currentColor = (255, 255, 0)
	raceBestColor = (128, 0, 128)
	personalBestColor = (0, 128, 0)
	baseColor = (255, 255, 255)
	borderColor = (0, 0, 0)
	xPos = 0
	output = plim.new('RGB', (int(margin*1.5), height))
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

		draw.rectangle([(xPos, 0), (xPos+int(margin/2)+1, height+1)], fill=fillColor, outline=borderColor)
		xPos += int(margin/2)

	return output

def result_data():
	data = tData[-1]
	startingGridData = sorted({(int(data[182+i*9]) & int('01111111', 2), n, t, c) for (i, n), t, c in zip(pData, teamData, carData)})

	widths = [(font.getsize(str(i))[0], font.getsize(n)[0], font.getsize(t)[0], font.getsize(c)[0], sum((font.getsize(str(i))[0], font.getsize(n)[0], font.getsize(t)[0], font.getsize(c)[0]))) for i, n, t, c in startingGridData]
	widths.append((0, 0, 0, 0, headingfont.getsize(headingtext)[0]))
	widths.append((0, 0, 0, 0, font.getsize(subheadingtext)[0]))

	heights = [max(font.getsize(str(i))[1], font.getsize(n)[1], font.getsize(t)[1], font.getsize(c)[1]) for i, n, t, c in startingGridData]
	dataHeight = max(heights)
	heights = [dataHeight for x in startingGridData]
	heights.append(headingfont.getsize(headingtext)[1])
	heights.append(font.getsize(subheadingtext)[1])

	columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
	text_width = columnWidths[-1]+margin*3
	text_height = sum(heights)+margin*len(heights)-1

	headerHeight = headingfont.getsize(headingtext)[1]+font.getsize(subheadingtext)[1]+margin*2
	bodyHeight = text_height-headerHeight

	topMaterial = round_rectangle((text_width+margin*2, headerHeight), 0, (255, 0, 0), [1, 1, 0, 0])

	material = plim.new('RGBA', (text_width+margin*2, text_height))
	material.paste(topMaterial, (0, 0))
	
	yPos = headerHeight
	for i, r in enumerate(startingGridData[0:-1]):
		if i % 2:
			materialColor = (255, 255, 255)
		else:
			materialColor = (192, 192, 192)

		dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 0, 0])
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+margin

	i += 1
	if i % 2:
		materialColor = (255, 255, 255)
	else:
		materialColor = (192, 192, 192)
	dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 1, 1])
	material.paste(dataMaterial, (0, yPos))
	
	return material, startingGridData, dataHeight, columnWidths

def make_result(t):
	material, startingGridData, dataHeight, columnWidths = result_data()

	draw = ImageDraw.Draw(material)

	yPos = margin

	draw.text((20, yPos), headingtext, fill='white', font=headingfont)
	yPos += headingfont.getsize(headingtext)[1]

	draw.text((20, yPos), subheadingtext, fill='white', font=font)
	yPos += font.getsize(headingtext)[1]+margin
	yPos += margin/2

	columnPositions = [margin*(i+1)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]

	for i, n, t, c in [list(zip(x, columnPositions)) for x in startingGridData]:
		draw.text((i[1], yPos), str(i[0]), fill='black', font=font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=font)
		draw.text((t[1], yPos), str(t[0]), fill='black', font=font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=font)
		yPos += dataHeight+margin

	return PIL_to_npimage(material.convert('RGB'))
	
def make_result_mask(t):
	material, _, _, _ = title_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))

def title_data():
	data = tData[0]
	startingGridData = sorted({(int(data[182+i*9]) & int('01111111', 2), n, t, c) for (i, n), t, c in zip(pData, teamData, carData)})

	widths = [(font.getsize(str(i))[0], font.getsize(n)[0], font.getsize(t)[0], font.getsize(c)[0], sum((font.getsize(str(i))[0], font.getsize(n)[0], font.getsize(t)[0], font.getsize(c)[0]))) for i, n, t, c in startingGridData]
	widths.append((0, 0, 0, 0, headingfont.getsize(headingtext)[0]))
	widths.append((0, 0, 0, 0, font.getsize(subheadingtext)[0]))

	heights = [max(font.getsize(str(i))[1], font.getsize(n)[1], font.getsize(t)[1], font.getsize(c)[1]) for i, n, t, c in startingGridData]
	dataHeight = max(heights)
	heights = [dataHeight for x in startingGridData]
	heights.append(headingfont.getsize(headingtext)[1])
	heights.append(font.getsize(subheadingtext)[1])

	columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
	text_width = columnWidths[-1]+margin*3
	text_height = sum(heights)+margin*len(heights)-1

	headerHeight = headingfont.getsize(headingtext)[1]+font.getsize(subheadingtext)[1]+margin*2
	bodyHeight = text_height-headerHeight

	topMaterial = round_rectangle((text_width+margin*2, headerHeight), 0, (255, 0, 0), [1, 1, 0, 0])

	material = plim.new('RGBA', (text_width+margin*2, text_height))
	material.paste(topMaterial, (0, 0))
	
	yPos = headerHeight
	for i, r in enumerate(startingGridData[0:-1]):
		if i % 2:
			materialColor = (255, 255, 255)
		else:
			materialColor = (192, 192, 192)

		dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 0, 0])
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+margin

	i += 1
	if i % 2:
		materialColor = (255, 255, 255)
	else:
		materialColor = (192, 192, 192)
	dataMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, materialColor, [0, 0, 1, 1])
	material.paste(dataMaterial, (0, yPos))
	
	return material, startingGridData, dataHeight, columnWidths

def make_title(t):
	material, startingGridData, dataHeight, columnWidths = title_data()

	draw = ImageDraw.Draw(material)

	yPos = margin

	draw.text((20, yPos), headingtext, fill='white', font=headingfont)
	yPos += headingfont.getsize(headingtext)[1]

	draw.text((20, yPos), subheadingtext, fill='white', font=font)
	yPos += font.getsize(headingtext)[1]+margin
	yPos += margin/2

	columnPositions = [margin*(i+1)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]

	for i, n, t, c in [list(zip(x, columnPositions)) for x in startingGridData]:
		draw.text((i[1], yPos), str(i[0]), fill='black', font=font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=font)
		draw.text((t[1], yPos), str(t[0]), fill='black', font=font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=font)
		yPos += dataHeight+margin

	return PIL_to_npimage(material.convert('RGB'))
	
def make_title_mask(t):
	material, _, _, _ = title_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))

def standings_data(t):
	if t >= racestart:
		try:
			data = [x for x in tData if x[-1] > t-racestart][0]
		except IndexError:
			data = tData[-1]
	else:
		data = tData[0]

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

	standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1], float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]) & int('0111', 2)) for (i, n) in pData})

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
	global lastLapTimes
	global leaderEt
	global leaderLaps
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

			material.paste(sector_rectangles(sectorStatus[i], dataHeight), (ss[1], int(yPos)))

			if lastLapTimes[i] == "":
				lastLapTime = "--.--"
			else:
				lastLapTime = "{:.2f}".format(lastLapTimes[i])
			draw.text((ll[1], yPos), str(lastLapTime), fill='black', font=font)

			draw.line([(margin, yPos+dataHeight), (margin+lineLength*r[0], yPos+dataHeight)], fill=(255, 0, 0), width=2)
			draw.line([(margin+lineLength*r[0], yPos+dataHeight), (materialWidth-margin, yPos+dataHeight)], fill=(255, 192, 192), width=2)
			draw.ellipse([(margin+lineLength*r[0]-2, yPos+dataHeight-2), (margin+lineLength*r[0]+2, yPos+dataHeight+2)], fill=(255, 0, 0))

		yPos += dataHeight+margin

	return PIL_to_npimage(material.convert('RGB'))
	
def make_standings_mask(t):
	material, _, _, _ = standings_data(t)
	return PIL_to_npimage(material.split()[-1].convert('RGB'))

def progress_data(t):
	if t >= racestart:
		try:
			time = "{:.2f}".format(float([x for x in tData if x[-1] > t-racestart][0][13]))
			data = [x for x in tData if x[-1] > t-racestart][0]
		except IndexError:
			time = "{:.2f}".format(float(tData[-1][13]))
			data = tData[-1]

		currentLap = min((int(data[10]), max([int(data[184+i*9]) for (i, n) in pData])))
		lap = "{}/{}".format(currentLap, data[10])

	else:
		time = "{:.2f}".format(float(0))
		data = tData[0]
		lap = "{}/{}".format(1, data[10])

	text_width = max((font.getsize(time)[0], font.getsize(lap)[0]))+margin
	dataHeight = max((font.getsize(time)[1], font.getsize(lap)[1]))
	text_height = sum((font.getsize(time)[1], font.getsize(lap)[1], margin))

	material = plim.new('RGBA', (text_width+margin*2, text_height+margin*2))

	topMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, (255, 255, 255, 128), [0, 0, 0, 0])
	material.paste(topMaterial, (0, 0))
	bottomMaterial = round_rectangle((text_width+margin*2, dataHeight+margin), 0, (192, 192, 192, 128), [0, 0, 0, 0])
	material.paste(bottomMaterial, (0, dataHeight+margin))

	draw = ImageDraw.Draw(material)
	draw.text((margin, int(margin/2)), time, fill='black', font=font)
	draw.text((margin, dataHeight+int(margin*1.5)), lap, fill='black', font=font)

	return material

def make_timer(t):
	return PIL_to_npimage(progress_data(t).convert('RGB'))

def make_timer_mask(t):
	return PIL_to_npimage(progress_data(t).split()[-1].convert('RGB'))

def make_lap(t):
	if t >= racestart:
		try:
			data = [x for x in tData if x[-1] > t-racestart][0]
		except IndexError:
			data = tData[-1]
		standings = sorted({(int(data[182+i*9]), n, int(data[184+i*9]), i) for (i, n) in pData})
		if int(max(standings, key=lambda x: x[2])[2]) > int(data[10]):
			lap = "{}/{}".format(data[10], data[10])
		else:
			lap = "{}/{}".format(max(standings, key=lambda x: x[2])[2], data[10])
	else:
		data = tData[0]
		lap = "{}/{}".format(1, data[10])

	material = plim.new('RGB', (200, 200), 'white')
	text_width, text_height = font.getsize(lap)
	material = material.resize((int(text_width*1.1), int(text_height*1.1)))
	material_width, material_height = material.size
	draw = ImageDraw.Draw(material)
	draw.text((int(material_width*0.05), int(material_height*0.05)), lap, fill='black', font=font)
	return PIL_to_npimage(material)

if len(sys.argv) != 3:
	print ("Usage: 'python'"+sys.argv[0]+" <video> <packetdirectory>'")

else:
	try:
		try:
			f = open(sys.argv[2]+'tele.csv', 'r')
		except FileNotFoundError:
			process_telemetry()
			f = open(sys.argv[2]+'tele.csv', 'r')
		finally:
			csvdata = csv.reader(f)

		global tData
		global pData
		
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

		#Because I'm a dirty savescummer, we need to find the last race, since
		#the earlier ones are savescum scum. Save.
		raceStart = -1
		raceEnd = -1

		for i, data in reversed(list(enumerate(tData))):
			if (int(data[9]) & int('111', 2) == 3) and (raceEnd == -1):
				raceEnd = i+1
			
			if (int(data[9]) & int('111', 2) == 0) and (raceEnd != -1) and (raceStart == -1):
				raceStart = i+1

		if raceStart == -1 or raceEnd == -1:
			raise ValueError("valueError: Couldn't detect raceStart and raceEnd you savescumming scum.")
			#raceStart = 0
			#raceEnd = -1

		tData = tData[raceStart:raceEnd]
		lastTime = 0
		addTime = 0
		for i, data in enumerate(tData):
			if float(data[13]) == -1:
				tData[i] = data+[-1]
			else:
				if float(data[13]) < lastTime:
					addTime = lastTime + addTime
				tData[i] = data+[float(data[13])+addTime]
				lastTime = float(data[13])
		
		global teamData
		global carData
		teamData = ["Dark Nitro" for x in range(len(pData))]
		carData = ["125cc Shifter Kart" for x in range(len(pData))]

		#Create black frame to detect fade in and fade out.
		video = mpy.VideoFileClip(sys.argv[1])

		#Test file hash, because blackframe detection is slow, so we cache it.
		#Get stored file.
		videostart = -1
		videoend = -1
		try:
			with open("file.cache", 'r') as h:
				cache = csv.reader(h)

				for row in cache:
					if row[0] == sys.argv[1] and row[1] == hashfile(open(sys.argv[1], 'rb'), hashlib.sha256()):
						videostart, videoend = float(row[2]), float(row[3])

		except FileNotFoundError:
			pass

		#Nothing found in the cache, so detect and add to cache.
		if videostart == -1 or videoend == -1:
			blackframe = mpy.ColorClip(video.size, duration=video.duration).set_fps(video.fps).get_frame(0).astype("uint8")
			
			try:
				threshold = 1
				skipstart = 0
				skipend = 0
				gaptime = 1

				blackframes = [t for (t, f) in video.iter_frames(with_times=True) if f.mean() < threshold]
				videostart = blackframes[where(diff(blackframes)>gaptime)[0][0+skipstart]]
				videoend = blackframes[::-1][where(diff(blackframes[::-1])<-gaptime)[0][0+skipend]]
			except IndexError:
				videostart = 0
				videoend = video.duration

			with open("file.cache", 'w') as h:
				cache = csv.writer(h)
				cache.writerow([sys.argv[1], hashfile(open(sys.argv[1], 'rb'), hashlib.sha256()), videostart, videoend])

		video = mpy.VideoFileClip(sys.argv[1]).subclip(videostart, videoend)
		video_width, video_height = video.size
		video = video.fx(mpy.vfx.freeze, t='end', freeze_duration=20)
		video = video.set_start(5).crossfadein(1)

		timer = mpy.VideoClip(make_timer)
		timer_mask = mpy.VideoClip(make_timer_mask).to_mask(1)
		timer_width, timer_height = timer.size
		timer = timer.set_position((video_width-timer_width-margin, margin)).set_duration(video.duration-20).crossfadeout(1)
		timer = timer.set_mask(timer_mask)
		timer = timer.set_start(5)

		#
		#lapcounter = mpy.VideoClip(make_lap)
		#lap_width, lap_height = lapcounter.size
		#lapcounter = lapcounter.set_position(('center', 10)).set_duration(video.duration)

		standing = mpy.VideoClip(make_standings)
		standing_mask = mpy.VideoClip(make_standings_mask).to_mask(1)
		standing = standing.set_position((margin, margin)).set_duration(video.duration-20).crossfadeout(1)
		standing = standing.set_mask(standing_mask)
		standing = standing.set_start(5)

		title = mpy.VideoClip(make_title)
		title_mask = mpy.VideoClip(make_title_mask).to_mask(1)
		title = title.set_position(('center', 'center')).set_duration(5).crossfadeout(1)
		title = title.set_mask(title_mask)

		result = mpy.VideoClip(make_result)
		result_mask = mpy.VideoClip(make_result_mask).to_mask(1)
		result = result.set_start(video.duration-15)
		result = result.set_position(('center', 'center')).set_duration(20).crossfadein(1)

		output = mpy.CompositeVideoClip([video,
										 timer,
										 standing,
										 title,
										 result])
		#output.subclip(0, 40).write_videofile("edit.mp4", fps=10)
		#output.write_videofile("edit.mp4", fps=10)
		output.write_videofile("edit.mp4")
		#output.save_frame("edit.jpg", 10)
		#for frame in range(40):
			#output.save_frame("edit.jpg", frame)

	except ValueError as e:
		print >> sys.stderr, e.message

	except IOError as e:
		print >> sys.stderr, "IOError: {}".format(e)
