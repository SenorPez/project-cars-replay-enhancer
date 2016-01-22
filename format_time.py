def format_time(seconds):
	minutes, seconds = divmod(float(seconds), 60)
	hours, minutes = divmod(minutes, 60)

	retVal = (int(hours), int(minutes), float(seconds))

	if hours:
		return "{0:d}:{1:0>2d}:{2:0>5.2f}".format(*retVal)
	elif minutes:
		return "{1:d}:{2:0>5.2f}".format(*retVal)
	else:
		return "{2:.2f}".format(*retVal)
