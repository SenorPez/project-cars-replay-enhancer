from numpy import where, diff
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Champion(StaticBase):	
	def __init__(self, replay):
		self.replay = replay

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)

		draw.text((self.replay.margin, self.replay.margin), self.replay.heading_text, fill='white', font=self.replay.heading_font)

		xPos = 300+self.replay.margin
		yPos = self.heading_height+self.replay.margin

		for r, n, t, c, *rest in self.standings[0:3]:
			if r == '1':
				draw.text((xPos, yPos), "Champion", fill='black', font=self.replay.heading_font)
				yPos += self.replay.heading_font.getsize("Champion")[1]
				draw.text((xPos, yPos), n, fill='black', font=self.replay.heading_font)
				yPos += self.replay.heading_font.getsize(n)[1]
			else:
				draw.text((xPos, yPos), "Runner Up", fill='black', font=self.replay.font)
				yPos += self.replay.font.getsize("Runner Up")[1]
				draw.text((xPos, yPos), n, fill='black', font=self.replay.font)
				yPos += self.replay.font.getsize(n)[1]
			draw.text((xPos+self.replay.column_margin, yPos), t, fill='black', font=self.replay.font)
			yPos += self.replay.font.getsize(t)[1]
			draw.text((xPos+self.replay.column_margin, yPos), c, fill='black', font=self.replay.font)
			yPos += self.replay.font.getsize(c)[1]+self.replay.margin

		return self.material
		
	def _make_material(self, bgOnly):
		#Find out who is lapped at the finish.
		#This is neccessary because PCARS shuffles the finish order as they cross
		#the line, not respecting laps-down.
		race_finish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2) == 2][0] + 1
		data = self.replay.telemetry_data[race_finish]

		lead_lap_indexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) >= int(data[10])]
		lapped_indexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) < int(data[10])]

		#Get lead lap classification, then append lapped classifications.
		data = self.replay.telemetry_data[-1]
		classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in self.replay.participant_data if i in lead_lap_indexes)
		classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in self.replay.participant_data if i in lapped_indexes)

		#Renumber
		classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(classification, 1)]

		sector_times = [list() for x in range(len(classification))]
		lap_times = [list() for x in range(len(classification))]
		personal_best_laps = ['' for x in range(len(classification))]

		for p, n, t, c, i, l in classification[:16]:
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

		if len(self.replay.point_structure) < 17:
			self.replay.point_structure += [0] * (17-len(self.replay.point_structure))

		if len(self.replay.points) < 17:
			self.replay.points += (0,) * (17-len(self.replay.points))

		self.standings = [(n, t, c, str(self.replay.points[i]+self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personal_best_laps if isinstance(x, float)]) == personal_best_laps[i] else self.replay.points[i]+self.replay.point_structure[p])) for p, n, t, c, i, l in classification[:16]]
		for i, x in enumerate(sorted(self.standings, key=lambda x: (-int(x[3]), str(x[0]).split(" ")[-1]))):
			if i == 0:
				self.standings[i] = (str(1),)+x
			elif self.standings[i][-1] == self.standings[i-1][-1]:
				self.standings[i] = (str(self.standings[i-1][0]),)+x
			else:
				self.standings[i] = (str(i+1),)+x

		heading_width = self.replay.heading_font.getsize(self.replay.heading_text)[0]+self.replay.margin*2
		text_width = max([max([self.replay.heading_font.getsize(n)[0] if r == '1' else self.replay.font.getsize(n)[0], self.replay.font.getsize(t)[0]+self.replay.column_margin, self.replay.font.getsize(c)[0]+self.replay.column_margin]) for r, n, t, c, *rest in self.standings[0:3]]+[self.replay.heading_font.getsize("Champion")[0]]+[self.replay.font.getsize("Runner Up")[0]])+self.replay.margin*2

		self.heading_height = self.replay.heading_font.getsize(self.replay.heading_text)[1]+self.replay.margin*2
		text_height = max([300, sum([self.replay.heading_font.getsize(n)[1]+self.replay.font.getsize(t)[1]+self.replay.font.getsize(c)[1] if r == '1' else self.replay.font.getsize(n)[1]+self.replay.font.getsize(t)[1]+self.replay.font.getsize(c)[1] for r, n, t, c, *rest in self.standings[0:3]]+[self.replay.heading_font.getsize("Champion")[1]]+[self.replay.font.getsize("Runner Up")[1]*2])+self.replay.margin*4])

		width = max((heading_width, 300+text_width))
		height = self.heading_height+text_height

		heading_material = Image.new('RGBA', (width, self.heading_height), self.replay.heading_color)
		series_logo = Image.open(self.replay.series_logo).resize((300, 300))

		self.material = Image.new('RGBA', (width, height), (255, 255, 255))
		self.material.paste(heading_material, (0, 0))
		self.material.paste(series_logo, (0, self.heading_height))

		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(Champion, self).to_frame()
	
	def make_mask(self):
		return super(Champion, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Champion, StaticBase))
	print('Instance:', isinstance(Champion(0), StaticBase))
