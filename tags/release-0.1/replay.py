import sys

if len(sys.argv) != 2:
	print ("Usage: 'python "+sys.argv[0]+" <configfile>'")
else:
	from importlib import import_module
	import moviepy.editor as mpy

	from black_test import black_test
	from get_telemetry import get_telemetry
	from make_results import make_results, make_results_mask
	from make_standings import make_standings, make_standings_mask
	from make_timer import make_timer, make_timer_mask
	from make_title import make_title, make_title_mask

	g = import_module(sys.argv[1][:-3])
	get_telemetry(g.sourcetelemetry)
	
	video = black_test(g.sourcevideo)
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

	#Full video.
	output.write_videofile(g.outputvideo)

	#Full video, low framerate
	#output.write_videofile(g.outputvideo, fps=10)

	#Subclip video. Note: May cause data to display incorrectly.
	#output.subclip(int(output.duration-30), output.duration).write_videofile(g.outputvideo, fps=10)

	#Single frame. Note: May cause data to display incorrectly.
	#output.save_frame(g.outputvideo+".jpg", 30)

	#Multiple frames. Note: May cause data to display incorrectly.
	#for frame in range(int(output.duration-30), int(output.duration)):
		#output.save_frame(g.outputvideo+"."+str(frame)+".jpg", frame)
