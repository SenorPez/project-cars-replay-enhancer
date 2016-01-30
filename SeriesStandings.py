import abc
from importlib import import_module
from numpy import where, diff
import PIL.Image as plim
from PIL import Image, ImageDraw
import os
import sys

from ReplayEnhancer import format_time, import_globals

from StaticBase import StaticBase

g = import_globals(sys.argv[1])

class SeriesStandings(StaticBase):
	def _write_data(self):
		draw = ImageDraw.Draw(self.material)
		yPos = g.margin

		draw.text((20, yPos), g.headingtext, fill='white', font=g.headingfont)
		yPos += g.headingfont.getsize(g.headingtext)[1]

		draw.text((20, yPos), g.subheadingtext, fill='white', font=g.font)
		yPos += g.font.getsize(g.subheadingtext)[1]+int(g.margin*1.5)

		columnPositions = [g.margin if i == 0 else g.margin+g.columnMargin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else g.margin+g.columnMargin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

		for r, n, t, c, pts in [list(zip(x, columnPositions)) for x in self.startingGridData]:
			draw.text((r[1], yPos), str(r[0]), fill='black', font=g.font)
			draw.text((n[1], yPos), str(n[0]), fill='black', font=g.font)
			draw.text((t[1], yPos), str(t[0]), fill='black', font=g.font)
			draw.text((c[1], yPos), str(c[0]), fill='black', font=g.font)
			draw.text((pts[1]+(self.widths[4]-g.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=g.font)
			yPos += self.dataHeight+g.margin
		return self.material

	def _make_material(self, bgOnly):
		#Find out who is lapped at the finish.
		#This is neccessary because PCARS shuffles the finish order as they cross
		#the line, not respecting laps-down.
		raceFinish = [i for i, data in reversed(list(enumerate(g.telemetryData))) if int(data[9]) & int('111', 2) == 2][0] + 1
		data = g.telemetryData[raceFinish]

		leadLapIndexes = [i for i, *rest in g.participantData if int(data[184+i*9]) >= int(data[10])]
		lappedIndexes = [i for i, *rest in g.participantData if int(data[184+i*9]) < int(data[10])]

		#Get lead lap classification, then append lapped classifications.
		data = g.telemetryData[-1]
		classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in g.participantData if i in leadLapIndexes)
		classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in g.participantData if i in lappedIndexes)

		#Renumber
		classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(classification, 1)]

		sectorTimes = [list() for x in range(len(classification))]
		lapTimes = [list() for x in range(len(classification))]
		personalBestLaps = ['' for x in range(len(classification))]

		for p, n, t, c, i, l in classification[:16]:
			lapFinish = raceFinish
			if p != 1:
				try:
					while (g.telemetryData[raceFinish][183+i*9] == g.telemetryData[lapFinish][183+i*9]):
						lapFinish += 1
				except IndexError:
					lapFinish = len(g.telemetryData)-1

			sectorTimes[i] = [float(g.telemetryData[x][186+i*9]) for x in where(diff([int(y[185+i*9]) & int('111', 2) for y in g.telemetryData[:lapFinish+1]]) != 0)[0].tolist() if float(g.telemetryData[x][186+i*9]) != -123.0]+[float(g.telemetryData[lapFinish][186+i*9])]

			sectorTimes[i] = sectorTimes[i][:divmod(len(sectorTimes[i]), 3)[0]*3]

			lapTimes[i] = [sum(sectorTimes[i][x:x+3]) for x in range(0, len(sectorTimes[i]), 3)]
			personalBestLaps[i] = min([x for x in lapTimes[i]])

		columnHeadings = [("Rank", "Driver", "Team", "Car", "Series Points")]
		
		if len(g.pointStructure) < 17:
			g.pointStructure += [0] * (17-len(g.pointStructure))

		if len(g.points) < 17:
			g.points += [0] * (17-len(g.points))

		self.startingGridData = [(n, t, c, str(g.points[i]+g.pointStructure[p]+g.pointStructure[0] if min([x for x in personalBestLaps if isinstance(x, float)]) == personalBestLaps[i] else g.points[i]+g.pointStructure[p])) for p, n, t, c, i, l in classification[:16]]
		for i, x in enumerate(sorted(self.startingGridData, key=lambda x: (-int(x[3]), str(x[0]).split(" ")[-1]))):
			if i == 0:
				self.startingGridData[i] = (str(1),)+x
			elif self.startingGridData[i][-1] == self.startingGridData[i-1][-1]:
				self.startingGridData[i] = (str(self.startingGridData[i-1][0]),)+x
			else:
				self.startingGridData[i] = (str(i+1),)+x

		columnHeadings = [tuple([x if len([y[i] for y in self.startingGridData if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
		self.startingGridData = columnHeadings + self.startingGridData

		self.widths = [max([g.font.getsize(x[i])[0] for x in self.startingGridData]) for i in range(len(self.startingGridData[0]))]
		self.widths.append(sum(self.widths))

		heights = [max([g.font.getsize(x[i])[1] for x in self.startingGridData]) for i in range(len(self.startingGridData[0]))]
		self.dataHeight = max(heights)
		heights = [self.dataHeight for x in self.startingGridData]
		heights.append(g.headingfont.getsize(g.headingtext)[1])
		heights.append(g.font.getsize(g.subheadingtext)[1])

		text_width = self.widths[-1]+g.columnMargin*(len([x for x in self.widths[:-1] if x != 0])-1)
		text_height = sum(heights)+g.margin*len(heights)-1

		headerHeight = g.headingfont.getsize(g.headingtext)[1]+g.font.getsize(g.subheadingtext)[1]+g.margin*2

		topMaterial = plim.new('RGBA', (text_width+g.margin*2, headerHeight), g.headingcolor)
		serieslogo = plim.open(g.serieslogo).resize((topMaterial.height, topMaterial.height))
		topMaterial.paste(serieslogo, (topMaterial.width-serieslogo.width, 0))

		self.material = plim.new('RGBA', (text_width+g.margin*2, text_height))
		self.material.paste(topMaterial, (0, 0))
		
		yPos = headerHeight
		for i, r in enumerate(self.startingGridData):
			if i % 2:
				self.materialColor = (255, 255, 255)
			else:
				self.materialColor = (192, 192, 192)

			dataMaterial = plim.new('RGBA', (text_width+g.margin*2, self.dataHeight+g.margin), self.materialColor)
			self.material.paste(dataMaterial, (0, yPos))
			yPos += self.dataHeight+g.margin

		return self.material if bgOnly else self._write_data()

	def to_frame(self):
		return super(SeriesStandings, self).to_frame()
	
	def make_mask(self):
		return super(SeriesStandings, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(SeriesStandings, StaticBase))
	print('Instance:', isinstance(SeriesStandings(0), StaticBase))
