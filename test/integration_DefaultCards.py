"""
Integration testing of StaticBase.py
"""
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
    configuration = json.load(open(config_file))

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    video = mpy.VideoFileClip(configuration['source_video']).subclip(configuration['video_skipstart'], configuration['video_skipend'])
    standings = GTStandings(race_data, ups=30, **configuration)

    clip_mask = mpy.VideoClip(make_frame=standings.make_mask_frame, ismask=True)
    clip = mpy.VideoClip(make_frame=standings.make_frame).set_mask(clip_mask)

    composite = mpy.CompositeVideoClip([video, clip]).set_duration(video.duration)
    composite.write_videofile('outputs/test.mp4', fps=30)
    # composite.save_frame('outputs/out.png', 10)

    # standings = GTStandings(race_data, ups=30, **configuration)
    # clip = mpy.VideoClip(make_frame=standings.make_frame, duration=10)
    #
    # clip.write_videofile('outputs/test.mp4', fps=30)
    # clip.write_gif('outputs/test.gif', fps=30)

    # starting_grid = StartingGrid(
    #     sorted(race_data.starting_grid, key=lambda x: x.position),
    #     **configuration)
    # Image.fromarray(starting_grid.to_frame()).save(
    #     output_prefix + "_starting_grid.png")

    # progress = tqdm(
    #     desc='Processing data',
    #     total=race_data.telemetry_data.packet_count,
    #     unit='packets')
    #
    # race_data.get_data(30)
    # standings = GTStandings(
    #     race_data,
    #     ups=30,
    #     **configuration)
    # Image.fromarray(standings.to_frame()).save(
    #     output_prefix + '_standings.png')

    # while True:
    #     try:
    #         race_data.get_data()
    #         progress.update()
    #     except StopIteration:
    #         break
    # progress.close()
    #
    # results = RaceResults(
    #     sorted(race_data.classification, key=lambda x: x.position),
    #     **configuration)
    # Image.fromarray(results.to_frame()).save(
    #     output_prefix + '_results.png')
    #
    # series_standings = SeriesStandings(
    #     race_data.classification,
    #     **configuration)
    # Image.fromarray(series_standings.to_frame()).save(
    #     output_prefix + '_series_standings.png')
    #
    # champion = SeriesChampion(
    #     race_data.classification,
    #     **configuration)
    # Image.fromarray(champion.to_frame()).save(
    #     output_prefix + '_champion.png')

if __name__ == '__main__':
    test_race(
        'assets/race1-descriptor',
        'assets/race1.json',
        'outputs/race_1')
