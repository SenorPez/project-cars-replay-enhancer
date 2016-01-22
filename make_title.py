from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
import os.path
import PIL.Image as plim
from PIL import ImageDraw
import sys

paths = os.path.split(os.path.abspath(sys.argv[1]))
sys.path.insert(0, paths[0])
g = import_module(os.path.splitext(paths[1])[0])

def title_data():
	data = g.telemetryData[0]

	startingGridData = sorted(((str(int(data[182+i*9]) & int('01111111', 2)), n, t if t is not None else "", c) for i, n, t, c in g.participantData), key=lambda x: int(x[0]))

	widths = [max([g.font.getsize(x[i])[0] for x in startingGridData[:16]]) for i in range(len(startingGridData[0]))]
	widths.append(sum(widths))

	heights = [max([g.font.getsize(x[i])[1] for x in startingGridData[:16]]) for i in range(len(startingGridData[0]))]
	dataHeight = max(heights)
	heights = [dataHeight for x in startingGridData[:16]]
	heights.append(g.headingfont.getsize(g.headingtext)[1])
	heights.append(g.font.getsize(g.subheadingtext)[1])

	text_width = widths[-1]+g.columnMargin*(len([x for x in widths[:-1] if x != 0])-1)
	text_height = sum(heights)+g.margin*len(heights)-1

	headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2
	bodyHeight = text_height-headerHeight

	topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), (255, 0, 0))

	material = plim.new('RGBA', (text_width+g.margin*2, text_height))
	material.paste(topMaterial, (0, 0))
	
	yPos = headerHeight
	for i, r in enumerate(startingGridData[:16]):
		if i % 2:
			materialColor = (255, 255, 255)
		else:
			materialColor = (192, 192, 192)

		dataMaterial = plim.new('RGBA', (text_width+g.margin*2, dataHeight+g.margin), materialColor)
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+g.margin

	return material, startingGridData, dataHeight, widths

def make_title():
	material, startingGridData, dataHeight, columnWidths = title_data()

	draw = ImageDraw.Draw(material)

	yPos = g.margin

	draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
	yPos += g.headingfont.getsize(g.headingtext)[1]

	draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
	yPos += g.font.getsize(g.subheadingtext)[1]+g.margin
	yPos += g.margin/2

	columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(columnWidths[0:i]) if columnWidths[i-1] != 0 else g.margin+g.columnMargin*(i-1)+sum(columnWidths[0:(i-1)]) for i, w in enumerate(columnWidths)]

	for i, n, t, c in [list(zip(x, columnPositions)) for x in startingGridData[:16]]:
		draw.text((i[1], yPos), str(i[0]), fill='black', font=g.font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
		draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
		yPos += dataHeight+g.margin

	return PIL_to_npimage(material)
	
def make_title_mask():
	material, *rest = title_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
