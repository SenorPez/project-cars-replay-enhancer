from numpy import where, diff, nonzero
from collections import deque
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Champion(StaticBase):	
	def __init__(self, replay):
		self.replay = replay

		participants = {x for x in self.replay.participant_lookup.values()}
		self.lap_finish = {n:-1 for n in participants}

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)

		draw.text((self.replay.margin, self.replay.margin), self.replay.heading_text, fill='white', font=self.replay.heading_font)

		xPos = 300+self.replay.margin
		yPos = self.heading_height+self.replay.margin

		for r, n, t, c, *rest in self.classification[0:3]:
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
		participants = {x for x in self.replay.participant_lookup.values()}
		sector_times = {n:[] for n in participants}
		laps_finished = {n:0 for n in participants}
		valid_lap_times = {n:[] for n in participants}
		personal_best_laps = {n:'' for n in participants}
		invalid_laps = {n:[] for n in participants}

		telemetry_data, participant_data, offset = zip(*[(x[0], x[-1], x[2]) for x in self.replay.telemetry_data if x[2] < self.replay.race_finish])
		participant_data = participant_data[-1]
		offset = offset[-1]
		telemetry_data = telemetry_data[-1][self.replay.race_finish-offset]

		lead_lap_indexes = [i for i, *rest in participant_data if int(telemetry_data[184+i*9]) >= int(telemetry_data[10])]
		lapped_indexes = [i for i, *rest in participant_data if int(telemetry_data[184+i*9]) < int(telemetry_data[10])]

		telemetry_data = self.replay.telemetry_data[0][0][-1]
		self.classification = sorted((int(telemetry_data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(telemetry_data[10])) for i, n, t, c in participant_data if i in lead_lap_indexes)
		self.classification += sorted((int(telemetry_data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(telemetry_data[183+i*9]) & int('01111111', 2)) for i, n, t, c in participant_data if i in lapped_indexes)
		self.classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(self.classification, 1)]

		telemetry_data = [x for x in zip(*self.replay.telemetry_data)][0]
		telemetry_data = [item for chunk in telemetry_data for item in chunk]

		for p, n, t, c, i, l in self.classification[:16]:
			lap_finish_number = self.replay.race_finish
			if p != 1:
				try:
					while (telemetry_data[self.replay.race_finish][183+i*9] == telemetry_data[lap_finish_number][183+i*9]):
						lap_finish_number += 1
				except IndexError:
					lap_finish_number = len(telemetry_data)-1
				self.lap_finish[n] = lap_finish_number

		for telemetry_data, participant_number, index_offset, participant_data in self.replay.telemetry_data:
			for i, n, *rest in participant_data:
				lap_finish = self.lap_finish[n] if self.lap_finish[n] != -1 else self.replay.race_end
				new_sector_times = [float(telemetry_data[x][186+i*9]) for x in nonzero(diff([int(y[185+i*9]) & int('111', 2) for data_index, y in enumerate(telemetry_data, index_offset) if data_index < lap_finish]))[0].tolist() if float(telemetry_data[x][186+i*9]) != -123.0]
				if float(telemetry_data[-1][186+i*9]) != -123.0:
					new_sector_times += [float(telemetry_data[-1][186+i*9])]
				
				try:
					if sector_times[n][-1] == new_sector_times[0]:
						sector_times[n] += new_sector_times[1:]
					else:
						raise IndexError
				except IndexError:
					sector_times[n] += new_sector_times

				laps_finished[n] = len(sector_times[n]) // 3

				invalid_laps[n] += list({int(x[184+i*9]) for x in telemetry_data if int(x[183+i*9]) & int('10000000') and float(x[186+i*9]) != -123.0})

		#Pull lap times. This doesn't filter out invalids, as this is used for the total time.
		#I recognize this is insanely sloppy, but at this point, I just can't care.
		#for n, v in sector_times.items():
			#lap_times[n] = [sum(sector_times[n][x:x+3]) for x in range(0, len(sector_times[n]), 3)]

		for n, laps in invalid_laps.items():
			for lap in reversed(sorted({x for x in laps})):
				del sector_times[n][(lap-1)*3:(lap-1)*3+3]

		for n, v in sector_times.items():
			#sector_times[n] += [sector_times[n].pop(0)]

			'''
			try:
				sector_bests[n][0] = min([x for x in sector_times[n][::3]])
			except ValueError:
				sector_bests[n][0] = -1

			try:
				sector_bests[n][1] = min([x for x in sector_times[n][1::3]])
			except ValueError:
				sector_bests[n][1] = -1

			try:
				sector_bests[n][2] = min([x for x in sector_times[n][2::3]])
			except ValueError:
				sector_bests[n][2] = -1
			'''

			sector_times[n] = sector_times[n][:divmod(len(sector_times[n]), 3)[0]*3]
			valid_lap_times[n] = [sum(sector_times[n][x:x+3]) for x in range(0, len(sector_times[n]), 3)]

			try:
				personal_best_laps[n] = min([x for x in valid_lap_times[n]])
			except ValueError:
				personal_best_laps[n] = -1

		in_classification = [n for _, n, *rest in self.classification]
		participant_data = self.replay.update_participants(deque(self.replay.participant_configurations))
		for n in sorted(laps_finished, key=laps_finished.get, reverse=True):
			if n not in in_classification:
				dnf_data = [x for x in participant_data if x[1] == n][0]
				self.classification.append(("DNF", dnf_data[1], dnf_data[2], dnf_data[3], "-1", laps_finished[n]))

		'''
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

		'''

		self.classification = [(i,) + tuple(rest) if i == "DNF" else (p,) + tuple(rest) for p, (i, *rest) in enumerate(self.classification, 1)]
		columnHeadings = [("Rank", "Driver", "Team", "Car", "Series Points")]
		
		if len(self.replay.point_structure) < 17:
			self.replay.point_structure += [0] * (17-len(self.replay.point_structure))

		if len(self.replay.point_structure) < 17:
			self.replay.point_structure += (0,) * (17-len(self.replay.point_structure))

		self.classification = [(n, t, c, "0" if p == "DNF" else "0" if l < 1 else str(self.replay.points[n]+self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personal_best_laps.values() if isinstance(x, float)]) == personal_best_laps[n] else self.replay.points[n]+self.replay.point_structure[p])) for p, n, t, c, i, l in self.classification[:16]]
		for i, x in enumerate(sorted(self.classification, key=lambda x: (-int(x[3]), str(x[0]).split(" ")[-1]))):
			if i == 0:
				self.classification[i] = (str(1),)+x
			elif self.classification[i][-1] == self.classification[i-1][-1]:
				self.classification[i] = (str(self.classification[i-1][0]),)+x
			else:
				self.classification[i] = (str(i+1),)+x

		heading_width = self.replay.heading_font.getsize(self.replay.heading_text)[0]+self.replay.margin*2
		text_width = max([max([self.replay.heading_font.getsize(n)[0] if r == '1' else self.replay.font.getsize(n)[0], self.replay.font.getsize(t)[0]+self.replay.column_margin, self.replay.font.getsize(c)[0]+self.replay.column_margin]) for r, n, t, c, *rest in self.classification[0:3]]+[self.replay.heading_font.getsize("Champion")[0]]+[self.replay.font.getsize("Runner Up")[0]])+self.replay.margin*2

		self.heading_height = self.replay.heading_font.getsize(self.replay.heading_text)[1]+self.replay.margin*2
		text_height = max([300, sum([self.replay.heading_font.getsize(n)[1]+self.replay.font.getsize(t)[1]+self.replay.font.getsize(c)[1] if r == '1' else self.replay.font.getsize(n)[1]+self.replay.font.getsize(t)[1]+self.replay.font.getsize(c)[1] for r, n, t, c, *rest in self.classification[0:3]]+[self.replay.heading_font.getsize("Champion")[1]]+[self.replay.font.getsize("Runner Up")[1]*2])+self.replay.margin*4])

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
