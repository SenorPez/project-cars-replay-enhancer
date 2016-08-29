"""
Provides the ReplayEnhancer and related classes.
"""
import argparse
import json
import os
import os.path

import moviepy.editor as mpy
from moviepy.editor import vfx
from moviepy.video.io.bindings import PIL_to_npimage
from PIL import Image, ImageDraw, ImageFont

from Champion import Champion
from Configuration import Configuration
from Results import Results
from SeriesStandings import SeriesStandings
from Standings import Standings
from RaceData import RaceData
from Timer import Timer
from Title import Title
from Track import Track
from UpdatedVideoClip import UpdatedVideoClip

from GTStandings import GTStandings

class ReplayEnhancer():
    """
    ReplayEnhancer class to hold configuration and execution
    data for Replays.
    """
    def __init__(self, configuration=None):
        with open(os.path.realpath(configuration), 'r') as config_file:
            try:
                json_data = json.load(config_file)
            except ValueError:
                raise

        self.race_mode = None

        self.font = ImageFont.truetype(
            json_data['font'],
            json_data['font_size'])
        self.heading_font = ImageFont.truetype(
            json_data['heading_font'],
            json_data['heading_font_size'])
        self.heading_color = tuple(json_data['heading_color'])

        self.heading_font_color = tuple(
            json_data['heading_font_color'])

        self.font_color = tuple(
            json_data['font_color'])

        self.backdrop = json_data['backdrop']
        self.logo = json_data['logo']
        self.logo_height = json_data['logo_height']
        self.logo_width = json_data['logo_width']
        self.series_logo = json_data['series_logo']

        self.result_lines = json_data['result_lines']

        self.show_champion = json_data['show_champion']

        self.heading_text = json_data['heading_text']
        self.subheading_text = json_data['subheading_text']

        self.margin = json_data['margin']
        self.column_margin = json_data['column_margin']

        self.source_video = json_data['source_video']
        self.source_telemetry = json_data['source_telemetry']
        self.telemetry_file = 'tele.csv'
        self.output_video = json_data['output_video']

        self.name_display = {k:v['display'] \
            for k, v in json_data['participant_config'].items()}

        additional_names = {k:k \
            for k, v \
            in json_data['additional_participant_config'].items()}
        self.name_display.update(additional_names)

        self.short_name_display = {k:v['short_display'] \
            for k, v in json_data['participant_config'].items()}

        additional_short_names = {k:v['short_display'] \
            for k, v \
            in json_data['additional_participant_config'].items()}
        self.short_name_display.update(additional_short_names)

        self.car_data = {k:v['car'] \
            for k, v in json_data['participant_config'].items()}
        additional_cars = {k:v['car'] \
            for k, v \
            in json_data['additional_participant_config'].items()}
        self.car_data.update(additional_cars)

        self.car_classes = json_data['car_classes']

        self.team_data = {k:v['team'] \
            for k, v in json_data['participant_config'].items()}
        additional_teams = {k:v['team'] \
            for k, v \
            in json_data['additional_participant_config'].items()}
        self.team_data.update(additional_teams)

        self.points = {k:v['points'] \
            for k, v in json_data['participant_config'].items()}
        additional_points = {k:v['points'] \
            for k, v \
            in json_data['additional_participant_config'].items()}
        self.points.update(additional_points)

        self.point_structure = json_data['point_structure']

        self.video_threshold = json_data['video_threshold']
        self.video_gaptime = json_data['video_gaptime']
        self.video_skipstart = json_data['video_skipstart']
        self.video_skipend = json_data['video_skipend']
        self.video_cache = json_data['video_cache']

        self.sync_racestart = json_data['sync_racestart']

        self.race_data = RaceData(self.source_telemetry, self)
        self.participant_data = list()
        self.participant_configurations = list()
        self.participant_lookup = dict()

        self.additional_participants = \
            [x for x \
            in json_data['additional_participant_config'].keys()]
        self.additional_participant_config = {k:v \
            for k, v \
            in json_data['additional_participant_config'].items()}

        self.viewed = None
        for name, data in json_data['participant_config'].items():
            try:
                if data['viewed']:
                    self.viewed = name
            except KeyError:
                pass

        self.telemetry_data = list()
        self.config_version = 4

        self.race_start = -1
        self.race_finish = -1
        self.race_p1_finish = -1
        self.race_end = -1

        self.size = None

        self.track = Track(self.race_data.track_length)

    @classmethod
    def new_configuration(cls):
        """
        Creates a new configuration file and builds
        a test video.
        """
        try:
            print("No configuration file provided.")
            print("Creating new configuration file.")

            config = Configuration()
            config.new_configuration()

            print("Creating low-quality video as {}".format(
                config.output_video))
            print(
                "If video trimming needs to be adjusted, run the ",
                "Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print(
                "To synchronize telemetry with video, run the ",
                "Project CARS Replay Enhancer with the `-r` option.")
            print(
                "Set the synchronization offset to the value shown "
                "on the Timer when the viewed car crosses the start ",
                "finish line to begin lap 2.")
            print(
                "Please wait. Telemetry being processed and ",
                "rendered. If this is the first time this data has ",
                "been used, it make take longer.")

            try:
                replay = cls(config.config_file)
            except ValueError as error:
                print("Invalid JSON in configuration file: {}".format(
                    error))
            else:
                start_video = replay.build_default_video(False)
                end_video = replay.build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips(
                    [start_video, end_video])
                output.write_videofile(
                    replay.output_video, fps=10, preset='superfast')
        except KeyboardInterrupt:
            raise

    @classmethod
    def edit_configuration(cls, previous_file):
        """
        Edits and exiting configuration file and builds a
        test video.
        """
        try:
            print("Editing configuration file {}".format(
                previous_file))

            config = Configuration(previous_file)
            config.new_configuration()

            print("Creating low-quality video as {}".format(
                config.output_video))
            print(
                "If video trimming needs to be adjusted, run the ",
                "Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print(
                "To synchronize telemetry with video, run the ",
                "Project CARS Replay Enhancer with the `-r` option.")
            print(
                "Set the synchronization offset to the value shown ",
                "on the Timer when the viewed car crosses the start ",
                "finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError as error:
                print("Invalid JSON in configuration file: {}".format(
                    error))
            else:
                start_video = replay.build_default_video(False)
                end_video = replay.build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips(
                    [start_video, end_video])
                output.write_videofile(
                    replay.output_video,
                    fps=10,
                    preset='superfast')

        except KeyboardInterrupt:
            raise

    @classmethod
    def edit_trim(cls, previous_file):
        """
        Updates the trimming parameters in the configuration
        file and builds a test video.
        """
        try:
            print("Editing configuration file {}".format(
                previous_file))

            config = Configuration(previous_file)
            config.modify_trim()

            print("Creating low-quality video as {}".format(
                config.output_video))
            print(
                "If video trimming needs to be adjusted, run the ",
                "Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print(
                "To synchronize telemetry with video, run the ",
                "Project CARS Replay Enhancer with the `-r` option.")
            print(
                "Set the synchronization offset to the value shown ",
                "on the Timer when the viewed car crosses the start ",
                "finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError:
                raise
            else:
                start_video = replay.build_default_video(False)
                end_video = replay.build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)

                output = mpy.concatenate_videoclips(
                    [start_video, end_video])
                output.write_videofile(
                    replay.output_video,
                    fps=10,
                    preset='superfast')

        except KeyboardInterrupt:
            raise

    @classmethod
    def edit_racestart(cls, previous_file):
        """
        Updates the race start parameters in the configuration
        file and builds a test video.
        """
        try:
            print(
                "Editing configuration file {}".format(
                    previous_file))

            config = Configuration(previous_file)
            config.modify_racestart()

            print(
                "Creating low-quality video as {}".format(
                    config.output_video))
            print(
                "If video trimming needs to be adjusted, run the ",
                "Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print(
                "To synchronize telemetry with video, run the ",
                "Project CARS Replay Enhancer with the `-r` option.")
            print(
                "Set the synchronization offset to the value shown ",
                "on the Timer when the viewed car crosses the start ",
                "finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError as error:
                print("Invalid JSON in configuration file: {}".format(
                    error))
            else:
                """
                start_video = replay.build_default_video(False)
                end_video = replay.build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips(
                    [start_video, end_video])
                output.write_videofile(
                    replay.output_video,
                    fps=10,
                    preset='superfast')
                """
                output1 = replay.build_custom_video(True, ups=10,
                                                    low_quality=True)
                output1 = output1.set_duration(
                    output1.duration).subclip(
                    output1.duration-150,
                    output1.duration)
                """
                output1 = output1.subclip(
                    0,
                    120)
                    """
                output1.write_videofile(replay.output_video)

                #output1 = output1.subclip(450, 540)
                #output1 = output1.subclip(455, 480)
                #output1.save_frame("outputs/output.jpg", 2)

        except KeyboardInterrupt:
            raise

    @classmethod
    def create_custom(cls, config_file):
        """
        Creates a custom video.
        Used right now for creating test videos, really.
        """
        try:
            print("Creating video with custom settings.")

            try:
                replay = cls(config_file)
            except ValueError as error:
                print("Invalid JSON in configuration file: {}".format(
                    error))
            else:
                output = replay.build_custom_video(True, ups=30)
                output.write_videofile(replay.output_video)
        except KeyboardInterrupt:
            raise

    @classmethod
    def create_video(cls, config_file):
        """
        Creates a video from the given replay parameters.
        """
        try:
            print("Creating video.")

            try:
                replay = cls(config_file)
            except ValueError as error:
                print("Invalid JSON in configuration file: {}".format(
                    error))
            else:
                output = replay.build_default_video(True)
                output.write_videofile(replay.output_video, fps=30)
        except KeyboardInterrupt:
            raise

    def build_custom_video(self, process_data, ups=30,
                           low_quality=False):
        """
        Builds a video with custom settings (used for testing).
        """

        if self.source_video is None:
            video = mpy.ColorClip(
                (1280, 720),
                duration=self.telemetry_data[-1][0][-1][-1])
        elif isinstance(self.video_skipstart, float) \
                or isinstance(self.video_skipend, float):
            video = mpy.VideoFileClip(
                self.source_video).subclip(
                    self.video_skipstart, self.video_skipend)
        else:
            raise ValueError(
                "ValueError: Blackframe Detection disabled.")

        video_width, video_height = video.size
        self.size = video.size

        if low_quality:
            def timecode_frame(time):
                """
                Adds a timecode.
                """
                timecode_image = Image.new('RGB', (50, 25))
                draw = ImageDraw.Draw(timecode_image)
                draw.text((0, 0), "%.02f"%(time))
                return PIL_to_npimage(timecode_image)

            timecode = mpy.VideoClip(
                timecode_frame,
                duration=video.duration)
            timecode = timecode.set_position((
                'right',
                'top'))

        if self.backdrop is not None:
            backdrop = Image.open(self.backdrop).resize(
                (video_width, video_height))
            if self.logo is not None:
                logo = Image.open(self.logo).resize(
                    (self.logo_width, self.logo_height))
                backdrop.paste(
                    logo,
                    (
                        backdrop.width-logo.width,
                        backdrop.height-logo.height),
                    logo)
        else:
            backdrop = Image.new(
                'RGBA',
                (video_width, video_height),
                (0, 0, 0))
            if self.logo is not None:
                logo = Image.open(self.logo).resize(
                    (self.logo_width, self.logo_height))
                backdrop.paste(
                    logo,
                    (
                        backdrop.width-logo.width,
                        backdrop.height-logo.height),
                    logo)

        backdrop_clip = mpy.ImageClip(PIL_to_npimage(backdrop))
        title = mpy.ImageClip(Title(self).to_frame()).set_duration(
            5).set_position(('center', 'center'))

        intro = mpy.CompositeVideoClip(
            [backdrop_clip, title],
            use_bgclip=True).set_duration(5)

        standing = GTStandings(
            self,
            process_data=process_data,
            ups=ups)
        standing_mask = GTStandings(
            self,
            mask=True,
            process_data=process_data,
            ups=ups)

        standing_clip = UpdatedVideoClip(
            standing)
        standing_clip = standing_clip.set_position(
            (0, 0)).set_duration(video.duration)

        standing_clip_mask = UpdatedVideoClip(
            standing_mask,
            ismask=True)
        """
        standing_clip_mask = standing_clip_mask.set_position(
            (0, 0)).set_duration(video.duration)
        """
        standing_clip = standing_clip.set_mask(standing_clip_mask)

        if low_quality:
            mainevent = mpy.CompositeVideoClip(
                [video, standing_clip, timecode],
                use_bgclip=False).set_duration(video.duration)
        else:
            mainevent = mpy.CompositeVideoClip(
                [video, standing_clip],
                use_bgclip=False).set_duration(video.duration)

        start_time = 0
        screen_duration = 20
        result = list()

        if len(self.car_classes):
            for index, car_class in enumerate(sorted(self.car_classes)):
                new_result = mpy.ImageClip(Results(
                    self,
                    self.result_lines,
                    car_class).to_frame())
                new_result = new_result.set_start(start_time)
                new_result = new_result.set_duration(screen_duration)
                new_result = new_result.set_position((
                    'center',
                    'center'))
                new_result = new_result.add_mask()
                start_time += screen_duration

                if index != 0:
                    new_result.mask = new_result.mask.fx(
                        vfx.fadein,
                        1)
                    result[index-1].mask = result[index-1].mask.fx(
                        vfx.fadeout,
                        1)

                result.append(new_result)
        else:
            new_result = mpy.ImageClip(Results(
                self,
                self.result_lines).to_frame())
            new_result = new_result.set_start(start_time)
            new_result = new_result.set_duration(screen_duration)
            new_result = new_result.set_position((
                'center',
                'center'))
            new_result = new_result.add_mask()
            start_time += screen_duration

            result.append(new_result)

        if self.point_structure is not None:
            series_standings = list()
            if len(self.car_classes):
                for index, car_class in enumerate(
                        sorted(self.car_classes)):
                    new_standing = mpy.ImageClip(SeriesStandings(
                        self,
                        self.result_lines,
                        car_class).to_frame())
                    new_standing = new_standing.set_start(start_time)
                    new_standing = new_standing.set_duration(
                        screen_duration)
                    new_standing = new_standing.set_position((
                        'center',
                        'center'))
                    new_standing = new_standing.add_mask()
                    start_time += screen_duration

                    if index != 0:
                        new_standing.mask = new_standing.mask.fx(
                            vfx.fadein,
                            1)
                        series_standings[index-1].mask = \
                            series_standings[index-1].mask.fx(
                                vfx.fadeout,
                                1)

                    series_standings.append(new_standing)
            else:
                new_standing = mpy.ImageClip(SeriesStandings(
                    self,
                    self.result_lines).to_frame())
                new_standing = new_standing.set_start(start_time)
                new_standing = new_standing.set_duration(
                    screen_duration)
                new_standing = new_standing.set_position((
                    'center',
                    'center'))
                new_standing = new_standing.add_mask()
                start_time += screen_duration

                series_standings.append(new_standing)

            result[-1].mask = result[-1].mask.fx(vfx.fadeout, 1)
            series_standings[0].mask = series_standings[0].mask.fx(
                vfx.fadein, 1)

            if self.show_champion:
                champion = list()
                if len(self.car_classes):
                    for index, car_class in enumerate(
                            sorted(self.car_classes)):
                        new_champion = mpy.ImageClip(Champion(
                            self,
                            car_class).to_frame())
                        new_champion = new_champion.set_start(
                            start_time)
                        new_champion = new_champion.set_duration(
                            screen_duration)
                        new_champion = new_champion.set_position((
                            'center',
                            'center'))
                        new_champion = new_champion.add_mask()
                        start_time += screen_duration

                        if index != 0:
                            new_champion.mask = new_champion.mask.fx(
                                vfx.fadein,
                                1)
                            champion[index-1].mask = \
                                series_standings[index-1].mask.fx(
                                    vfx.fadeout,
                                    1)

                        champion.append(new_champion)
                else:
                    new_champion = mpy.ImageClip(Champion(
                        self).to_frame())
                    new_champion = new_champion.set_start(start_time)
                    new_champion = new_champion.set_duration(
                        screen_duration)
                    new_champion = new_champion.set_position((
                        'center',
                        'center'))
                    new_champion = new_champion.add_mask()
                    start_time += screen_duration

                    champion.append(new_champion)

                series_standings[-1].mask = \
                    series_standings[-1].mask.fx(
                        vfx.fadeout, 1)
                champion[0].mask = champion[0].mask.fx(
                    vfx.fadein, 1)
        else:
            if self.show_champion:
                champion = list()
                if len(self.car_classes):
                    for index, car_class in enumerate(
                            sorted(self.car_classes)):
                        new_champion = mpy.ImageClip(Champion(
                            self,
                            car_class).to_frame())
                        new_champion = new_champion.set_start(
                            start_time)
                        new_champion = new_champion.set_duration(
                            screen_duration)
                        new_champion = new_champion.set_position((
                            'center',
                            'center'))
                        new_champion = new_champion.add_mask()
                        start_time += screen_duration

                        if index != 0:
                            new_champion.mask = new_champion.mask.fx(
                                vfx.fadein,
                                1)
                            champion[index-1].mask = series_standings\
                                [index-1].mask.fx(
                                    vfx.fadeout,
                                    1)

                        champion.append(new_champion)
                else:
                    new_champion = mpy.ImageClip(Champion(
                        self).to_frame())
                    new_champion = new_champion.set_start(start_time)
                    new_champion = new_champion.set_duration(
                        screen_duration)
                    new_champion = new_champion.set_position((
                        'center',
                        'center'))
                    new_champion = new_champion.add_mask()
                    start_time += screen_duration

                    champion.append(new_champion)

                champion[0].mask = champion[0].mask.fx(
                    vfx.fadein, 1)

        outro_videos = [backdrop_clip] + result
        if self.point_structure is not None:
            outro_videos.extend(series_standings)
        if self.show_champion:
            outro_videos.extend(champion)

        outro = mpy.CompositeVideoClip(
            outro_videos,
            use_bgclip=True).set_duration(
                sum([x.duration for x in outro_videos[1:]])).fx(
                    vfx.fadein, 1)

        output = mpy.concatenate_videoclips([
            intro, mainevent, outro])
        output = output.set_fps(ups)
        return output

    def build_default_video(self, process_data):
        """
        Builds a video with the default settings.
        """
        if self.source_video is None:
            video = mpy.ColorClip(
                (1280, 720),
                duration=self.telemetry_data[-1][0][-1][-1])
        elif isinstance(self.video_skipstart, float) \
                or isinstance(self.video_skipend, float):
            video = mpy.VideoFileClip(
                self.source_video).subclip(
                    self.video_skipstart, self.video_skipend)
        else:
            raise ValueError(
                "ValueError: Blackframe Detection disabled.")

        video_width, video_height = video.size

        if self.backdrop is not None:
            backdrop = Image.open(self.backdrop).resize(
                (video_width, video_height))
            if self.logo is not None:
                logo = Image.open(self.logo).resize(
                    (self.logo_width, self.logo_height))
                backdrop.paste(
                    logo,
                    (
                        backdrop.width-logo.width,
                        backdrop.height-logo.height),
                    logo)
        else:
            backdrop = Image.new(
                'RGBA',
                (video_width, video_height),
                (0, 0, 0))
            if self.logo is not None:
                logo = Image.open(self.logo).resize(
                    (self.logo_width, self.logo_height))
                backdrop.paste(
                    logo,
                    (
                        backdrop.width-logo.width,
                        backdrop.height-logo.height),
                    logo)

        backdrop_clip = mpy.ImageClip(PIL_to_npimage(backdrop))
        title = mpy.ImageClip(Title(self).to_frame()).set_duration(
            5).set_position(('center', 'center'))

        standing = UpdatedVideoClip(Standings(
            self,
            process_data=process_data))
        standing = standing.set_position(
            (self.margin, self.margin)).set_duration(video.duration)
        standing_mask = mpy.ImageClip(
            Standings(
                self,
                process_data=process_data).make_mask(),
            ismask=True, duration=video.duration)
        standing = standing.set_mask(standing_mask)

        timer = UpdatedVideoClip(
            Timer(self, process_data=process_data))
        timer_width, _ = timer.size
        timer = timer.set_position(
            (video_width-timer_width-self.margin, self.margin)
            ).set_duration(video.duration)
        timer_mask = mpy.ImageClip(
            Timer(self, process_data=process_data).make_mask(),
            ismask=True,
            duration=video.duration)
        timer = timer.set_mask(timer_mask)

        result = mpy.ImageClip(
            Results(self).to_frame()).set_duration(
                20).set_position(('center', 'center')).add_mask()

        if self.point_structure is not None:
            result.mask = result.mask.fx(vfx.fadeout, 1)
            series_standings = mpy.ImageClip(
                SeriesStandings(self).to_frame()).set_start(
                    20).set_duration(20).set_position(
                        ('center', 'center')).add_mask()

            if self.show_champion:
                series_standings.mask = series_standings.mask.fx(
                    vfx.fadein, 1).fx(vfx.fadeout, 1)
                champion = mpy.ImageClip(
                    Champion(self).to_frame()).set_start(
                        40).set_duration(20).set_position(
                            ('center', 'center')).add_mask()
                champion.mask = champion.mask.fx(vfx.fadein, 1)
            else:
                series_standings.mask = series_standings.mask.fx(
                    vfx.fadein, 1)
        else:
            if self.show_champion:
                result.mask = result.mask.fx(vfx.fadeout, 1)
                champion = mpy.ImageClip(
                    Champion(self).to_frame()).set_start(
                        20).set_duration(20).set_position(
                            ('center', 'center')).add_mask()
                champion.mask = champion.mask.fx(vfx.fadein, 1)


        intro = mpy.CompositeVideoClip(
            [backdrop_clip, title]).set_duration(5).fx(vfx.fadeout, 1)
        mainevent = mpy.CompositeVideoClip(
            [video, standing, timer]).set_duration(video.duration)

        outro_videos = [backdrop_clip, result]
        if self.point_structure is not None:
            outro_videos.append(series_standings)
        if self.show_champion:
            outro_videos.append(champion)

        outro = mpy.CompositeVideoClip(outro_videos).set_duration(
            sum([x.duration for x in outro_videos[1:]])).fx(
                vfx.fadein, 1)

        output = mpy.concatenate_videoclips([intro, mainevent, outro])
        return output

if __name__ == "__main__":
    try:
        PARSER = argparse.ArgumentParser(
            description="Project CARS Replay Enhancer")
        PARSER.add_argument(
            '-v',
            '--version',
            action='version',
            version='Version 0.3')
        PARSER.add_argument('configuration', nargs='?')
        PARSER.add_argument(
            '-c',
            '--configure',
            action='store_true',
            help='create or edit configuration file')
        PARSER.add_argument(
            '-u',
            '--custom',
            action='store_true',
            help=argparse.SUPPRESS)
        PARSER.add_argument(
            '-r',
            '--racestart',
            action='store_true',
            help='modify race start for telemetry sync')
        PARSER.add_argument(
            '-t',
            '--trim',
            action='store_true',
            help='modify video trim parameters')

        ARGS = PARSER.parse_args()

        ERR_MSG = ""
        if ARGS.racestart is True and \
                ARGS.configuration is None:
            ERR_MSG += \
                "\n-r, --racestart requires a provided configuration \
                file."
        if ARGS.trim is True and ARGS.configuration is None:
            ERR_MSG += "\n-t, --trim requires a provided \
                configuration file."

        if len(ERR_MSG):
            PARSER.error(ERR_MSG)

        if ARGS.custom is True:
            try:
                ReplayEnhancer.create_custom(ARGS.configuration)
            except FileNotFoundError:
                PARSER.error("\n{} not found. Aborting.".format(
                    ARGS.configuration))
        elif ARGS.configure is True:
            if ARGS.configuration is None:
                ReplayEnhancer.new_configuration()
            else:
                try:
                    ReplayEnhancer.edit_configuration(
                        ARGS.configuration)
                except FileNotFoundError:
                    PARSER.error("\n{} not found. Aborting.".format(
                        ARGS.configuration))
        elif ARGS.trim is True:
            try:
                ReplayEnhancer.edit_trim(ARGS.configuration)
            except FileNotFoundError:
                PARSER.error("\n{} not found. Aborting.".format(
                    ARGS.configuration))
        elif ARGS.racestart is True:
            try:
                ReplayEnhancer.edit_racestart(ARGS.configuration)
            except FileNotFoundError:
                PARSER.error("\n{} not found. Aborting.".format(
                    ARGS.configuration))
        else:
            if ARGS.configuration is None:
                ReplayEnhancer.new_configuration()
            else:
                try:
                    ReplayEnhancer.create_video(ARGS.configuration)
                except FileNotFoundError:
                    PARSER.error("\n{} not found. Aborting.".format(
                        ARGS.configuration))
    except KeyboardInterrupt:
        print("Aborting Project CARS Replay Enhancer.")
        raise
