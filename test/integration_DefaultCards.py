"""
Integration testing of StaticBase.py
"""
from copy import deepcopy
import json
import os

import moviepy.editor as mpy
from PIL import Image
from tqdm import tqdm

from replayenhancer.DefaultCards \
    import RaceResults, SeriesChampion, SeriesStandings, StartingGrid
from replayenhancer.GTStandings import GTStandings
from replayenhancer.RaceData import RaceData


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
    pcre_standings = GTStandings(race_data, ups=framerate, **configuration)

    standings_clip_mask = mpy.VideoClip(make_frame=pcre_standings.make_mask_frame, ismask=True)
    standings_clip = mpy.VideoClip(make_frame=pcre_standings.make_frame).set_mask(standings_clip_mask)

    main_event = mpy.CompositeVideoClip([source_video, standings_clip]).set_duration(source_video.duration)

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

    pcre_results = RaceResults(
        sorted(result_data.classification, key=lambda x: x.position),
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
        series_standings.fadein(1)
    ], method="compose")
    output.write_videofile(output_prefix + '_output.mp4', fps=framerate)

if __name__ == '__main__':
    test_race(
        'assets/race1-descriptor',
        'assets/race1.json',
        'outputs/race_1')
k.