def format_time(seconds):
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

def import_globals(module):
	"""Imports global variable module."""

	from importlib import import_module
	import os
	import sys

	paths = os.path.split(os.path.abspath(module))
	sys.path.insert(0, paths[0])
	return import_module(os.path.splitext(paths[1])[0])
