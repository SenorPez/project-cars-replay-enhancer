import sys

if len(sys.argv) != 2:
	print ("Usage: 'python "+sys.argv[0]+" <configfile>'")
else:
	from importlib import import_module
	import moviepy.editor as mpy
	from moviepy.editor import afx, vfx
	from moviepy.video.io.bindings import PIL_to_npimage
	from PIL import Image

	from black_test import black_test
	from get_telemetry import get_telemetry
	from make_results import make_results, make_results_mask
	from make_title import make_title, make_title_mask
	from make_series_standings import make_series_standings, make_series_standings_mask
	from UpdatedVideoClip import UpdatedVideoClip, simWorld

	g = import_module(".".join(sys.argv[1][:-3].split('/')[1:]))
	get_telemetry(g.sourcetelemetry)

	video = black_test(g.sourcevideo)
	video_width, video_height = video.size

	backdrop = Image.open(g.backdrop).resize((video_width, video_height))
	logo = Image.open(g.logo).resize((g.logo_width, g.logo_height))
	backdrop.paste(logo, (backdrop.width-logo.width, backdrop.height-logo.height), logo)
	backdrop = mpy.ImageClip(PIL_to_npimage(backdrop))
	title = mpy.ImageClip(make_title()).set_duration(6).set_position(('center', 'center'))

	standingWorld = simWorld('make_standings', g.racestart)
	standing = UpdatedVideoClip(standingWorld)
	standing = standing.set_position((g.margin, g.margin)).set_duration(video.duration)
	standing_mask = mpy.ImageClip(standingWorld.make_mask(), ismask=True, duration=video.duration)
	standing = standing.set_mask(standing_mask)

	timerWorld = simWorld('make_timer', g.racestart)
	timer = UpdatedVideoClip(timerWorld)
	timer_width, timer_height = timer.size
	timer = timer.set_position((video_width-timer_width-g.margin, g.margin)).set_duration(video.duration)
	timer_mask = mpy.ImageClip(timerWorld.make_mask(), ismask=True, duration=video.duration)
	timer = timer.set_mask(timer_mask)

	result = mpy.ImageClip(make_results()).set_duration(20).set_position(('center', 'center'))
	result.mask = result.mask.fx(vfx.fadeout, 1)
	series_standings = mpy.ImageClip(make_series_standings()).set_start(20).set_duration(20).set_position(('center', 'center'))
	series_standings.mask = series_standings.mask.fx(vfx.fadein, 1)

	intro = mpy.CompositeVideoClip([backdrop, title]).set_duration(6).fx(vfx.fadeout, 1)
	mainevent = mpy.CompositeVideoClip([video, standing, timer]).set_duration(video.duration)
	outro = mpy.CompositeVideoClip([backdrop, result, series_standings]).set_duration(sum([x.duration for x in [result, series_standings]])).fx(vfx.fadein, 1)

	output = mpy.concatenate_videoclips([intro, mainevent, outro])

	#Full video.
	output.write_videofile(g.outputvideo)

	#Full video, low framerate
	#output.subclip(output.duration-60, output.duration).write_videofile(g.outputvideo, fps=10)

	#Subclip video.
	#output.subclip(30, 40).write_videofile(g.outputvideo, fps=10)
	#output.subclip(output.duration-25, output.duration).write_videofile(g.outputvideo, fps=10)
	#output.subclip(output.duration-25, output.duration-15).write_videofile(g.outputvideo, fps=10)

	#Single frame.
	#output.save_frame(g.outputvideo+".jpg", 30)

	#Multiple frames.
	#for frame in range(int(output.duration-45), int(output.duration-25)):
		#output.save_frame(g.outputvideo+"."+str(frame)+".jpg", frame)
