import abc
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim

class DynamicBase(metaclass=abc.ABCMeta):
	@property
	@abc.abstractmethod
	def ups(self):
		"""Updates per second of the simulation."""

	@ups.setter
	@abc.abstractmethod
	def ups(self, value):
		return

	@property
	@abc.abstractmethod
	def clip_t(self):
		"""Current time in simulation."""

	@clip_t.setter
	@abc.abstractmethod
	def clip_t(self, value):
		return

	@abc.abstractmethod
	def update(self):
		"""Update the simulation including updating clip_t"""

	@abc.abstractmethod
	def to_frame(self):
		"""Render a frame based on the world's state."""
		return PIL_to_npimage(self._make_material(False).convert('RGB'))

	@abc.abstractmethod
	def make_mask(self):
		"""Default mask creation. Override to customize."""
		return PIL_to_npimage(self._make_material(True).split()[-1].convert('RGB'))

	@abc.abstractmethod
	def _write_data(self):
		"""Write data to the canvas."""

	@abc.abstractmethod
	def _make_material(self, bgOnly):
		"""Create material used as a canvas."""

	@abc.abstractmethod
	def _format_time(self, seconds):
		"""Default time formatter. Override to customize."""
		minutes, seconds = divmod(float(seconds), 60)
		hours, minutes = divmod(minutes, 60)

		retVal = (int(hours), int(minutes), float(seconds))

		if hours:
			return "{0:d}:{1:0>2d}:{2:0>5.2f}".format(*retVal)
		elif minutes:
			return "{1:d}:{2:0>5.2f}".format(*retVal)
		else:
			return "{2:.2f}".format(*retVal)
