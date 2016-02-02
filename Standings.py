from numpy import diff, where
from PIL import Image, ImageDraw

from DynamicBase import DynamicBase

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

	def __init__(self, replay, clip_t=0, ups=30):
		self.replay = replay
		self.clip_t = clip_t
		self.ups = ups

		participants = [n for i, n, *rest in self.replay.participant_data]

		self.sector_status = {n:['current', 'none', 'none'] for n in participants}
		self.last_lap_valid = {n:True for n in participants}
		self.last_lap_sectors = {n:[-1, -1, -1] for n in participants}

		self.sector_bests = [-1, -1, -1]
		self.personal_bests = {n:[-1, -1, -1] for n in participants}
		self.best_lap = -1
		self.personal_best_laps = {n:-1 for n in participants}
		self.elapsed_times = {n:-1 for n in participants}

		self.current_laps = {n:1 for n in participants}
		self.last_lap_splits = {n:-1 for n in participants}
		self.leader_elapsed_time = -1
		self.leader_laps_completed = 0

		'''
		self.sector_status = [['current', 'none', 'none'] for x in range(64)]
		self.last_lap_valid = [True for x in range(64)]
		self.last_lap_sectors = [[-1, -1, -1] for x in range(64)]

		self.sector_bests = [-1, -1, -1]
		self.personal_bests = [[-1, -1, -1] for x in range(64)]
		self.best_lap = -1
		self.personal_best_laps = [-1 for x in range(64)]
		self.elapsed_times = [-1 for x in range(64)]

		self.current_laps = [1 for x in range(64)]
		self.last_lap_splits = [-1 for x in range(64)]
		self.leader_elapsed_time = -1
		self.leader_laps_completed = 0
		'''

		self.max_lap_time = -1

		self.standings = list()

		self.next_change_time = -1
		self.current_group = 10

	def __sector_rectangles(self, data, height):
		invalid_color = (255, 0, 0)
		current_color = (255, 255, 0)
		race_best_color = (128, 0, 128)
		personal_best_color = (0, 128, 0)
		base_color = (255, 255, 255)
		border_color = (0, 0, 0)
		xPos = 0

		output = Image.new('RGB', (int(self.replay.margin*1.5)+4, height))
		draw = ImageDraw.Draw(output)

		for sector in data:
			if sector == 'invalid':
				fillColor = invalid_color
			elif sector == 'current':
				fillColor = current_color
			elif sector == 'racebest':
				fillColor = race_best_color
			elif sector == 'personalbest':
				fillColor = personal_best_color
			elif sector == 'none':
				fillColor = base_color
			else:
				fillColor = (0, 0, 255)

			draw.rectangle([(xPos, 0), (xPos+int(self.replay.margin/2)+1, height-1)], fill=fillColor, outline=border_color)
			xPos += int(self.replay.margin/2)+1

		return output

	def _write_data(self):
		materialWidth = self.material.size[0]
		lineLength = materialWidth-self.replay.margin*2

		draw = ImageDraw.Draw(self.material)

		columnPositions = [self.replay.margin*(i+1)+sum(self.columnWidths[0:i]) if i == 0 else self.replay.margin+self.replay.column_margin*(i)+sum(self.columnWidths[0:i]) for i, w in enumerate(self.columnWidths)]
		yPos = self.replay.margin/2

		for p, n, r, i, s, l, et, lx, cl in self.standings[:10]+self.standings[self.current_group:self.current_group+6]:
			for pp, nn, ss, ll, rr in [list(zip((p, n, s, l, r), columnPositions+[0]))]:
				draw.text((pp[1], yPos), str(pp[0]), fill='black', font=self.replay.font)
				draw.text((nn[1], yPos), str(nn[0]), fill='black', font=self.replay.font)


				if isinstance(self.last_lap_splits[n], int) and self.last_lap_splits[n] < 0:
					last_lap_time = "{}".format('')
				elif isinstance(self.last_lap_splits[n], int):
					suffix = " laps" if self.last_lap_splits[n] > 1 else " lap"
					last_lap_time = "{:+d}".format(self.last_lap_splits[n])+suffix
				elif isinstance(self.last_lap_splits[n], float) and self.last_lap_splits[n] > 0:
					last_lap_time = self.format_time(self.last_lap_splits[n])
				elif isinstance(self.last_lap_splits[n], float):
					last_lap_time = "+"+self.format_time(self.last_lap_splits[n]*-1)

				timeWidth = self.replay.font.getsize(last_lap_time)[0]

				tPos = int(materialWidth-self.replay.margin-timeWidth)

				draw.text((tPos, yPos), str(last_lap_time), fill='black', font=self.replay.font)

				draw.line([(self.replay.margin, yPos+self.dataHeight), (self.replay.margin+lineLength*rr[0], yPos+self.dataHeight)], fill=(255, 0, 0), width=2)
				draw.line([(self.replay.margin+lineLength*rr[0], yPos+self.dataHeight), (materialWidth-self.replay.margin, yPos+self.dataHeight)], fill=(255, 192, 192), width=2)

				self.material.paste(self.__sector_rectangles(self.sector_status[n], self.dataHeight), (ss[1]-2, int(yPos)))

				draw.ellipse([(self.replay.margin+lineLength*rr[0]-2, yPos+self.dataHeight-2), (self.replay.margin+lineLength*rr[0]+2, yPos+self.dataHeight+2)], fill=(255, 0, 0))

			yPos += self.dataHeight+self.replay.margin

		return self.material

	def _make_material(self, bgOnly):
		self.standings = self.update()

		if self.max_lap_time == -1:
			#Who has the slowest lap?
			splitData = [[float(self.replay.telemetry_data[y+1][186+i*9]) for y in where(diff([float(x[186+i*9]) for x in self.replay.telemetry_data]) != 0)[0].tolist()] for i in range(56)]
			self.max_lap_time = max([sum(x[i:i+3]) for x in splitData for i in range(0, len(x), 3)])

		maxMinutes, maxSeconds = divmod(self.max_lap_time, 60)
		maxHours, maxMinutes = divmod(maxMinutes, 60)

		if maxHours > 0:
			sizeString = "+24:00:00.00"
		elif maxMinutes > 0:
			sizeString = "+60:00.00"
		else:
			sizeString = "+00.00"

		widths = [(self.replay.font.getsize(str(p))[0], self.replay.font.getsize(str(n))[0], int(self.replay.margin*1.5), max([self.replay.font.getsize(str(sizeString))[0], self.replay.font.getsize("+00 laps")[0]])) for p, n, *rest in self.standings]

		heights = [max(self.replay.font.getsize(str(p))[1], self.replay.font.getsize(str(n))[1], self.replay.font.getsize(str("{:.2f}".format(0.00)))[1]) for p, n, *rest in self.standings]
		self.dataHeight = max(heights)
		heights = [self.dataHeight for x in self.standings[:16]]

		self.columnWidths = [max(widths, key=lambda x: x[y])[y] for y in range(len(widths[0]))]
		text_width = sum(self.columnWidths)+self.replay.column_margin*(len(widths[0])-1)
		text_height = sum(heights)+self.replay.margin*(len(heights)-1)

		self.material = Image.new('RGBA', (text_width+self.replay.margin*2, text_height+self.replay.margin))
		yPos = 0

		for i, r in enumerate(self.standings[:16]):
			if i % 2:
				materialColor = (255, 255, 255, 128)
			else:
				materialColor = (192, 192, 192, 128)

			dataMaterial = Image.new('RGBA', (text_width+self.replay.margin*2, self.dataHeight+self.replay.margin), materialColor)
			self.material.paste(dataMaterial, (0, yPos))
			yPos += self.dataHeight+self.replay.margin

		return self.material if bgOnly else self._write_data()

	def update(self):
		if self.clip_t > self.replay.sync_racestart:
			try:
				data = [x for x in self.replay.telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0]
			except IndexError:
				raceFinish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2) == 2][0] + 1
				data = self.replay.telemetry_data[raceFinish]
		else:
			data = self.replay.telemetry_data[0]
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
		
		self.standings = sorted({(int(data[182+i*9]) & int('01111111', 2), n.split(" ")[0][0]+". "+n.split(" ")[-1] if len(n.split(" ")) > 1 else n, float(data[181+i*9])/float(data[682]), int(i), int(data[185+i*9]) & int('111', 2), float(data[186+i*9]), float(data[-1]), int(data[183+i*9]), int(data[184+i*9])) for i, n, *rest in self.replay.participant_data})

		if self.next_change_time == -1:
			self.next_change_time = self.clip_t+5
		elif self.clip_t > self.next_change_time:
			self.current_group = self.current_group+6 if self.current_group+6 < len(self.standings) else 10
			self.next_change_time = self.clip_t+5

		for p, n, r, i, s, l, et, lx, cl in self.standings:
			if s == 1:
				#If we're in the first sector, we need to check to see if we've set a record in sector 3.
				if l != -123:
					self.sector_status[n][0] = 'current'

					if self.last_lap_sectors[n][0] != l:
						self.last_lap_sectors[n][0] = l

					if lx & int('10000000', 2) and r > 0:
						self.sector_status[n][1] = 'invalid'
						self.sector_status[n][2] = 'invalid'
						self.last_lap_valid[n] = False
					elif self.sector_status[n][2] != 'invalid':
						if self.sector_bests[2] == -1 or self.sector_bests[2] >= l:
							self.sector_bests[2] = l
							self.personal_bests[n][2] = l
							self.sector_status[n][2] = 'racebest'
						elif self.personal_bests[n][2] == -1 or self.personal_bests[n][2] >= l:
							self.personal_bests[n][2] = l
							self.sector_status[n][2] = 'personalbest'
						else:
							self.sector_status[n][2] = 'none'

					#Test to see if we've just started a new lap.
					if self.current_laps[n] != cl:
						self.elapsed_times[n] += float(sum(self.last_lap_sectors[n]))
						self.current_laps[n] = cl

						#Do we have a valid last lap? If so, compare records.
						#If not, set Sector 3 to invalid (to hold it at red until
						#we get back there and reset the flag.
						if self.last_lap_valid[n] and -1 not in self.last_lap_sectors[n]:
							self.last_lap_time = float(sum(self.last_lap_sectors[n]))
							if self.best_lap == -1 or self.best_lap > self.last_lap_time:
								self.best_lap = self.last_lap_time
								self.personal_best_laps[n] = self.last_lap_time
							elif self.personal_best_laps[n] == -1 or self.personal_best_laps[n] >= self.last_lap_time:
								self.personal_best_laps[n] = self.last_lap_time
						else:
							self.sector_status[n][2] = 'invalid'
							self.last_lap_valid[n] = True

						if p == 1:
							self.leader_laps_completed = cl
							self.leader_elapsed_time = self.elapsed_times[n]
							self.last_lap_splits[n] = float(sum(self.last_lap_sectors[n]))
						#Test to see if you're down a lap.
						elif self.leader_laps_completed > cl:
							self.last_lap_splits[n] = int(self.leader_laps_completed-cl)
						#Just a laggard.
						elif lx & int('01111111', 2) != 0:
							self.last_lap_splits[n] = float(self.leader_elapsed_time-self.elapsed_times[n])
			elif s == 2:
				#Sector 2 checks sector 1 records
				if l != -123:
					self.sector_status[n][1] = 'current'

					if self.last_lap_sectors[n][1] != l:
						self.last_lap_sectors[n][1] = l

					if lx & int('10000000', 2) and r > 0:
						self.sector_status[n][0] = 'invalid'
						self.sector_status[n][2] = 'invalid'
						self.last_lap_valid[n] = False
					elif self.sector_status[n][0] != 'invalid':
						if self.sector_bests[0] == -1 or self.sector_bests[0] >= l:
							self.sector_bests[0] = l
							self.personal_bests[n][0] = l
							self.sector_status[n][0] = 'racebest'
						elif self.personal_bests[n][0] == -1 or self.personal_bests[n][0] >= l:
							self.personal_bests[n][0] = l
							self.sector_status[n][0] = 'personalbest'
						else:
							self.sector_status[n][0] = 'none'
			elif s == 3:
				#Sector 3 checks sector 2 records.
				if l != -123:
					self.sector_status[n][2] = 'current'

					if self.last_lap_sectors[n][2] != l:
						self.last_lap_sectors[n][2] = l

					if lx & int('10000000', 2) and r > 0:
						self.sector_status[n][0] = 'invalid'
						self.sector_status[n][1] = 'invalid'
						self.last_lap_valid[n] = False
					elif self.sector_status[n][1] != 'invalid':
						if self.sector_bests[1] == -1 or self.sector_bests[1] >= l:
							self.sector_bests[1] = l
							self.personal_bests[n][1] = l
							self.sector_status[n][1] = 'racebest'
						elif self.personal_bests[n][1] == -1 or self.personal_bests[n][1] >= l:
							self.personal_bests[n][1] = l
							self.sector_status[n][1] = 'personalbest'
						else:
							self.sector_status[n][1] = 'none'

			self.last_lap_time = self.last_lap_splits[n]
		self.clip_t += float(1/self.ups)

		return self.standings

	def to_frame(self):
		return super(Standings, self).to_frame()

	def make_mask(self):
		return super(Standings, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Standings, DynamicBase))
	print('Instance:', isinstance(Standings(30), DynamicBase))
