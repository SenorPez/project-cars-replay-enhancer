from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Title(StaticBase):
	def __init__(self, replay):
		self.replay = replay

		data = self.replay.telemetry_data[0][0]
		self.participant_queue = deque(self.participant_configurations)
		self.participant_data = self.replay.update_participants(self.participant_queue)

		self.starting_grid = sorted(((str(int(data[182+i*9]) & int('01111111', 2)), n, t if t is not None else "", c) for i, n, t, c in self.participant_data), key=lambda x: int(x[0]))

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)

		yPos = self.replay.margin

		draw.text((20, yPos), self.replay.heading_text, fill='white', font=self.replay.heading_font)
		yPos += self.replay.heading_font.getsize(self.replay.heading_text)[1]

		draw.text((20, yPos), self.replay.subheading_text, fill='white', font=self.replay.font)
		yPos += self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin
		yPos += self.replay.margin/2

		column_positions = [self.replay.margin if i == 0 else self.replay.margin+self.replay.column_margin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else self.replay.margin+self.replay.column_margin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

		for i, n, t, c in [list(zip(x, column_positions)) for x in self.starting_grid[:16]]:
			draw.text((i[1], yPos), str(i[0]), fill='black', font=self.replay.font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=self.replay.font)
			draw.text((t[1], yPos), str(t[0]), fill='black', font=self.replay.font)
			draw.text((c[1], yPos), str(c[0]), fill='black', font=self.replay.font)
			yPos += self.data_height+self.replay.margin

		return self.material

	def _make_material(self, bgOnly):
		self.widths = [max([self.replay.font.getsize(x[i])[0] for x in self.starting_grid[:16]]) for i in range(len(self.starting_grid[0]))]
		self.widths.append(sum(self.widths))

		heights = [max([self.replay.font.getsize(x[i])[1] for x in self.starting_grid[:16]]) for i in range(len(self.starting_grid[0]))]
		self.data_height = max(heights)
		heights = [self.data_height for x in self.starting_grid[:16]]
		heights.append(self.replay.heading_font.getsize(self.replay.heading_text)[1])
		heights.append(self.replay.font.getsize(self.replay.subheading_text)[1])

		header_height = self.replay.heading_font.getsize(self.replay.heading_text)[1]+self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin*2

		text_width = max(self.widths[-1]+self.replay.column_margin*(len([x for x in self.widths[:-1] if x != 0])-1), self.replay.heading_font.getsize(self.replay.heading_text)[0]+self.replay.column_margin+header_height, self.replay.font.getsize(self.replay.subheading_text)[0]+self.replay.column_margin+header_height)
		text_height = sum(heights)+self.replay.margin*len(heights)-1

		heading_material = Image.new('RGBA', (text_width+self.replay.margin*2, header_height), self.replay.heading_color)
		series_logo = Image.open(self.replay.series_logo).resize((heading_material.height, heading_material.height))
		heading_material.paste(series_logo, (heading_material.width-series_logo.width, 0))

		self.material = Image.new('RGBA', (text_width+self.replay.margin*2, text_height))
		self.material.paste(heading_material, (0, 0))
		
		yPos = header_height
		for i, r in enumerate(self.starting_grid[:16]):
			if i % 2:
				self.material_color = (255, 255, 255)
			else:
				self.material_color = (192, 192, 192)

			row_material = Image.new('RGBA', (text_width+self.replay.margin*2, self.data_height+self.replay.margin), self.material_color)
			self.material.paste(row_material, (0, yPos))
			yPos += self.data_height+self.replay.margin

		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(Title, self).to_frame()
	
	def make_mask(self):
		return super(Title, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Title, StaticBase))
	print('Instance:', isinstance(Title(0), StaticBase))
