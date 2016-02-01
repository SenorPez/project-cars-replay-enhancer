import abc
from moviepy.video.io.bindings import PIL_to_npimage
import PIL.Image as plim
from ReplayEnhancerBase import ReplayEnhancerBase

class StaticBase(ReplayEnhancerBase, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def to_frame(self):
		"""Render the card with data. Override to customize."""
		return PIL_to_npimage(self._make_material(False).convert('RGB'))

	@abc.abstractmethod
	def make_mask(self):
		"""Default mask creation. Override to customize."""
		return PIL_to_npimage(self._make_material(True).split()[-1].convert('RGB'))

	@abc.abstractmethod
	def _write_data(self):
		"""Write data to the canvase."""

	@abc.abstractmethod
	def _make_material(self, bgOnly):
		"""Create material used as a canvas."""

