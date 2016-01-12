from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
from PIL import ImageDraw
from round_rectangle import round_rectangle
import sys

g = import_module(sys.argv[1][:-3])

def timer_data(t):
	racestart = g.racestart
	telemetryData = g.telemetryData
	participantData = g.participantData

	font = g.font
	margin = g.margin

	if t >= racestart:
		try:
			time = "{:.2f}".format(float([x for x in telemetryData if x[-1] > t-racestart][0][13]))
			data = [x for x in telemetryData if x[-1] > t-racestart][0]
		except IndexError:
			time = "{:.2f}".format(float(telemetryData[-1][13]))
			data = telemetryData[-1]

		#currentLap = min((int(data[10]), max([int(data[184+i*9]) for (i, n) in participantData])))
		currentLap = min((int(data[10]), max([int(data[184+i*9]) for i, _, _, _ in g.participantData])))
		lap = "{}/{}".format(currentLap, data[10])

	else:
		time = "{:.2f}".format(float(0))
		data = telemetryData[0]
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
	return PIL_to_npimage(timer_data(t).convert('RGB'))

def make_timer_mask(t):
	return PIL_to_npimage(timer_data(t).split()[-1].convert('RGB'))
