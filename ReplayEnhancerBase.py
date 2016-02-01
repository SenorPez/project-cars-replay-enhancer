class ReplayEnhancerBase():
	def format_time(self, seconds):
		"""Converts seconds into seconds, minutes:seconds, or
		   hours:minutes.seconds as appropriate."""

		minutes, seconds = divmod(float(seconds), 60)
		hours, minutes = divmod(minutes, 60)

		retVal = (int(hours), int(minutes), float(seconds))

		if hours:
			return "{0:d}:{1:0>2d}:{2:0>5.2f}".format(*retVal)
		elif minutes:
			return "{1:d}:{2:0>5.2f}".format(*retVal)
		else:
			return "{2:.2f}".format(*retVal)

	def import_globals(self, module):
		"""Imports global variable module."""
		paths = os.path.split(os.path.abspath(module))
		sys.path.insert(0, paths[0])
		return import_module(os.path.splitext(paths[1])[0])
