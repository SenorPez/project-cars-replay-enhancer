import csv
from hashfile import hashfile
from hashlib import sha256
from importlib import import_module
import moviepy.editor as mpy
from numpy import diff, where
import os.path
import sys

paths = os.path.split(os.path.abspath(sys.argv[1]))
sys.path.insert(0, paths[0])
g = import_module(os.path.splitext(paths[1])[0])

def black_test(filename):
	#Test file hash, because blackframe detection is slow, so we cache it.
	#Get stored file.
	try:
		with open(g.cachefile, 'r') as h:
			cache = csv.reader(h)

			for row in cache:
				try:
					if row[0] == os.path.abspath(filename) and row[1] == hashfile(open(filename, 'rb'), sha256()):
						videostart, videoend = float(row[2]), float(row[3])
						return mpy.VideoFileClip(filename).subclip(videostart, videoend)
				except IndexError:
					pass
			raise FileNotFoundError

	except FileNotFoundError:
		#Nothing found in the cache, so detect and add to cache.
		video = mpy.VideoFileClip(filename)
		
		try:
			blackframes = [t for (t, f) in video.iter_frames(with_times=True) if f.mean() < g.threshold]

			videostart = blackframes[where(diff(blackframes)>g.gaptime)[0][0]]
			videoend = blackframes[::-1][where(diff(blackframes[::-1])<-g.gaptime)[0][0+g.skipend]]
		except IndexError:
			#Some replays don't use blackframes to separate frames. In this case
			#the only blackframes are the start and stop of the replay.
			if len(where(diff(blackframes)>g.gaptime)[0]):
				videostart = blackframes[where(diff(blackframes)>g.gaptime)[0][0]]
				videoend = blackframes[::-1][where(diff(blackframes[::-1])<-g.gaptime)[0][0+g.skipend]]
			else:
				videostart = 0
				videoend = video.duration
		finally:
			with open(g.cachefile, 'a') as h:
				cache = csv.writer(h)
				cache.writerow([os.path.abspath(filename), hashfile(open(filename, 'rb'), sha256()), videostart, videoend])
			return mpy.VideoFileClip(filename).subclip(videostart, videoend)
