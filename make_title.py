from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
from PIL import ImageDraw
from round_rectangle import round_rectangle

import replay_globals as g

def title_data():
	data = g.telemetryData[0]
	participantData = g.participantData
	teamData = g.teamData
	carData = g.carData

	margin = g.margin
	
	headingfont = g.headingfont
	font = g.font

	headingtext = g.headingtext
	subheadingtext = g.subheadingtext

	startingGridData = sorted({(int(data[182+i*9]) & int('01111111', 2), n, t, c) for (i, n), t, c in zip(participantData, teamData, carData)})

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

	margin = g.margin
	
	headingfont = g.headingfont
	font = g.font

	headingtext = g.headingtext
	subheadingtext = g.subheadingtext

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
