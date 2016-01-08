import csv
from hashfile import hashfile
from hashlib import sha256
import moviepy.editor as mpy
from numpy import diff, where

def black_test(filename, threshold=1, gaptime=1, skipstart=0, skipend=0, cache='file.cache'):
	#video = mpy.VideoFileClip(filename)

	#Test file hash, because blackframe detection is slow, so we cache it.
	#Get stored file.
	try:
		with open("file.cache", 'r') as h:
			cache = csv.reader(h)

			for row in cache:
				if row[0] == filename and row[1] == hashfile(open(filename, 'rb'), sha256()):
					videostart, videoend = float(row[2]), float(row[3])
					return mpy.VideoFileClip(filename).subclip(videostart, videoend)

	except FileNotFoundError:
		pass

	#Nothing found in the cache, so detect and add to cache.
	video = mpy.VideoFileClip(filename)
	blackframe = mpy.ColorClip(video.size, duration=video.duration).set_fps(video.fps).get_frame(0).astype("uint8")
	
	try:
		blackframes = [t for (t, f) in video.iter_frames(with_times=True) if f.mean() < threshold]
		videostart = blackframes[where(diff(blackframes)>gaptime)[0][0+skipstart]]
		videoend = blackframes[::-1][where(diff(blackframes[::-1])<-gaptime)[0][0+skipend]]
	except IndexError:
		videostart = 0
		videoend = video.duration

	with open("file.cache", 'w') as h:
		cache = csv.writer(h)
		cache.writerow([filename, hashfile(open(filename, 'rb'), sha256()), videostart, videoend])
	return mpy.VideoFileClip(filename).subclip(videostart, videoend)
