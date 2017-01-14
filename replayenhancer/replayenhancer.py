"""
Main execution script.
"""
import argparse
import json
import os
import sys

import moviepy.editor as mpy
from PIL import Image, ImageDraw
from moviepy.video.io.bindings import PIL_to_npimage
from tqdm import tqdm

from replayenhancer.DefaultCards \
    import SeriesChampion, SeriesStandings, StartingGrid
from replayenhancer.GTStandings import GTStandings
from replayenhancer.RaceData import RaceData
from replayenhancer.RaceResultsWithChange import RaceResultsWithChange
from replayenhancer.SeriesStandingsWithChange \
    import SeriesStandingsWithChange


def make_video(config_file, *, framerate=None, sync=False):
    configuration = json.load(open(config_file))
    try:
        race_data = RaceData(configuration['source_telemetry'])
        result_data = RaceData(configuration['source_telemetry'])
    except KeyError:
        sys.exit("Configuration Error: Source Telemetry not found.")

    try:
        output_prefix = os.path.splitext(configuration['output_video'])[0]
    except KeyError:
        sys.exit("Configuration Error: Output Video not found.")

    try:
        champion = configuration['show_champion']
    except KeyError:
        champion = False

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    try:
        video_skipstart = configuration['video_skipstart']
    except KeyError:
        video_skipstart = 0

    try:
        video_skipend = configuration['video_skipend']
    except KeyError:
        video_skipend = None

    if 'source_video' in configuration \
            and configuration['source_video'] is not None:
        source_video = mpy.VideoFileClip(
            configuration['source_video']
        ).subclip(
            video_skipstart,
            video_skipend)
        if framerate is None:
            framerate = source_video.fps
    else:
        time_data = RaceData(configuration['source_telemetry'])
        with tqdm(desc="Detecting Telemetry Duration") as progress:
            while True:
                try:
                    _ = time_data.get_data()
                    progress.update()
                except StopIteration:
                    break
        source_video = mpy.ColorClip((1280, 1024)).set_duration(
            time_data.elapsed_time)

        if framerate is None:
            framerate = 30

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

    if sync:
        def timecode_frame(time):
            """
            Custom make frame for timecode.
            """
            timecode_image = Image.new('RGB', (100, 40))
            draw = ImageDraw.Draw(timecode_image)
            draw.text((10, 10), "%.02f"%(time))
            return PIL_to_npimage(timecode_image)

        timecode_clip = mpy.VideoClip(
            timecode_frame,
            duration=source_video.duration
        ).set_position(('center', 'top'))

        first_lap_data = RaceData(configuration['source_telemetry'])
        with tqdm(desc="Detecting Video Start") as progress:
            while not any(
                    [x.laps_complete > 0
                     for x in first_lap_data.drivers.values()]):
                _ = first_lap_data.get_data()
                progress.update()

        start_time = first_lap_data.elapsed_time - 10
        end_time = None

        with tqdm(desc="Detecting Video End") as progress:
            while not all(
                    [x.laps_complete > 0
                     for x in first_lap_data.drivers.values()]):
                try:
                    _ = first_lap_data.get_data()
                    progress.update()
                except StopIteration:
                    end_time = start_time + 60
                    break

        if end_time is None:
            end_time = first_lap_data.elapsed_time + 10

        main_event = mpy.CompositeVideoClip(
            [source_video, standings_clip, timecode_clip]
        ).set_duration(
            source_video.duration
        ).subclip(start_time, end_time)

    else:
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

    end_titles = list()

    pcre_results = RaceResultsWithChange(
        sorted(result_data.all_driver_classification, key=lambda x: x.position),
        result_data.starting_grid,
        size=source_video.size,
        **configuration)
    Image.fromarray(pcre_results.to_frame()).save(
        output_prefix + '_results.png')
    results = mpy.ImageClip(pcre_results.to_frame()).set_duration(20)

    end_titles.append(results)

    try:
        if any(configuration['point_structure']):
            if not any([
                    x['points'] for x
                    in configuration['participant_config'].values()]):
                pcre_series_standings = SeriesStandings(
                    result_data.all_driver_classification,
                    size=source_video.size,
                    **configuration)

                Image.fromarray(pcre_series_standings.to_frame()).save(
                    output_prefix + '_series_standings.png')
                series_standings = mpy.ImageClip(
                    pcre_series_standings.to_frame()).set_duration(20)

                end_titles.append(series_standings)
            else:
                pcre_series_standings = SeriesStandingsWithChange(
                    result_data.all_driver_classification,
                    size=source_video.size,
                    **configuration)

                Image.fromarray(pcre_series_standings.to_frame()).save(
                    output_prefix + '_series_standings.png')
                series_standings = mpy.ImageClip(
                    pcre_series_standings.to_frame()).set_duration(20)

                end_titles.append(series_standings)
    except KeyError:
        try:
            _ = configuration['point_structure']
            pcre_series_standings = SeriesStandings(
                result_data.all_driver_classification,
                size=source_video.size,
                **configuration)

            Image.fromarray(pcre_series_standings.to_frame()).save(
                output_prefix + '_series_standings.png')
            series_standings = mpy.ImageClip(
                pcre_series_standings.to_frame()).set_duration(20)

            end_titles.append(series_standings)
        except:
            pass

    if champion:
        pcre_series_champion = SeriesChampion(
            result_data.all_driver_classification,
            size=source_video.size,
            **configuration)
        Image.fromarray(pcre_series_champion.to_frame()).save(
            output_prefix + '_series_champion.png')
        series_champion = mpy.ImageClip(
            pcre_series_champion.to_frame()).set_duration(20)

        end_titles.append(series_champion)

    output = mpy.concatenate_videoclips([starting_grid.fadeout(1), main_event] + [clip.fadein(1).fadeout(1) for clip in end_titles[:-1]] + [end_titles[-1].fadein(1)], method="compose")

    output.write_videofile(configuration['output_video'], fps=float(framerate))


def main():
    parser = argparse.ArgumentParser(
        description="Project CARS Replay Enhancer")

    parser.add_argument('config')

    parser.add_argument(
        '-f',
        '--framerate',
        action='store',
        default=None)

    parser.add_argument(
        '-s',
        '--sync',
        action='store_true')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='Version 0.5 Release Candidate 2')

    args = parser.parse_args()

    make_video(
        args.config,
        framerate=args.framerate,
        sync=args.sync)

if __name__ == '__main__':
    main()
