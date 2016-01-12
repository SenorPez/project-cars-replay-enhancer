from importlib import import_module
import moviepy.editor as mpy
import sys

from black_test import black_test
from get_telemetry import get_telemetry
from make_results import make_results, make_results_mask
from make_standings import make_standings, make_standings_mask
from make_timer import make_timer, make_timer_mask
from make_title import make_title, make_title_mask

if len(sys.argv) != 4:
	print ("Usage: 'python'"+sys.argv[0]+" <video> <videooptions> <packetdirectory>'")

else:
	g = import_module(sys.argv[2][:-3])
	get_telemetry(sys.argv[3])
	
	video = black_test(sys.argv[1])
	video_width, video_height = video.size
	video = video.fx(mpy.vfx.freeze, t='end', freeze_duration=20)
	video = video.set_start(5).crossfadein(1)

	timer = mpy.VideoClip(make_timer)
	timer_mask = mpy.VideoClip(make_timer_mask).to_mask(1)
	timer_width, timer_height = timer.size
	timer = timer.set_position((video_width-timer_width-g.margin, g.margin)).set_duration(video.duration-20).crossfadeout(1)
	timer = timer.set_mask(timer_mask)
	timer = timer.set_start(5)

	standing = mpy.VideoClip(make_standings)
	standing_mask = mpy.VideoClip(make_standings_mask).to_mask(1)
	standing = standing.set_position((g.margin, g.margin)).set_duration(video.duration-20).crossfadeout(1)
	standing = standing.set_mask(standing_mask)
	standing = standing.set_start(5)
	
	title = mpy.VideoClip(make_title)
	title_mask = mpy.VideoClip(make_title_mask).to_mask(1)
	title = title.set_position(('center', 'center')).set_duration(5).crossfadeout(1)
	title = title.set_mask(title_mask)

	result = mpy.VideoClip(make_results)
	result_mask = mpy.VideoClip(make_results_mask).to_mask(1)
	result = result.set_start(video.duration-15)
	result = result.set_position(('center', 'center')).set_duration(20).crossfadein(1)

	output = mpy.CompositeVideoClip([video,
									 timer,
									 standing,
									 title,
									 result])
	#output.subclip(0, 50).write_videofile("edit.mp4", fps=10)
	#output.write_videofile("edit.mp4", fps=10)
	#output.write_videofile("edit.mp4")
	#output.subclip(50, 70).write_videofile("edit.mp4", fps=10)
	#output.save_frame("edit.jpg", 2)
	#for frame in range(40, 50):
		#output.save_frame("edit"+str(frame)+".jpg", frame)
	output.subclip(video.duration-20, video.duration).write_videofile(sys.argv[1][:-4]+"-output.mp4", fps=10)
