import abc
from importlib import import_module
import PIL.Image as plim
from PIL import ImageDraw
import os
import sys

from DynamicBase import DynamicBase

class Timer(DynamicBase):
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

		self.time = -1
		self.lap = -1
		self.data_height = -1

	def _write_data(self):
		draw = ImageDraw.Draw(self.material)
		draw.text((self.replay.margin, int(self.replay.margin/2)), self.format_time(self.time), fill='black', font=self.replay.font)
		draw.text((self.replay.margin, self.data_height+int(self.replay.margin*1.5)), self.lap, fill='black', font=self.replay.font)

		return self.material

	def _make_material(self, bgOnly):
		self.time, self.lap = self.update()

		self.data_height = max((self.replay.font.getsize(self.time)[1], self.replay.font.getsize(self.lap)[1]))
		text_height = sum((self.replay.font.getsize(self.time)[1], self.replay.font.getsize(self.lap)[1], self.replay.margin))
		
		self.material = plim.new('RGBA', (100, text_height+self.replay.margin*2))

		topMaterial = plim.new('RGBA', (100, self.data_height+self.replay.margin), (255, 255, 255, 128))
		self.material.paste(topMaterial, (0, 0))

		bottomMaterial = plim.new('RGBA', (100, self.data_height+self.replay.margin), (192, 192, 192, 128))
		self.material.paste(bottomMaterial, (0, self.data_height+self.replay.margin))

		return self.material if bgOnly else self._write_data()

	def update(self):
		if self.clip_t > self.replay.sync_racestart:
			try:
				self.time = "{:.2f}".format(float([x for x in self.replay.telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0][13]))
				data = [x for x in self.replay.telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0]
			except IndexError:
				raceFinish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2)  == 2][0] + 1
				self.time = "{:.2f}".format(float(self.replay.telemetry_data[raceFinish][13]))
				data = self.replay.telemetry_data[raceFinish]

			currentLap = min((int(data[10]), int(data[184+int(data[3])*9])))
			self.lap = "{}/{}".format(currentLap, data[10])
		else:
			self.time = "0.00"
			data = self.replay.telemetry_data[0]
			self.lap = "{}/{}".format(1, data[10])

		self.clip_t += float(1/self.ups)

		return self.time, self.lap

	def to_frame(self):
		return super(Timer, self).to_frame()

	def make_mask(self):
		return super(Timer, self).make_mask()

if __name__ == '__main__':
	print('Subclass:', issubclass(Timer, DynamicBase))
	print('Instance:', isinstance(Timer(30), DynamicBase))
