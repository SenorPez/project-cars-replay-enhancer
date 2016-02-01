import abc
from importlib import import_module
from numpy import where, diff
import PIL.Image as plim
from PIL import Image, ImageDraw
import os
import sys

from StaticBase import StaticBase

class SeriesStandings(StaticBase):
	def __init__(self, replay):
		self.replay = replay

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)
		yPos = self.replay.margin

		draw.text((20, yPos), self.replay.heading_text, fill='white', font=self.replay.heading_font)
		yPos += self.replay.heading_font.getsize(self.replay.heading_text)[1]

		draw.text((20, yPos), self.replay.subheading_text, fill='white', font=self.replay.font)
		yPos += self.replay.font.getsize(self.replay.subheading_text)[1]+int(self.replay.margin*1.5)

		columnPositions = [self.replay.margin if i == 0 else self.replay.margin+self.replay.column_margin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else self.replay.margin+self.replay.column_margin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

		for r, n, t, c, pts in [list(zip(x, columnPositions)) for x in self.classification_data]:
			draw.text((r[1], yPos), str(r[0]), fill='black', font=self.replay.font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=self.replay.font)
			draw.text((t[1], yPos), str(t[0]), fill='black', font=self.replay.font)
			draw.text((c[1], yPos), str(c[0]), fill='black', font=self.replay.font)
			draw.text((pts[1]+(self.widths[4]-self.replay.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=self.replay.font)
			yPos += self.row_height+self.replay.margin
		return self.material

	def _make_material(self, bgOnly):
		#Find out who is lapped at the finish.
		#This is neccessary because PCARS shuffles the finish order as they cross
		#the line, not respecting laps-down.
		raceFinish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2) == 2][0] + 1
		data = self.replay.telemetry_data[raceFinish]

		leadLapIndexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) >= int(data[10])]
		lappedIndexes = [i for i, *rest in self.replay.participant_data if int(data[184+i*9]) < int(data[10])]

		#Get lead lap classification, then append lapped classifications.
		data = self.replay.telemetry_data[-1]
		classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in self.replay.participant_data if i in leadLapIndexes)
		classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in self.replay.participant_data if i in lappedIndexes)

		#Renumber
		classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(classification, 1)]

		sectorTimes = [list() for x in range(len(classification))]
		lapTimes = [list() for x in range(len(classification))]
		personalBestLaps = ['' for x in range(len(classification))]

		for p, n, t, c, i, l in classification[:16]:
			lapFinish = raceFinish
			if p != 1:
				try:
					while (self.replay.telemetry_data[raceFinish][183+i*9] == self.replay.telemetry_data[lapFinish][183+i*9]):
						lapFinish += 1
				except IndexError:
					lapFinish = len(self.replay.telemetry_data)-1

			sectorTimes[i] = [float(self.replay.telemetry_data[x][186+i*9]) for x in where(diff([int(y[185+i*9]) & int('111', 2) for y in self.replay.telemetry_data[:lapFinish+1]]) != 0)[0].tolist() if float(self.replay.telemetry_data[x][186+i*9]) != -123.0]+[float(self.replay.telemetry_data[lapFinish][186+i*9])]

			sectorTimes[i] = sectorTimes[i][:divmod(len(sectorTimes[i]), 3)[0]*3]

			lapTimes[i] = [sum(sectorTimes[i][x:x+3]) for x in range(0, len(sectorTimes[i]), 3)]
			personalBestLaps[i] = min([x for x in lapTimes[i]])

		columnHeadings = [("Rank", "Driver", "Team", "Car", "Series Points")]
		
		if len(self.replay.point_structure) < 17:
			self.replay.point_structure += [0] * (17-len(self.replay.point_structure))

		if len(self.replay.points) < 17:
			self.replay.points += (0,) * (17-len(self.replay.points))

		self.classification_data = [(n, t, c, str(self.replay.points[i]+self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personalBestLaps if isinstance(x, float)]) == personalBestLaps[i] else self.replay.points[i]+self.replay.point_structure[p])) for p, n, t, c, i, l in classification[:16]]
		for i, x in enumerate(sorted(self.classification_data, key=lambda x: (-int(x[3]), str(x[0]).split(" ")[-1]))):
			if i == 0:
				self.classification_data[i] = (str(1),)+x
			elif self.classification_data[i][-1] == self.classification_data[i-1][-1]:
				self.classification_data[i] = (str(self.classification_data[i-1][0]),)+x
			else:
				self.classification_data[i] = (str(i+1),)+x

		columnHeadings = [tuple([x if len([y[i] for y in self.classification_data if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
		self.classification_data = columnHeadings + self.classification_data

		self.widths = [max([self.replay.font.getsize(x[i])[0] for x in self.classification_data]) for i in range(len(self.classification_data[0]))]
		self.widths.append(sum(self.widths))

		heights = [max([self.replay.font.getsize(x[i])[1] for x in self.classification_data]) for i in range(len(self.classification_data[0]))]
		self.row_height = max(heights)
		heights = [self.row_height for x in self.classification_data]
		heights.append(self.replay.heading_font.getsize(self.replay.heading_text)[1])
		heights.append(self.replay.font.getsize(self.replay.subheading_text)[1])

		heading_height = self.replay.heading_font.getsize(self.replay.heading_text)[1]+self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin*2

		text_width = max(self.widths[-1]+self.replay.column_margin*(len([x for x in self.widths[:-1] if x != 0])-1), self.replay.heading_font.getsize(self.replay.heading_text)[0]+self.replay.column_margin+heading_height, self.replay.font.getsize(self.replay.subheading_text)[0]+self.replay.column_margin+heading_height)
		text_height = sum(heights)+self.replay.margin*len(heights)-1

		heading_material = plim.new('RGBA', (text_width+self.replay.margin*2, heading_height), self.replay.heading_color)
		series_logo = plim.open(self.replay.series_logo).resize((heading_material.height, heading_material.height))
		heading_material.paste(series_logo, (heading_material.width-series_logo.width, 0))

		self.material = plim.new('RGBA', (text_width+self.replay.margin*2, text_height))
		self.material.paste(heading_material, (0, 0))
		
		yPos = heading_height
		for i, r in enumerate(self.classification_data):
			if i % 2:
				material_color = (255, 255, 255)
			else:
				material_color = (192, 192, 192)

			row_material = plim.new('RGBA', (text_width+self.replay.margin*2, self.row_height+self.replay.margin), material_color)
			self.material.paste(row_material, (0, yPos))
			yPos += self.row_height+self.replay.margin

		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(SeriesStandings, self).to_frame()
	
	def make_mask(self):
		return super(SeriesStandings, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(SeriesStandings, StaticBase))
	print('Instance:', isinstance(SeriesStandings(0), StaticBase))
