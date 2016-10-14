"""
Integration testing of StaticBase.py
"""
import json
import os

import moviepy.editor as mpy
from moviepy.video.io.bindings import PIL_to_npimage
from PIL import Image, ImageDraw

from replayenhancer.DefaultCards \
    import RaceResults, SeriesChampion, SeriesStandings, StartingGrid
from replayenhancer.GTStandings import GTStandings
from replayenhancer.RaceData import RaceData
from replayenhancer.RaceResultsWithChange import RaceResultsWithChange
from replayenhancer.SeriesStandingsWithChange import SeriesStandingsWithChange


def test_race(telemetry_data, config_file, output_prefix):
    """
    Test of race data.
    """
    race_data = RaceData(telemetry_data)
    result_data = RaceData(telemetry_data)
    configuration = json.load(open(config_file))

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    framerate = 30

    source_video = mpy.VideoFileClip(configuration['source_video']).subclip(configuration['video_skipstart'], configuration['video_skipend'])

    def make_time(t):
        image = Image.new('RGB', (100, 100))
        draw = ImageDraw.Draw(image)
        draw.text((5, 50), "%.02f"%(t))
        return PIL_to_npimage(image)

    time_clip = mpy.VideoClip(make_frame=make_time, duration=source_video.duration)
    time_clip.set_position((800, 'top'))
    source_video = mpy.CompositeVideoClip([source_video, time_clip])

    pcre_standings = GTStandings(race_data, ups=framerate, **configuration)
    standings_clip_mask = mpy.VideoClip(make_frame=pcre_standings.make_mask_frame, ismask=True)
    standings_clip = mpy.VideoClip(make_frame=pcre_standings.make_frame).set_mask(standings_clip_mask)
    
    main_event = mpy.CompositeVideoClip([source_video, standings_clip]).set_duration(source_video.duration).subclip(0, 70)
   
    pcre_starting_grid = StartingGrid(
        sorted(race_data.starting_grid, key=lambda x: x.position),
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_starting_grid.to_frame()).save(
        output_prefix + "_starting_grid.png")
    starting_grid = mpy.ImageClip(pcre_starting_grid.to_frame()).set_duration(5)

    while True:
        try:
            result_data.get_data()
        except StopIteration:
            break

    pcre_results = RaceResultsWithChange(
        sorted(result_data.classification, key=lambda x: x.position),
        result_data.starting_grid,
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_results.to_frame()).save(
        output_prefix + '_results.png')
    results = mpy.ImageClip(pcre_results.to_frame()).set_duration(20)

    pcre_series_standings = SeriesStandings(
        result_data.classification,
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_series_standings.to_frame()).save(
        output_prefix + '_series_standings.png')
    series_standings = mpy.ImageClip(pcre_series_standings.to_frame()).set_duration(20)

    pcre_champion = SeriesChampion(
        result_data.classification,
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_champion.to_frame()).save(
        output_prefix + '_champion.png')
    champion = mpy.ImageClip(pcre_champion.to_frame()).set_duration(20)
    
    output = mpy.concatenate_videoclips([
        starting_grid.fadeout(1),
        main_event,
        results.fadein(1).fadeout(1),
        series_standings.fadein(1).fadeout(1),
        champion.fadein(1)
    ], method="compose")
    output.write_videofile(output_prefix + '.mp4', fps=framerate)

if __name__ == '__main__':
    test_race(
        'assets/race8',
        'assets/race8.json',
        'outputs/race8')
