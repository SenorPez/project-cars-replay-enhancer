from numpy import where, diff
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Results(StaticBase):
	def __init__(self, replay):
		self.replay = replay

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)

		yPos = self.replay.margin

		draw.text((20, yPos), self.replay.heading_text, fill='white', font=self.replay.heading_font)
		yPos += self.replay.heading_font.getsize(self.replay.heading_text)[1]

		draw.text((20, yPos), self.replay.subheading_text, fill='white', font=self.replay.font)
		yPos += self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin
		yPos += self.replay.margin/2

		column_positions = [self.replay.margin if i == 0 else self.replay.margin+self.replay.column_margin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else self.replay.margin+self.replay.column_margin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

		for p, n, t, c, l, et, bl, bs1, bs2, bs3, pts in [list(zip(x, column_positions)) for x in self.classification_data]:
			draw.text((p[1], yPos), str(p[0]), fill='black', font=self.replay.font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=self.replay.font)
			if t != "":
				draw.text((t[1], yPos), str(t[0]), fill='black', font=self.replay.font)
			draw.text((c[1], yPos), str(c[0]), fill='black', font=self.replay.font)
			draw.text((l[1]+(self.widths[4]-self.replay.font.getsize(str(l[0]))[0])/2, yPos), str(l[0]), fill='black', font=self.replay.font)
			draw.text((et[1]+(self.widths[5]-self.replay.font.getsize(str(et[0]))[0])/2, yPos), str(et[0]), fill='black', font=self.replay.font)
			draw.text((bl[1]+(self.widths[6]-self.replay.font.getsize(str(bl[0]))[0])/2, yPos), str(bl[0]), fill='black', font=self.replay.font)
			draw.text((bs1[1]+(self.widths[7]-self.replay.font.getsize(str(bs1[0]))[0])/2, yPos), str(bs1[0]), fill='black', font=self.replay.font)
			draw.text((bs2[1]+(self.widths[8]-self.replay.font.getsize(str(bs2[0]))[0])/2, yPos), str(bs2[0]), fill='black', font=self.replay.font)
			draw.text((bs3[1]+(self.widths[9]-self.replay.font.getsize(str(bs3[0]))[0])/2, yPos), str(bs3[0]), fill='black', font=self.replay.font)
			draw.text((pts[1]+(self.widths[10]-self.replay.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=self.replay.font)
			yPos += self.data_height+self.replay.margin

		return self.material

	def _make_material(self, bgOnly):
		#Find out who is lapped at the finish.
		#This is neccessary because PCARS shuffles the finish order as they cross
		#the line, not respecting laps-down.
		race_finish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2) == 2][0] + 1
		data = self.replay.telemetry_data[race_finish]

		lead_lap_indexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) >= int(data[10])]
		lapped_indexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) < int(data[10])]

		#Get lead lap self.classification_data, then append lapped self.classification_datas.
		data = self.replay.telemetry_data[-1]
		self.classification_data = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in self.replay.participant_data if i in lead_lap_indexes)
		self.classification_data += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in self.replay.participant_data if i in lapped_indexes)

		#Renumber
		self.classification_data = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(self.classification_data, 1)]

		sector_bests = [[-1, -1, -1] for x in range(len(self.classification_data))]
		sector_times = [list() for x in range(len(self.classification_data))]
		lap_times = [list() for x in range(len(self.classification_data))]
		personal_best_laps = ['' for x in range(len(self.classification_data))]

		for p, n, t, c, i, l in self.classification_data[:16]:
			lap_finish = race_finish
			if p != 1:
				try:
					while (self.replay.telemetry_data[race_finish][183+i*9] == self.replay.telemetry_data[lap_finish][183+i*9]):
						lap_finish += 1
				except IndexError:
					lap_finish = len(self.replay.telemetry_data)-1

			sector_times[i] = [float(self.replay.telemetry_data[x][186+i*9]) for x in where(diff([int(y[185+i*9]) & int('111', 2) for y in self.replay.telemetry_data[:lap_finish+1]]) != 0)[0].tolist() if float(self.replay.telemetry_data[x][186+i*9]) != -123.0]+[float(self.replay.telemetry_data[lap_finish][186+i*9])]

			sector_times[i] = sector_times[i][:divmod(len(sector_times[i]), 3)[0]*3]

			lap_times[i] = [sum(sector_times[i][x:x+3]) for x in range(0, len(sector_times[i]), 3)]
			personal_best_laps[i] = min([x for x in lap_times[i]])

			sector_bests[i][0] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 2 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
			sector_bests[i][1] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 3 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
			sector_bests[i][2] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 1 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])

		columnHeadings = [("Pos.", "Driver", "Team", "Car", "Laps", "Time", "Best Lap", "Best S1", "Best S2", "Best S3", "Points")]
		
		if len(self.replay.point_structure) < 17:
			self.replay.point_structure += [0] * (17-len(self.replay.point_structure))

		self.classification_data = [(str(p), n, t, c, str(l), self.format_time(sum(lap_times[i])), "{:.2f}".format(float(min(lap_times[i]))), "{:.2f}".format(float(sector_bests[i][0])), "{:.2f}".format(float(sector_bests[i][1])), "{:.2f}".format(float(sector_bests[i][2])), str(self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personal_best_laps if isinstance(x, float)]) == personal_best_laps[i] else self.replay.point_structure[p])) for p, n, t, c, i, l in self.classification_data[:16]]
		columnHeadings = [tuple([x if len([y[i] for y in self.classification_data if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
		self.classification_data = columnHeadings+self.classification_data

		self.widths = [max([self.replay.font.getsize(x[i])[0] for x in self.classification_data]) for i in range(len(self.classification_data[0]))]
		self.widths.append(sum(self.widths))

		heights = [max([self.replay.font.getsize(x[i])[1] for x in self.classification_data]) for i in range(len(self.classification_data[0]))]
		self.data_height = max(heights)
		heights = [self.data_height for x in self.classification_data]
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
		for i, r in enumerate(self.classification_data):
			if i % 2:
				self.material_color = (255, 255, 255)
			else:
				self.material_color = (192, 192, 192)

			row_material = Image.new('RGBA', (text_width+self.replay.margin*2, self.data_height+self.replay.margin), self.material_color)
			self.material.paste(row_material, (0, yPos))
			yPos += self.data_height+self.replay.margin

		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(Results, self).to_frame()
	
	def make_mask(self):
		return super(Results, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Results, StaticBase))
	print('Instance:', isinstance(Results(0), StaticBase))
