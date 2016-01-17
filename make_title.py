from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
from PIL import ImageDraw
import sys

g = import_module(".".join(sys.argv[1][:-3].split('/')[1:]))

def title_data():
	data = g.telemetryData[0]

	startingGridData = sorted((int(data[182+i*9]) & int('01111111', 2), n, t, c) for i, n, t, c in g.participantData)
	widths = [(g.font.getsize(str(i))[0], g.font.getsize(n)[0], g.font.getsize(t)[0], g.font.getsize(c)[0], sum((g.font.getsize(str(i))[0], g.font.getsize(n)[0], g.font.getsize(t)[0], g.font.getsize(c)[0]))) for i, n, t, c in startingGridData]
	widths.append((0, 0, 0, 0, g.headingfont.getsize(g.headingtext)[0]))
	widths.append((0, 0, 0, 0, g.font.getsize(g.subheadingtext)[0]))

	heights = [max(g.font.getsize(str(i))[1], g.font.getsize(n)[1], g.font.getsize(t)[1], g.font.getsize(c)[1]) for i, n, t, c in startingGridData]
	dataHeight = max(heights)
	heights = [dataHeight for x in startingGridData]
	heights.append(g.headingfont.getsize(g.headingtext)[1])
	heights.append(g.font.getsize(g.subheadingtext)[1])

	columnWidths = [max(widths[:-1], key=lambda x: x[y])[y] for y in range(len(widths[0][:-1]))]+[sum([max(widths[:-1], key=lambda x: x[y])[y] for y in range(len(widths[0][:-1]))])]
	text_width = columnWidths[-1]+g.margin*3
	text_height = sum(heights)+g.margin*len(heights)-1

	headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2
	bodyHeight = text_height-headerHeight

	topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), (255, 0, 0))

	material = plim.new('RGBA', (text_width+g.margin*2, text_height))
	material.paste(topMaterial, (0, 0))
	
	yPos = headerHeight
	for i, r in enumerate(startingGridData[0:-1]):
		if i % 2:
			materialColor = (255, 255, 255)
		else:
			materialColor = (192, 192, 192)

		dataMaterial = plim.new('RGBA', (text_width+g.margin*2, dataHeight+g.margin), materialColor)
		material.paste(dataMaterial, (0, yPos))
		yPos += dataHeight+g.margin

	i += 1
	if i % 2:
		materialColor = (255, 255, 255)
	else:
		materialColor = (192, 192, 192)
	dataMaterial = plim.new('RGBA', (text_width+g.margin*2, dataHeight+g.margin), materialColor)
	material.paste(dataMaterial, (0, yPos))
	
	return material, startingGridData, dataHeight, columnWidths

def make_title():
	material, startingGridData, dataHeight, columnWidths = title_data()

	draw = ImageDraw.Draw(material)

	yPos = g.margin

	draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
	yPos += g.headingfont.getsize(g.headingtext)[1]

	draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
	yPos += g.font.getsize(g.headingtext)[1]+g.margin
	yPos += g.margin/2

	columnPositions = [g.margin*(i+1)+sum(columnWidths[0:i]) for i, w in enumerate(columnWidths)]

	for i, n, t, c in [list(zip(x, columnPositions)) for x in startingGridData]:
		draw.text((i[1], yPos), str(i[0]), fill='black', font=g.font)
		draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
		draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
		draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
		yPos += dataHeight+g.margin

	return PIL_to_npimage(material)
	
def make_title_mask():
	material, *rest = title_data()
	return PIL_to_npimage(material.split()[-1].convert('RGB'))
