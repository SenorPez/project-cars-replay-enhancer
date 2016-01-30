import abc
from importlib import import_module
import PIL.Image as plim
from PIL import Image, ImageDraw
import os
import sys

from ReplayEnhancer import format_time, import_globals

from StaticBase import StaticBase

g = import_globals(sys.argv[1])

class Title(StaticBase):
	def _write_data(self):
		draw = ImageDraw.Draw(self.material)

		yPos = g.margin

		draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
		yPos += g.headingfont.getsize(g.headingtext)[1]

		draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
		yPos += g.font.getsize(g.subheadingtext)[1]+g.margin
		yPos += g.margin/2

		columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else g.margin+g.columnMargin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

		for i, n, t, c in [list(zip(x, columnPositions)) for x in self.startingGridData[:16]]:
			draw.text((i[1], yPos), str(i[0]), fill='black', font=g.font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
			draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
			draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
			yPos += self.dataHeight+g.margin

		return self.material

	def _make_material(self, bgOnly):
		data = g.telemetryData[0]

		self.startingGridData = sorted(((str(int(data[182+i*9]) & int('01111111', 2)), n, t if t is not None else "", c) for i, n, t, c in g.participantData), key=lambda x: int(x[0]))

		self.widths = [max([g.font.getsize(x[i])[0] for x in self.startingGridData[:16]]) for i in range(len(self.startingGridData[0]))]
		self.widths.append(sum(self.widths))

		heights = [max([g.font.getsize(x[i])[1] for x in self.startingGridData[:16]]) for i in range(len(self.startingGridData[0]))]
		self.dataHeight = max(heights)
		heights = [self.dataHeight for x in self.startingGridData[:16]]
		heights.append(g.headingfont.getsize(g.headingtext)[1])
		heights.append(g.font.getsize(g.subheadingtext)[1])

		headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2

		text_width = max(self.widths[-1]+g.columnMargin*(len([x for x in self.widths[:-1] if x != 0])-1), g.headingfont.getsize(g.headingtext)[0]+g.columnMargin+headerHeight, g.font.getsize(g.subheadingtext)[0]+g.columnMargin+headerHeight)
		text_height = sum(heights)+g.margin*len(heights)-1

		topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), g.headingcolor)
		serieslogo = Image.open(g.serieslogo).resize((topMaterial.height, topMaterial.height))
		topMaterial.paste(serieslogo, (topMaterial.width-serieslogo.width, 0))

		self.material = plim.new('RGBA', (text_width+g.margin*2, text_height))
		self.material.paste(topMaterial, (0, 0))
		
		yPos = headerHeight
		for i, r in enumerate(self.startingGridData[:16]):
			if i % 2:
				self.materialColor = (255, 255, 255)
			else:
				self.materialColor = (192, 192, 192)

			dataMaterial = plim.new('RGBA', (text_width+g.margin*2, self.dataHeight+g.margin), self.materialColor)
			self.material.paste(dataMaterial, (0, yPos))
			yPos += self.dataHeight+g.margin

		#return self.material, self.startingGridData, self.dataHeight, self.widths
		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(Title, self).to_frame()
	
	def make_mask(self):
		return super(Title, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Title, StaticBase))
	print('Instance:', isinstance(Title(0), StaticBase))
