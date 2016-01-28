import csv
from hashfile import hashfile
from hashlib import sha256
from importlib import import_module
import moviepy.editor as mpy
from numpy import diff, where, nonzero
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
		
		blackframes = [t for (t, f) in video.iter_frames(with_times=True, progress_bar=1) if f.mean() < g.threshold]

		try:
			videostart = blackframes[where(diff(blackframes)>g.gaptime)[0][0+g.skipstart]]
		except IndexError:
			#Some replays don't use blackframes to separate frames. In this case
			#the only blackframes are the start and stop of the replay.
			videostart = blackframes[where(diff(blackframes)>g.gaptime)[0][0]]
			luminosity_difference = abs(diff([f.sum() for f in video.subclip(videostart,videostart+60).iter_frames(dtype=float, progress_bar=1)]))
			luminosity_average = luminosity_difference.mean()
			luminosity_jumps = 1+nonzero(luminosity_difference>10*luminosity_average)[0]
			tt = [videostart] + list((1.0/video.fps)*luminosity_jumps+videostart) + [videostart+60]
			try:
				videostart = [tt[x] for x in nonzero(diff(tt)>1)[0]][0+g.skipstart]
			except IndexError:
				videostart = 0

		try:
			videoend = blackframes[::-1][where(diff(blackframes[::-1])<-g.gaptime)[0][0+g.skipend]]
		except IndexError:
			#Some replays don't use blackframes to separate frames. In this case
			#the only blackframes are the start and stop of the replay.
			videoend = blackframes[::-1][where(diff(blackframes[::-1])<-g.gaptime)[0][0]]
			luminosity_difference = abs(diff([f.sum() for f in video.subclip(videoend-60,videoend).iter_frames(dtype=float, progress_bar=1)]))
			luminosity_average = luminosity_difference.mean()
			luminosity_jumps = 1+nonzero(luminosity_difference>10*luminosity_average)[0]
			tt = [videoend-60] + list((1.0/video.fps)*luminosity_jumps+videoend-60) + [videoend]
			try:
				videoend = [tt[x] for x in nonzero(diff(tt)>1)[0]][0-g.skipend]
			except IndexError:
				videoend = video.duration

		finally:
			with open(g.cachefile, 'a') as h:
				cache = csv.writer(h)
				cache.writerow([os.path.abspath(filename), hashfile(open(filename, 'rb'), sha256()), videostart, videoend])
			return mpy.VideoFileClip(filename).subclip(videostart, videoend)
