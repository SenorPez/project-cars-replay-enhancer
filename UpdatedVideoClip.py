from importlib import import_module
import moviepy.editor as mpy
from moviepy.video.io.bindings import PIL_to_npimage

class simWorld():
	def __init__(self, module, racestart, ups=30):
		self.mod = import_module(module)
		self.clip_t = racestart
		self.ups = ups

	def update(self):
		self.mod.update_data(self.clip_t)
		self.clip_t += float(1/self.ups)

	def to_frame(self):
		return PIL_to_npimage(self.mod.make_material(self.clip_t).convert('RGB'))

	def make_mask(self):
		return self.mod.make_mask(self.clip_t)

class UpdatedVideoClip(mpy.VideoClip):
	"""

	Class of clips whose make_frame requires some objects to
	be updated. Particularly practical in science where some
	algorithm needs to make some steps before a new frame can
	be generated.

	UpdatedVideoClips have the following make_frame:
	>>> def make_frame(t):
	>>>     while self.world.clip_t < t:
	>>>         world.update() # updates, and increases world.clip_t
	>>>     return world.to_frame()
	Parameters
	-----------
	world
	An object with the following attributes:
	- world.clip_t : the clip's time corresponding to the
	world's state
	- world.update() : update the world's state, (including
	increasing world.clip_t of one time step)
	- world.to_frame() : renders a frame depending on the world's state
	ismask
	True if the clip is a WxH mask with values in 0-1
	duration
	Duration of the clip, in seconds

	"""


	def __init__(self, world, ismask=False, duration=None):
		self.world = world
		def make_frame(t):
			while self.world.clip_t < t:
				world.update()
			return world.to_frame()
		mpy.VideoClip.__init__(self, make_frame= make_frame, ismask=ismask, duration=duration)
