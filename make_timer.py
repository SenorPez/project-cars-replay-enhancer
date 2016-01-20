from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
import os.path
import PIL.Image as plim
from PIL import ImageDraw
import sys

paths = os.path.split(os.path.abspath(sys.argv[1]))
sys.path.insert(0, paths[0])
g = import_module(os.path.splitext(paths[1])[0])

def write_data(material, dataHeight, time, lap):
	draw = ImageDraw.Draw(material)
	draw.text((g.margin, int(g.margin/2)), time, fill='black', font=g.font)
	draw.text((g.margin, dataHeight+int(g.margin*1.5)), lap, fill='black', font=g.font)
	
	return material

def make_material(t, bgOnly=False):
	time, lap = update_data(t)

	text_width = max((g.font.getsize(time)[0], g.font.getsize(lap)[0]))+g.margin
	dataHeight = max((g.font.getsize(time)[1], g.font.getsize(lap)[1]))
	text_height = sum((g.font.getsize(time)[1], g.font.getsize(lap)[1], g.margin))

	material = plim.new('RGBA', (100, text_height+g.margin*2))

	topMaterial = plim.new('RGBA', (100, dataHeight+g.margin), (255, 255, 255, 128))
	material.paste(topMaterial, (0, 0))
	bottomMaterial = plim.new('RGBA', (100, dataHeight+g.margin), (192, 192, 192, 128))
	material.paste(bottomMaterial, (0, dataHeight+g.margin))

	return material if bgOnly else write_data(material, dataHeight, time, lap)

def update_data(t):
	if t >= g.racestart:
		try:
			time = "{:.2f}".format(float([x for x in g.telemetryData if x[-1] > t-g.racestart][0][13]))
			data = [x for x in g.telemetryData if x[-1] > t-g.racestart][0]
		except IndexError:
			time = "{:.2f}".format(float(g.telemetryData[-1][13]))
			data = g.telemetryData[-1]

		currentLap = min((int(data[10]), max([int(data[184+i*9]) for i, _, _, _ in g.participantData])))
		lap = "{}/{}".format(currentLap, data[10])

	else:
		time = "{:.2f}".format(float(0))
		data = g.telemetryData[0]
		lap = "{}/{}".format(1, data[10])

	return time, lap

def make_mask(t):
	return PIL_to_npimage(make_material(t, bgOnly=True).split()[-1].convert('RGB'))
