import abc
from importlib import import_module
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, where
import os.path
import PIL.Image as plim
from PIL import ImageDraw
import sys

from ReplayEnhancer import format_time, import_globals

from DynamicBase import DynamicBase

g = import_globals(sys.argv[1])

class Standings(DynamicBase):
	_clip_t = 0
	_ups = 30

	@property
	def clip_t(self):
		return self._clip_t

	@clip_t.setter
	def clip_t(self, value):
		self._clip_t = value

	@property
	def ups(self):
		return self._ups

	@ups.setter
	def ups(self, value):
		self._ups = value

	def __init__(self, clip_t, ups=30):
		self.clip_t = clip_t
		self.ups = ups

		self.sectorStatus = [['current', 'none', 'none'] for x in range(64)]
		self.lastLapValid = [True for x in range(64)]
		self.lastLapSectors = [[-1, -1, -1] for x in range(64)]

		self.currentLaps = [1 for x in range(64)]
		self.lastLapSplits = [-1 for x in range(64)]
		self.leaderET = -1
		self.leaderLapsCompleted = 0

		self.maxLapTime = -1

		self.standings = list()

		self.changeGroup = False
		self.nextChangeTime = -1
		self.currentGroup = 10

	def __sector_rectangles(self, data, height):
		invalidColor = (255, 0, 0)
		currentColor = (255, 255, 0)
		raceBestColor = (128, 0, 128)
		personalBestColor = (0, 128, 0)
		baseColor = (255, 255, 255)
		borderColor = (0, 0, 0)
		xPos = 0

		output = plim.new('RGB', (int(g.margin*1.5)+4, height))
		draw = ImageDraw.Draw(output)

		for sector in data:
			if sector == 'invalid':
				fillColor = invalidColor
			elif sector == 'current':
				fillColor = currentColor
			elif sector == 'racebest':
				fillColor = raceBestColor
			elif sector == 'personalbest':
				fillColor = personalBestColor
			elif sector == 'none':
				fillColor = baseColor
			else:
				fillColor = (0, 0, 255)

			draw.rectangle([(xPos, 0), (xPos+int(g.margin/2)+1, height-1)], fill=fillColor, outline=borderColor)
			xPos += int(g.margin/2)+1

		return output

	def _write_data(self):
		materialWidth = self.material.size[0]
		lineLength = materialWidth-g.margin*2

		draw = ImageDraw.Draw(self.material)

		columnPositions = [g.margin*(i+1)+sum(self.columnWidths[0:i]) if i == 0 else g.margin+g.columnMargin*(i)+sum(self.columnWidths[0:i]) for i, w in enumerate(self.columnWidths)]
		yPos = g.margin/2

		for p, n, r, i, s, l, et, lx, cl in self.standings[:10]+self.standings[self.currentGroup:self.currentGroup+6]:
			for pp, nn, ss, ll, rr in [list(zip((p, n, s, l, r), columnPositions+[0]))]:
				draw.text((pp[1], yPos), str(pp[0]), fill='black', font=g.font)
				draw.text((nn[1], yPos), str(nn[0]), fill='black', font=g.font)


				if isinstance(self.lastLapSplits[i], int) and self.lastLapSplits[i] < 0:
					lastLapTime = "{}".format('')
				elif isinstance(self.lastLapSplits[i], int):
					suffix = " laps" if self.lastLapSplits[i] > 1 else " lap"
					lastLapTime = "{:+d}".format(self.lastLapSplits[i])+suffix
				elif isinstance(self.lastLapSplits[i], float) and self.lastLapSplits[i] > 0:
					lastLapTime = format_time(self.lastLapSplits[i])
				elif isinstance(self.lastLapSplits[i], float):
					lastLapTime = "+"+format_time(self.lastLapSplits[i]*-1)

				timeWidth = g.font.getsize(lastLapTime)[0]

				tPos = int(materialWidth-g.margin-timeWidth)

				draw.text((tPos, yPos), str(lastLapTime), fill='black', font=g.font)

				draw.line([(g.margin, yPos+self.dataHeight), (g.margin+lineLength*rr[0], yPos+self.dataHeight)], fill=(255, 0, 0), width=2)
				draw.line([(g.margin+lineLength*rr[0], yPos+self.dataHeight), (materialWidth-g.margin, yPos+self.dataHeight)], fill=(255, 192, 192), width=2)

				self.material.paste(self.__sector_rectangles(self.sectorStatus[i], self.dataHeight), (ss[1]-2, int(yPos)))

				draw.ellipse([(g.margin+lineLength*rr[0]-2, yPos+self.dataHeight-2), (g.margin+lineLength*rr[0]+2, yPos+self.dataHeight+2)], fill=(255, 0, 0))

			yPos += self.dataHeight+g.margin

		return self.material

	def _make_material(self, bgOnly):
		self.standings = self.update()

		if self.maxLapTime == -1:
			#Who has the slowest lap?
			splitData = [[float(g.telemetryData[y+1][186+i*9]) for y in where(diff([float(x[186+i*9]) for x in g.telemetryData]) != 0)[0].tolist()] for i in range(56)]
			self.maxLapTime = max([sum(x[i:i+3]) for x in splitData for i in range(0, len(x), 3)])

		maxMinutes, maxSeconds = divmod(self.maxLapTime, 60)
		maxHours, maxMinutes = divmod(maxMinutes, 60)

		if maxHours > 0:
			sizeString = "+24:00:00.00"
		elif maxMinutes > 0:
			sizeString = "+60:00.00"
		else:
			sizeString = "+00.00"

		widths = [(g.font.getsize(str(p))[0], g.font.getsize(str(n))[0], int(g.margin*1.5), max([g.font.getsize(str(sizeString))[0], g.font.getsize("+00 laps")[0]])) for p, n, *rest in self.standings]

		heights = [max(g.font.getsize(str(p))[1], g.font.getsize(str(n))[1], g.font.getsize(str("{:.2f}".format(0.00)))[1]) for p, n, *rest in self.standings]
		self.dataHeight = max(heights)
		heights = [self.dataHeight for x in self.standings[:16]]

		self.columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
		text_width = sum(self.columnWidths)+g.columnMargin*(len(widths[0])-1)
		text_height = sum(heights)+g.margin*(len(heights)-1)

		self.material = plim.new('RGBA', (text_width+g.margin*2, text_height+g.margin))
		yPos = 0

		for i, r in enumerate(self.standings[:16]):
			if i % 2:
				materialColor = (255, 255, 255, 128)
			else:
				materialColor = (192, 192, 192, 128)

			dataMaterial = plim.new('RGBA', (text_width+g.margin*2, self.dataHeight+g.margin), materialColor)
			self.material.paste(dataMaterial, (0, yPos))
			yPos += self.dataHeight+g.margin

		return self.material if bgOnly else self._write_data()

	def update(self):
		if self.clip_t > g.racestart:
			try:
				data = [x for x in g.telemetryData if x[-1] > self.clip_t-g.racestart][0]
			except IndexError:
				raceFinish = [i for i, data in reversed(list(enumerate(g.telemetryData))) if int(data[9]) & int('111', 2) == 2][0] + 1
				data = g.telemetryData[raceFinish]
		else:
			data = g.telemetryData[0]
		'''
		Standings Data Structure
			p 0: int Race Position (sorted)
			n 1: string Name
			r 2: float Percentage of lap completed
			i 3: int Participant index
			s 4: int Current sector
			l 5: float Last sector time (-123 if none)
		   et 6: float Elapsed time
		   lx 7: int Laps completed and valid lap
		   cl 8: int Current lap
		'''
		
		self.standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1] if len(n.split(" ")) > 1 else n, float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]), int(data[184+i*9])) for i, n, *rest in g.participantData})

		if self.nextChangeTime == -1:
			self.nextChangeTime = self.clip_t+5
		elif self.clip_t > self.nextChangeTime:
			self.currentGroup = self.currentGroup+6 if self.currentGroup+6 < len(self.standings) else 10
			self.nextChangeTime = self.clip_t+5

		for p, n, r, i, s, l, et, lx, cl in self.standings:
			if s == 1:
				#If we're in the first sector, we need to check to see if we've set a record in sector 3.
				if l != -123:
					self.sectorStatus[i][0] = 'current'

					if self.lastLapSectors[i][0] != l:
						self.lastLapSectors[i][0] = l

					if lx & int('10000000', 2) and r > 0:
						self.sectorStatus[i][1] = 'invalid'
						self.sectorStatus[i][2] = 'invalid'
						self.lastLapValid[i] = False
					else:
						if g.sectorBests[2] == -1 or g.sectorBests[2] >= l:
							g.sectorBests[2] = l
							g.personalBests[i][2] = l
							self.sectorStatus[i][2] = 'racebest'
						elif g.personalBests[i][2] == -1 or g.personalBests[i][2] >= l:
							g.personalBests[i][2] = l
							self.sectorStatus[i][2] = 'personalbest'
						else:
							self.sectorStatus[i][2] = 'none'

					#Test to see if we've just started a new lap.
					if self.currentLaps[i] != cl:
						g.elapsedTimes[i] += float(sum(self.lastLapSectors[i]))
						self.currentLaps[i] = cl

						#Do we have a valid last lap? If so, compare records.
						#If not, then do nothing, but reset the flag.
						if self.lastLapValid[i] and -1 not in self.lastLapSectors[i]:
							self.lastLapTime = float(sum(self.lastLapSectors[i]))
							if g.bestLap == -1 or g.bestLap > self.lastLapTime:
								g.bestLap = self.lastLapTime
								g.personalBestLaps[i] = self.lastLapTime
							elif g.personalBestLaps[i] == -1 or g.personalBestLaps[i] >= self.lastLapTime:
								g.personalBestLaps[i] = self.lastLapTime
						else:
							self.lastLapValid[i] = True

						if p == 1:
							self.leaderLapsCompleted = cl
							self.leaderET = g.elapsedTimes[i]
							self.lastLapSplits[i] = float(sum(self.lastLapSectors[i]))
						#Test to see if you're down a lap.
						elif self.leaderLapsCompleted > cl:
							self.lastLapSplits[i] = int(self.leaderLapsCompleted-cl)
						#Just a laggard.
						elif lx & int('01111111', 2) != 0:
							self.lastLapSplits[i] = float(self.leaderET-g.elapsedTimes[i])
			elif s == 2:
				#Sector 2 checks sector 1 records
				if l != -123:
					self.sectorStatus[i][1] = 'current'

					if self.lastLapSectors[i][1] != l:
						self.lastLapSectors[i][1] = l

					if lx & int('10000000', 2) and r > 0:
						self.sectorStatus[i][0] = 'invalid'
						self.sectorStatus[i][2] = 'invalid'
						self.lastLapValid[i] = False
					else:
						if g.sectorBests[0] == -1 or g.sectorBests[0] >= l:
							g.sectorBests[0] = l
							g.personalBests[i][0] = l
							self.sectorStatus[i][0] = 'racebest'
						elif g.personalBests[i][0] == -1 or g.personalBests[i][0] >= l:
							g.personalBests[i][0] = l
							self.sectorStatus[i][0] = 'personalbest'
						else:
							self.sectorStatus[i][0] = 'none'
			elif s == 3:
				#Sector 3 checks sector 2 records.
				if l != -123:
					self.sectorStatus[i][2] = 'current'

					if self.lastLapSectors[i][2] != l:
						self.lastLapSectors[i][2] = l

					if lx & int('10000000', 2) and r > 0:
						self.sectorStatus[i][0] = 'invalid'
						self.sectorStatus[i][1] = 'invalid'
						self.lastLapValid[i] = False
					else:
						if g.sectorBests[1] == -1 or g.sectorBests[1] >= l:
							g.sectorBests[1] = l
							g.personalBests[i][1] = l
							self.sectorStatus[i][1] = 'racebest'
						elif g.personalBests[i][1] == -1 or g.personalBests[i][1] >= l:
							g.personalBests[i][1] = l
							self.sectorStatus[i][1] = 'personalbest'
						else:
							self.sectorStatus[i][1] = 'none'

			self.lastLapTime = self.lastLapSplits[i]
		self.clip_t += float(1/self.ups)

		return self.standings

	def to_frame(self):
		return super(Standings, self).to_frame()

	def make_mask(self):
		return super(Standings, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Timer, DynamicBase))
	print('Instance:', isinstance(Timer(30), DynamicBase))
