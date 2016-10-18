"""
Integration testing of StaticBase.py
"""
import json
import os
import re
import sys

import moviepy.editor as mpy
from moviepy.video.io.bindings import PIL_to_npimage
from PIL import Image, ImageDraw

from replayenhancer.DefaultCards \
    import SeriesStandings, StartingGrid
from replayenhancer.GTStandings import GTStandings
from replayenhancer.RaceData import RaceData
from replayenhancer.RaceResultsWithChange import RaceResultsWithChange
from replayenhancer.SeriesStandingsWithChange \
    import SeriesStandingsWithChange


def make_video(config_file):
    """
    Test of race data.
    """
    configuration = json.load(open(config_file))
    race_data = RaceData(configuration['source_telemetry'])
    result_data = RaceData(configuration['source_telemetry'])
    output_prefix = re.match(
        r'(.*)\.json$',
        os.path.basename(config_file)).group(1)

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    framerate = 30

    source_video = mpy.VideoFileClip(
        configuration['source_video']
    ).subclip(
        configuration['video_skipstart'],
        configuration['video_skipend'])

    pcre_standings = GTStandings(
        race_data,
        ups=framerate,
        **configuration)
    standings_clip_mask = mpy.VideoClip(
        make_frame=pcre_standings.make_mask_frame,
        ismask=True)
    standings_clip = mpy.VideoClip(
        make_frame=pcre_standings.make_frame
    ).set_mask(standings_clip_mask)

    try:
        if sys.argv[2] == "sync":
            def timecode_frame(time):
                """
                Custom make frame for timecode.
                """
                timecode_image = Image.new('RGB', (200, 50))
                draw = ImageDraw.Draw(timecode_image)
                draw.text((50, 25), "%.02f"%(time))
                return PIL_to_npimage(timecode_image)

            timecode_clip = mpy.VideoClip(
                timecode_frame,
                duration=source_video.duration
            ).set_position(('center', 'top'))

            first_lap_data = RaceData(configuration['source_telemetry'])
            while first_lap_data.drivers_by_index[0].laps_complete < 1:
                _ = first_lap_data.get_data()

            main_event = mpy.CompositeVideoClip(
                [source_video, standings_clip, timecode_clip]
            ).set_duration(
                source_video.duration
            ).subclip(
                first_lap_data.elapsed_time-5,
                first_lap_data.elapsed_time+5)
        else:
            raise IndexError

    except IndexError:
        main_event = mpy.CompositeVideoClip(
            [source_video, standings_clip]
        ).set_duration(source_video.duration)

    pcre_starting_grid = StartingGrid(
        sorted(race_data.starting_grid, key=lambda x: x.position),
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_starting_grid.to_frame()).save(
        output_prefix + "_starting_grid.png")
    starting_grid = mpy.ImageClip(
        pcre_starting_grid.to_frame()).set_duration(5)

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

    if not any([
            x['points'] for x
            in configuration['participant_config'].values()]):
        pcre_series_standings = SeriesStandings(
            result_data.classification,
            size=source_video.size,
            **configuration)
    else:
        pcre_series_standings = SeriesStandingsWithChange(
            result_data.classification,
            size=source_video.size,
            **configuration)
    Image.fromarray(pcre_series_standings.to_frame()).save(
        output_prefix + '_series_standings.png')
    series_standings = mpy.ImageClip(
        pcre_series_standings.to_frame()).set_duration(20)

    output = mpy.concatenate_videoclips([
        starting_grid.fadeout(1),
        main_event,
        results.fadein(1).fadeout(1),
        series_standings.fadein(1)
    ], method="compose")
    output.write_videofile(configuration['output_video'], fps=framerate)

if __name__ == '__main__':
    make_video(sys.argv[1])
