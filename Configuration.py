"""
Provides the Configuration object for creating and modifying
configuration files for the Project CARS Replay Enhancer.
"""

from collections import OrderedDict
import csv
import re
import os
import json
from glob import glob
from struct import unpack

import moviepy.editor as mpy
from natsort import natsorted
from tqdm import tqdm

class Configuration:
    """
    Creates a Configuration that is written to a JSON file for the
    Project CARS Replay Enhancer
    """

    def __init__(self, previous_file=None):
        self.font = None
        self.font_size = None
        self.heading_font = None
        self.heading_font_size = None
        self.heading_color = None

        self.backdrop = None
        self.logo = None
        self.logo_height = None
        self.logo_width = None
        self.series_logo = None

        self.show_champion = None

        self.heading_text = None
        self.subheading_text = None

        self.margin = None
        self.column_margin = None

        self.source_video = None
        self.source_telemetry = None
        self.telemetry_file = None
        self.output_video = None

        self.car_data = None
        self.team_data = None
        self.points = None

        self.point_structure = None

        self.video_threshold = None
        self.video_gaptime = None
        self.video_skipstart = None
        self.video_skipend = None
        self.video_cache = None

        self.sync_racestart = None

        self.participant_config = None

        self.participants = dict()
        self.participant_lookup = dict()
        self.participant_configurations = list()

        self.previous_file = previous_file
        if previous_file:
            self.config_file = os.path.realpath(previous_file)
            self.__load_configuration(previous_file)

    def new_configuration(self):
        """
        Creates or edits a configuration.
        If parent object hasa previous file set, that previous file
        is used for the defaults.
        """
        previous_file = self.previous_file

        print("Creating configuration file.")
        print("Press CTRL+C at any time to abort.")

        try:
            if self.sync_racestart is None:
                self.sync_racestart = 0.0

            while True:
                print("Enter destination file for configuration.")
                print(".json file extension will be added",
                      "automatically.")
                print("CAUTION: Existing file contents will be",
                      "overwritten.")
                prompt = "({})".format(self.config_file) \
                    if previous_file else ""
                config_file = input(prompt+"--> ")

                if len(config_file) == 0 and previous_file:
                    break
                elif os.path.isdir(os.path.split(
                        os.path.realpath(config_file))[0]):
                    self.config_file = config_file+".json"
                    break
                else:
                    print("Configuration file location invalid.",
                          "Please try again.")
                    print("Directories must be created before",
                          "running script.")

            while True:
                print("Enter source video file.")
                print("Enter -1 for no file. Video will be rendered",
                      "on a transparent background.")
                prompt = "({})".format(self.source_video) \
                    if previous_file else ""
                source_video = input(prompt+"--> ")

                if len(source_video) == 0 and previous_file:
                    break
                if source_video == "-1":
                    self.source_video = None
                    break
                elif os.path.isfile(os.path.realpath(source_video)):
                    self.source_video = source_video
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Enter source telemetry directory.")
                prompt = "({})".format(self.source_telemetry) \
                    if previous_file else ""
                source_telemetry = input(prompt+"--> ")

                if len(source_telemetry) == 0 and previous_file:
                    break
                elif os.path.isdir(os.path.realpath(source_telemetry)):
                    if source_telemetry[-1] != os.sep:
                        self.source_telemetry = source_telemetry+os.sep
                    else:
                        self.source_telemetry = source_telemetry
                    break
                else:
                    print("Not a directory. Please try again.")

            while True:
                print("Enter output video file.")
                prompt = "({})".format(self.output_video) \
                    if previous_file else ""
                output_video = input(prompt+"--> ")

                if len(output_video) == 0 and previous_file:
                    break
                elif os.path.isdir(os.path.split(
                        os.path.realpath(output_video))[0]):
                    self.output_video = output_video
                    break
                else:
                    print("Configuration file location invalid.",
                          "Please try again.")
                    print("Directories must be created before",
                          "running script.")

            while True:
                print("Enter path to font.")
                prompt = "({})".format(self.font) \
                    if previous_file else ""
                font = input(prompt+"--> ")

                if len(font) == 0 and previous_file:
                    break
                elif os.path.isfile(os.path.realpath(font)):
                    self.font = font
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Enter size of font.")
                prompt = "({})".format(self.font_size) \
                    if previous_file else "15"
                font_size = input(prompt+"--> ")

                if len(font_size) == 0 and previous_file:
                    break
                elif len(font_size) == 0:
                    self.font_size = 15
                    break
                elif len(font_size) != 0:
                    try:
                        self.font_size = int(font_size)
                    except ValueError:
                        print("Font size should be an integer value.")
                    else:
                        break

            while True:
                print("Enter path to heading font.")
                prompt = "({})".format(self.heading_font) \
                    if previous_file else ""
                heading_font = input(prompt+"--> ")

                if len(heading_font) == 0 and previous_file:
                    break
                elif os.path.isfile(os.path.realpath(heading_font)):
                    self.heading_font = heading_font
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Enter size of heading font.")
                prompt = "({})".format(self.heading_font_size) \
                    if previous_file else str(int(self.font_size/0.75))
                heading_font_size = input(prompt+"--> ")

                if len(heading_font_size) == 0 and previous_file:
                    break
                elif len(heading_font_size) == 0:
                    self.heading_font_size = int(self.font_size/0.75)
                    break
                elif len(heading_font_size) != 0:
                    try:
                        self.heading_font_size = int(heading_font_size)
                    except ValueError:
                        print("Heading font size should be an integer",
                              "value.")
                    else:
                        break

            while True:
                print("Enter margin width.")
                prompt = "({})".format(self.margin) \
                    if previous_file else str(self.heading_font_size)
                margin = input(prompt+"--> ")

                if len(margin) == 0 and previous_file:
                    break
                elif len(margin) == 0:
                    self.margin = self.heading_font_size
                    break
                elif len(margin) != 0:
                    try:
                        self.margin = int(margin)
                    except ValueError:
                        print("Margin width should be an integer value")
                    else:
                        break

            while True:
                print("Enter column margin width.")
                prompt = "({})".format(self.column_margin) \
                    if previous_file else str(int(self.margin/2))
                column_margin = input(prompt+"--> ")

                if len(column_margin) == 0 and previous_file:
                    break
                elif len(column_margin) == 0:
                    self.column_margin = int(self.margin/2)
                    break
                elif len(column_margin) != 0:
                    try:
                        self.column_margin = int(column_margin)
                    except ValueError:
                        print("Column margin width should be an",
                              "integer value.")
                    else:
                        break

            purge_cache = False
            use_blackframe = False
            """
            Removing blackframe detection for the time being.
            It's too slow, there are too many problems with it, and
            it's too arcane for the average user.

            Until it can be better automated and faster, it's gone.
            """

            '''
            while True:
                print("Use blackframe detection to crop video?")
                print("Choose YES (default) to trim video based on",
                      "fade-through-blacks present in most Project",
                      "CARS replays.")
                print("Choose NO to manually enter, in seconds, the",
                      "start and stop time of the video.")
                use_blackframe = input("[Y/n]--> ")
                if len(use_blackframe) == 0 or \
                        str.lower(use_blackframe) == 'y':
                    use_blackframe = True
                    break
                elif str.lower(use_blackframe) == 'n':
                    use_blackframe = False
                    break
            '''
            if self.source_video is not None:
                if use_blackframe:
                    while True:
                        print("Enter blackframe detection threshold.")
                        print("This sets how dark the screen must be to",
                              "be recognized as a fade.")
                        prompt = "({})".format(self.video_threshold) \
                            if previous_file else "1"
                        video_threshold = input(prompt+"--> ")

                        if len(video_threshold) == 0 and previous_file:
                            break
                        elif len(video_threshold) == 0:
                            self.video_threshold = 1
                            purge_cache = True
                            break
                        elif len(video_threshold) != 0:
                            try:
                                self.video_threshold = int(video_threshold)
                                purge_cache = True
                            except ValueError:
                                print("Blackframe detection threshold",
                                      "should be an integer value.")
                            else:
                                break

                    while True:
                        print("Enter blackframe gap time.")
                        print("This sets the minimum time between",
                              "blackframes to be considered separate",
                              "events")
                        prompt = "({})".format(self.video_gaptime) \
                            if previous_file else "1"
                        video_gaptime = input(prompt+"--> ")

                        if len(video_gaptime) == 0 and previous_file:
                            break
                        elif len(video_gaptime) == 0:
                            self.video_gaptime = 1
                            purge_cache = True
                            break
                        elif len(video_gaptime):
                            try:
                                self.video_gaptime = int(video_gaptime)
                                purge_cache = True
                            except ValueError:
                                print("Blackframe gap time should be an",
                                      "integer value.")
                            else:
                                break

                while True:
                    if use_blackframe:
                        print("Enter number of scenes to skip at the",
                              "start of the video.")
                    else:
                        print("Enter the start time of the video.")

                    duration = mpy.VideoFileClip(self.source_video).duration
                    prompt = "({})".format(self.video_skipstart \
                        if previous_file else "1" if use_blackframe \
                                         else "0.0")
                    video_skipstart = input(prompt+"--> ")

                    if len(video_skipstart) == 0 and previous_file:
                        if self.video_skipstart < 0.0:
                            print("Start time should be greater than",
                                  "or equal to zero and less than the",
                                  "video duration of {}.".format(duration))
                        elif self.video_skipstart <= duration:
                            break
                        else:
                            print("Start time should be greater than",
                                  "or equal to zero and less than the",
                                  "video duration of {}.".format(duration))
                    elif len(video_skipstart) == 0:
                        self.video_skipstart = 1 if use_blackframe else 0.0
                        purge_cache = True
                        self.sync_racestart = 0.0
                        break
                    elif len(video_skipstart) != 0 and use_blackframe:
                        try:
                            self.video_skipstart = int(video_skipstart)
                            purge_cache = True
                            self.sync_racestart = 0.0
                            break
                        except ValueError:
                            print("Number of scenes to skip should be an",
                                  "integer value.")
                    elif len(video_skipstart) != 0 and not use_blackframe:
                        try:
                            video_skipstart = float(video_skipstart)
                            if video_skipstart < 0.0:
                                raise ValueError
                            elif video_skipstart <= duration:
                                self.video_skipstart = \
                                    float(video_skipstart)
                                purge_cache = True
                                self.sync_racestart = 0.0
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("End time should be greater than zero",
                                  "and less than the",
                                  "video duration of {}.".format(duration))

                while True:
                    if use_blackframe:
                        print("Enter number of scenes to skip at the",
                              "end of the video.")
                    else:
                        print("Enter the ending time of the video.")

                    duration = mpy.VideoFileClip(self.source_video).duration
                    prompt = "({})".format(self.video_skipend \
                        if previous_file else "1" if use_blackframe \
                                         else str(duration))
                    video_skipend = input(prompt+"--> ")

                    if len(video_skipend) == 0 and previous_file:
                        if self.video_skipend <= self.video_skipstart:
                            break
                        elif self.video_skipend <= duration:
                            break
                        else:
                            print("End time should be greater than the",
                                  "start time and less than the",
                                  "video duration of {}.".format(duration))
                    elif len(video_skipend) == 0:
                        self.video_skipend = 1 if use_blackframe \
                            else duration
                        purge_cache = True
                        break
                    elif len(video_skipend) != 0 and use_blackframe:
                        try:
                            self.video_skipend = int(video_skipend)
                            purge_cache = True
                            break
                        except ValueError:
                            print("Number of scenes to skip should be an",
                                  "integer value.")
                    elif len(video_skipend) != 0 and not use_blackframe:
                        try:
                            video_skipend = float(video_skipend)
                            if video_skipend <= self.video_skipstart:
                                raise ValueError
                            elif video_skipend <= duration:
                                self.video_skipend = float(video_skipend)
                                purge_cache = True
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("End time should be greater than the",
                                  "start time and less than the",
                                  "video duration of {}.".format(duration))

                '''
                while True:
                    print("Enter file to use as a cache for video data.")
                    prompt = "({})".format(self.video_cache \
                        if previous_file else "file.cache")
                    video_cache = input(prompt+"--> ")

                    if len(video_cache) == 0 and previous_file:
                        break
                    elif os.path.isdir(os.path.realpath(video_cache)):
                        try:
                            if video_cache[-1] != os.sep:
                                video_cache += os.sep
                        except IndexError:
                            video_cache = os.path.realpath(os.curdir)+os.sep
                        video_cache += "file.cache"
                        self.video_cache = video_cache
                        purge_cache = True
                        break
                    elif os.path.isdir(os.path.split(os.path.realpath(
                            video_cache))[0]):
                        self.video_cache = video_cache
                        purge_cache = True
                        break
                    else:
                        print("Location invalid. Please try again.")
                        print("Directories must be created before",
                              "running script.")
                '''

            #TODO: Move to module-specific configuration
            while True:
                print("Enter heading color.")
                print("Color should be entered as three integers,",
                      "separated by commas, representing Red, Green,",
                      "and Blue values.")
                prompt = "({}, {}, {})".format(*self.heading_color) \
                    if previous_file else ""
                heading_color = input(prompt+"--> ")

                if len(heading_color) == 0 and previous_file:
                    break
                else:
                    try:
                        heading_color = [int(x) \
                            for x in heading_color.split(',')]
                        if all([x >= 0 and x <= 255 \
                                for x in heading_color]):
                            self.heading_color = heading_color
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("Invalid color value.")

            while True:
                print("Enter background for title and results",
                      "screens.")
                print("Enter -1 for none.")
                prompt = "({})".format(self.backdrop) \
                    if previous_file else ""
                backdrop = input(prompt+"--> ")

                if len(backdrop) == 0 and previous_file:
                    break
                elif backdrop == "-1":
                    self.backdrop = ""
                    break
                elif os.path.isfile(os.path.realpath(backdrop)):
                    self.backdrop = backdrop
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Enter logo for title and results",
                      "screens.")
                print("Enter -1 for none.")
                prompt = "({})".format(self.logo) \
                    if previous_file else ""
                logo = input(prompt+"--> ")

                if len(logo) == 0 and previous_file:
                    break
                elif logo == "-1":
                    self.logo = ""
                    break
                elif os.path.isfile(os.path.realpath(logo)):
                    self.logo = logo
                    break
                else:
                    print("Not a file. Please try again.")

            if len(self.logo):
                while True:
                    print("Enter height for logo.")
                    prompt = "({})".format(self.logo_height \
                        if previous_file else "150")
                    logo_height = input(prompt+"--> ")

                    if len(logo_height) == 0 and previous_file:
                        break
                    elif len(logo_height) == 0:
                        self.logo_height = 150
                        break
                    elif len(logo_height) != 0:
                        try:
                            self.logo_height = int(logo_height)
                        except ValueError:
                            print("Logo height should be an integer",
                                  "value.")
                        else:
                            break

                while True:
                    print("Enter width for logo.")
                    prompt = "({})".format(self.logo_width \
                        if previous_file else str(self.logo_height))
                    logo_width = input(prompt+"--> ")

                    if len(logo_width) == 0 and previous_file:
                        break
                    elif len(logo_width) == 0:
                        self.logo_width = self.logo_height
                        break
                    elif len(logo_width) != 0:
                        try:
                            self.logo_width = int(logo_width)
                        except ValueError:
                            print("Logo width should be an integer",
                                  "value.")
                        else:
                            break
            else:
                self.logo_height = 0
                self.logo_width = 0

            while True:
                print("Enter a series logo for title and results",
                      "screens.")
                print("Enter -1 for none.")
                prompt = "({})".format(self.series_logo) \
                    if previous_file else ""
                series_logo = input(prompt+"--> ")

                if len(series_logo) == 0 and previous_file:
                    break
                elif series_logo == "-1":
                    self.series_logo = ""
                    break
                elif os.path.isfile(os.path.realpath(series_logo)):
                    self.series_logo = series_logo
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Show series champion screen?")
                prompt = "[y/N]"
                show_champion = input(prompt+"--> ")

                if len(show_champion) == 0 or \
                     str.lower(show_champion) == 'n':
                    self.show_champion = False
                    break
                elif str.lower(show_champion) == 'y':
                    self.show_champion = True
                    break

            while True:
                print("Enter main heading text.")
                print("Enter -1 for none.")
                prompt = "({})".format(self.heading_text) \
                    if previous_file else ""
                heading_text = input(prompt+"--> ")

                if len(heading_text) == 0 and previous_file:
                    break
                elif heading_text == "-1":
                    self.heading_text = ""
                    break
                elif len(heading_text):
                    self.heading_text = heading_text
                    break

            while True:
                print("Enter subheading text.")
                print("Enter -1 for none.")
                prompt = "({})".format(self.subheading_text) \
                    if previous_file else ""
                subheading_text = input(prompt+"--> ")

                if len(subheading_text) == 0 and previous_file:
                    break
                elif subheading_text == "-1":
                    self.subheading_text = ""
                    break
                elif len(subheading_text):
                    self.subheading_text = subheading_text
                    break

            point_structure = [0]
            while True:
                position = len(point_structure)
                print("Enter points scored for finish position",
                      "{}".format(position))
                if position == 1:
                    print("Enter 0 to disable points for this race")
                else:
                    print("Enter 0 to finish points structure.")

                if previous_file:
                    print("Enter -1 to use previous values for",
                          "remaining positions.")
                try:
                    prompt = "({})".format(str(
                        self.point_structure[position])) \
                        if previous_file else "0"
                except IndexError:
                    prompt = "(0)"
                except TypeError:
                    prompt = "(0)"

                new_point = input(prompt+"--> ")
                if new_point == "0":
                    break
                elif new_point == "-1" and previous_file:
                    point_structure = self.__finish_array(
                        point_structure, self.point_structure)
                    break
                elif new_point == "-1":
                    print("Point values should be greater than"
                          "zero.")
                elif len(new_point) == 0 and previous_file:
                    try:
                        if self.point_structure is None:
                            break
                        elif self.point_structure[position] == 0:
                            break
                        else:
                            point_structure.append(
                                int(self.point_structure[position]))
                    except IndexError:
                        print("No previous value for this position.",
                              "Enter 0 to end points structure.")
                elif len(new_point) == 0:
                    break
                else:
                    try:
                        point_structure.append(int(new_point))
                    except ValueError:
                        print("Points should be integer values.")

            if len(point_structure) > 1:
                while True:
                    print("Enter bonus points for fastest lap.")
                    prompt = "({})".format(str(
                        self.point_structure[0]) \
                        if previous_file else "0")
                    bonus_point = input(prompt+"--> ")

                    if len(bonus_point) == 0 and previous_file:
                        point_structure[0] = int(self.point_structure[0])
                        break
                    elif len(bonus_point) == 0:
                        point_structure[0] = int(0)
                        break
                    else:
                        try:
                            point_structure[0] = int(bonus_point)
                            break
                        except ValueError:
                            print("Points should be integer values.")

                self.point_structure = point_structure
            else:
                self.point_structure = None

            print("Parsing telemetry data for driver information.")
            print("Please wait...")

            self.__get_participants(self.source_telemetry, "tele.csv")

            last_car = None
            last_team = None
            last_points = 0
            use_last_car = False
            use_last_team = False
            use_last_points = False

            if self.point_structure is None:
                last_points = None
                use_last_points = True

            while True:
                print("Include team data for drivers?")
                prompt = "[Y/n]"
                show_team = input(prompt+"--> ")

                if len(show_team) == 0 or \
                        str.lower(show_team) == 'y':
                    break
                elif str.lower(show_team) == 'n':
                    last_team = ""
                    use_last_team = True
                    break

            if previous_file:
                self.participant_config = {k:v \
                    for k, v in self.participant_config.items() \
                    if k in self.participants}
            if not previous_file:
                self.participant_config = dict()

            for participant in sorted(
                    self.participants,
                    key=lambda x: str(x).lower()):
                print("Entering data for {}.".format(participant))
                if participant not in self.participant_config.keys():
                    self.participant_config[participant] = {
                        'display': None,
                        'car': None,
                        'team': None,
                        'points': None,
                        'short_display': None}

                while True:
                    print("Enter display name override for",
                          "{}.".format(participant))
                    if self.participant_config[participant]['display'] \
                            is not None:
                        prompt = "({})".format(
                            self.participant_config[participant]\
                                ['display'])
                    else:
                        prompt = "({})".format(participant)
                    display_name = input(prompt+"--> ")

                    if len(display_name) == 0 and \
                            previous_file and \
                            self.participant_config[participant]\
                                ['display'] is not None:
                        break
                    elif len(display_name) == 0:
                        self.participant_config[participant]\
                            ['display'] = participant
                        break
                    else:
                        self.participant_config[participant]\
                            ['display'] = display_name
                        break

                while True:
                    print("Enter abbreviated name override for",
                          "{}.".format(participant))
                    print("(Used by some modules for space saving.)")

                    if self.participant_config[participant]\
                            ['short_display'] is not None:
                        prompt = "({})".format(
                            self.participant_config[participant]\
                                ['short_display'])
                    else:
                        prompt = "({})".format(
                            self.participant_config[participant]\
                                ['display'].split(" ")[0][0] + \
                            ". " + \
                            self.participant_config[participant]\
                                ['display'].split(" ")[-1] \
                            if len(self.participant_config[participant]\
                                ['display'].split(" ")) > 1 \
                            else self.participant_config[participant]\
                                ['display'])
                    short_display_name = input(prompt+"--> ")

                    if len(short_display_name) == 0 and \
                            previous_file and \
                            self.participant_config[participant]\
                                ['short_display'] is not None:
                        break
                    elif len(short_display_name) == 0:
                        self.participant_config[participant]\
                            ['short_display'] = \
                        self.participant_config[participant]\
                            ['display'].split(" ")[0][0] + \
                        ". " + \
                        self.participant_config[participant]\
                            ['display'].split(" ")[-1] \
                        if len(self.participant_config[participant]\
                            ['display'].split(" ")) > 1 \
                        else self.participant_config[participant]\
                            ['display']
                        break
                    else:
                        self.participant_config[participant]\
                            ['short_display'] = short_display_name
                        break

                if use_last_car:
                    self.participant_config[participant]['car'] = \
                        last_car
                else:
                    while True:
                        print("Enter car for {}.".format(participant))
                        if last_car:
                            print("Enter -1 to use {}".format(
                                last_car),
                                  "for remaining drivers.")

                        if self.participant_config[participant]['car'] \
                                is not None:
                            prompt = "({})".format(
                                self.participant_config[participant]\
                                    ['car'])
                        else:
                            prompt = "({})".format(
                                last_car) if last_car else ""
                        car = input(prompt+"--> ")

                        if len(car) == 0 and \
                                previous_file and \
                                self.participant_config[participant]\
                                    ['car'] is not None:
                            break
                        elif len(car) == 0 and last_car:
                            self.participant_config[participant]\
                                ['car'] = last_car
                            break
                        elif car == "-1" and last_car:
                            self.participant_config[participant]\
                                ['car'] = last_car
                            use_last_car = True
                            break
                        elif len(car) != 0 and car != "-1":
                            last_car = car
                            self.participant_config[participant]\
                                ['car'] = last_car
                            break

                if use_last_team:
                    self.participant_config[participant]['team'] = \
                        last_team
                else:
                    while True:
                        print("Enter team for {}.".format(participant))
                        if last_team:
                            print("Enter -1 to use {}".format(
                                last_team),
                                  "for remaining drivers.")

                        if self.participant_config[participant]\
                                ['team'] is not None:
                            prompt = "({})".format(
                                self.participant_config[participant]\
                                    ['team'])
                        else:
                            prompt = "({})".format(
                                last_team if last_team else "")
                        team = input(prompt+"--> ")

                        if len(team) == 0 and \
                                previous_file and \
                                self.participant_config[participant]\
                                    ['team'] is not None:
                            break
                        elif len(team) == 0 and last_team:
                            self.participant_config[participant]\
                                ['team'] = last_team
                            break
                        elif team == "-1" and last_team:
                            self.participant_config[participant]\
                                ['team'] = last_team
                            use_last_team = True
                            break
                        elif len(team) != 0 and team != "-1":
                            last_team = team
                            self.participant_config[participant]\
                                ['team'] = last_team
                            break

                if use_last_points:
                    self.participant_config[participant]\
                        ['points'] = last_points
                else:
                    while True:
                        print("Enter previous series points for",
                              "{}.".format(participant))
                        print("Enter -1 to use {}".format(
                            last_points),
                              "for remaining drivers.")

                        if self.participant_config[participant]\
                            ['points'] is not None:
                            prompt = "({})".format(
                                self.participant_config[participant]\
                                    ['points'])
                        else:
                            prompt = "({})".format(
                                last_points)
                        points = input(prompt+"--> ")

                        if len(points) == 0 and \
                                previous_file and \
                                self.participant_config[participant]\
                                    ['points'] is not None:
                            break
                        elif len(points) == 0:
                            self.participant_config[participant]\
                                ['points'] = last_points
                            break
                        elif points == "-1":
                            self.participant_config[participant]\
                                ['points'] = last_points
                            use_last_points = True
                            break
                        elif len(points) != 0 and points != "-1":
                            try:
                                last_points = int(points)
                                self.participant_config[participant]\
                                    ['points'] = last_points
                                break
                            except ValueError:
                                print("Point values should be",
                                      "integers.")
        except KeyboardInterrupt:
            print("\n\nExiting. No configuration data written.")
            raise KeyboardInterrupt
        else:
            with open(os.path.realpath(self.config_file), 'w') \
                    as config_file:
                json.dump(self.__get_values(), config_file, indent=4)
            print("\n\nConfiguration data written to {}".format(
                self.config_file))

            '''
            if purge_cache:
                try:
                    with open(os.path.realpath(self.video_cache), 'r') \
                            as cache_file:
                        cache_data = cache_file.read()

                    matches = re.findall(
                        r"(^"+re.escape(
                            os.path.realpath(
                                self.source_video))+".*$)",
                        cache_data, re.M)
                    if len(matches):
                        for match in matches:
                            cache_data = cache_data.replace(match, "")

                    with open(
                        os.path.realpath(
                            self.video_cache), 'w') as cache_file:
                        cache_file.write(cache_data)
                except FileNotFoundError:
                    pass

                print("\n\nFile cache modified at {}".format(
                    self.video_cache))
            '''

    def modify_racestart(self):
        """
        Modifies the telemetry synchronization value in the
        configuraiton file. All other properties are left
        unchanged.
        """
        try:
            if self.previous_file is None:
                raise ValueError
            else:
                previous_file = self.previous_file

            print("Modifying synchronization offset value.")
            print("Press CTRL+C at any time to abort.")

            while True:
                print("Enter new synchronization offset value.")
                prompt = "({})".format(str(self.sync_racestart) \
                    if previous_file else "0.0")
                sync_racestart = input(prompt+"--> ")

                if len(sync_racestart) == 0 and previous_file:
                    break
                elif len(sync_racestart) == 0:
                    self.sync_racestart = 0.0
                    break
                elif len(sync_racestart):
                    try:
                        self.sync_racestart = float(sync_racestart)
                    except ValueError:
                        print("Race start should be a number.")
                    else:
                        break

        except KeyboardInterrupt:
            print("\n\nExiting. No configuration data written.")
            raise KeyboardInterrupt
        except ValueError:
            print("\n\nMust provide existing configuration file.")
        else:
            with open(os.path.realpath(self.config_file), 'w') \
                    as config_file:
                json.dump(self.__get_values(), config_file, indent=4)
            print("\n\nConfiguration data written to {}".format(
                self.config_file))

    def modify_trim(self):
        """
        Modifies the video trimming properties in the configuraiton
        file. Telemetry synchronization is reset to 0.0 if any value
        is changed. All other valuesare unchanged.
        """
        try:
            if self.previous_file is None:
                raise ValueError
            else:
                previous_file = self.previous_file

            print("Modifying video trim files.")
            print("If blackframe detection values or starting trim",
                  "value is changed, telemetry synchronization value",
                  "will be reset to 0.0")
            print("Press CTRL+C at any time to abort.")

            purge_cache = False
            use_blackframe = False
            '''
            while True:
                print("Use blackframe detection to crop video?")
                print("Choose YES (default) to trim video based on",
                      "fade-through-blacks present in most Project",
                      "CARS replays.")
                print("Choose NO to manually enter, in seconds, the",
                      "start and stop time of the video.")
                use_blackframe = input("[Y/n]--> ")
                if len(use_blackframe) == 0 or \
                        str.lower(use_blackframe) == 'y':
                    use_blackframe = True
                    break
                elif str.lower(use_blackframe) == 'n':
                    use_blackframe = False
                    break
            '''

            if self.source_video is not None:
                if use_blackframe:
                    while True:
                        print("Enter blackframe detection threshold.")
                        print("This sets how dark the screen must be to",
                              "be recognized as a fade.")
                        prompt = "({})".format(self.video_threshold) \
                            if previous_file else "1"
                        video_threshold = input(prompt+"--> ")

                        if len(video_threshold) == 0 and previous_file:
                            break
                        elif len(video_threshold) == 0:
                            self.video_threshold = 1
                            purge_cache = True
                            self.sync_racestart = 0.0
                            break
                        elif len(video_threshold) != 0:
                            try:
                                self.video_threshold = int(video_threshold)
                                purge_cache = True
                                self.sync_racestart = 0.0
                            except ValueError:
                                print("Blackframe detection threshold",
                                      "should be an integer value.")
                            else:
                                break

                    while True:
                        print("Enter blackframe gap time.")
                        print("This sets the minimum time between",
                              "blackframes to be considered separate",
                              "events")
                        prompt = "({})".format(self.video_gaptime) \
                            if previous_file else "1"
                        video_gaptime = input(prompt+"--> ")

                        if len(video_gaptime) == 0 and previous_file:
                            break
                        elif len(video_gaptime) == 0:
                            self.video_gaptime = 1
                            purge_cache = True
                            self.sync_racestart = 0.0
                            break
                        elif len(video_gaptime):
                            try:
                                self.video_gaptime = int(video_gaptime)
                                purge_cache = True
                                self.sync_racestart = 0.0
                            except ValueError:
                                print("Blackframe gap time should be an",
                                      "integer value.")
                            else:
                                break

                while True:
                    if use_blackframe:
                        print("Enter number of scenes to skip at the",
                              "start of the video.")
                    else:
                        print("Enter the start time of the video.")

                    duration = mpy.VideoFileClip(self.source_video).duration
                    prompt = "({})".format(self.video_skipstart \
                        if previous_file else "1" if use_blackframe \
                                         else "0.0")
                    video_skipstart = input(prompt+"--> ")

                    if len(video_skipstart) == 0 and previous_file:
                        if self.video_skipstart < 0.0:
                            print("Start time should be greater than",
                                  "or equal to zero and less than the",
                                  "video duration of {}.".format(duration))
                        elif self.video_skipstart <= duration:
                            break
                        else:
                            print("Start time should be greater than",
                                  "or equal to zero and less than the",
                                  "video duration of {}.".format(duration))
                    elif len(video_skipstart) == 0:
                        self.video_skipstart = 1 if use_blackframe else 0.0
                        purge_cache = True
                        self.sync_racestart = 0.0
                        break
                    elif len(video_skipstart) != 0 and use_blackframe:
                        try:
                            self.video_skipstart = int(video_skipstart)
                            purge_cache = True
                            self.sync_racestart = 0.0
                            break
                        except ValueError:
                            print("Number of scenes to skip should be an",
                                  "integer value.")
                    elif len(video_skipstart) != 0 and not use_blackframe:
                        try:
                            video_skipstart = float(video_skipstart)
                            if video_skipstart < 0.0:
                                raise ValueError
                            elif video_skipstart <= duration:
                                self.video_skipstart = float(
                                    video_skipstart)
                                purge_cache = True
                                self.sync_racestart = 0.0
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("End time should be greater than zero",
                                  "and less than the",
                                  "video duration of {}.".format(duration))

                while True:
                    if use_blackframe:
                        print("Enter number of scenes to skip at the",
                              "end of the video.")
                    else:
                        print("Enter the ending time of the video.")

                    duration = mpy.VideoFileClip(self.source_video).duration
                    prompt = "({})".format(self.video_skipend \
                        if previous_file else "1" if use_blackframe \
                                         else str(duration))
                    video_skipend = input(prompt+"--> ")

                    if len(video_skipend) == 0 and previous_file:
                        if self.video_skipend <= self.video_skipstart:
                            break
                        elif self.video_skipend <= duration:
                            break
                        else:
                            print("End time should be greater than the",
                                  "start time and less than the",
                                  "video duration of {}.".format(duration))

                    elif len(video_skipend) == 0:
                        self.video_skipend = 1 if use_blackframe \
                            else duration
                        purge_cache = True
                        break
                    elif len(video_skipend) != 0 and use_blackframe:
                        try:
                            self.video_skipend = int(video_skipend)
                            purge_cache = True
                            break
                        except ValueError:
                            print("Number of scenes to skip should be an",
                                  "integer value.")
                    elif len(video_skipend) != 0 and not use_blackframe:
                        try:
                            video_skipend = float(video_skipend)
                            if video_skipend <= self.video_skipstart:
                                raise ValueError
                            elif video_skipend <= duration:
                                self.video_skipend = float(video_skipend)
                                purge_cache = True
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("End time should be greater than the",
                                  "start time and less than the",
                                  "video duration of {}.".format(duration))

                '''
                while True:
                    print("Enter file to use as a cache for video data.")
                    prompt = "({})".format(self.video_cache \
                        if previous_file else "file.cache")
                    video_cache = input(prompt+"--> ")

                    if len(video_cache) == 0 and previous_file:
                        break
                    elif os.path.isdir(os.path.realpath(video_cache)):
                        try:
                            if video_cache[-1] != os.sep:
                                video_cache += os.sep
                        except IndexError:
                            video_cache = os.path.realpath(os.curdir)+os.sep
                        video_cache += "file.cache"
                        self.video_cache = video_cache
                        purge_cache = True
                        break
                    elif os.path.isdir(os.path.split(os.path.realpath(
                            video_cache))[0]):
                        self.video_cache = video_cache
                        purge_cache = True
                        break
                    else:
                        print("Location invalid. Please try again.")
                        print("Directories must be created before",
                              "running script.")
                '''

        except KeyboardInterrupt:
            print("\n\nExiting. No configuration data written.")
            raise KeyboardInterrupt
        except ValueError:
            print("\n\nMust provide existing configuration file.")
        else:
            with open(os.path.realpath(self.config_file), 'w') \
                    as config_file:
                json.dump(self.__get_values(), config_file, indent=4)
            print("\n\nConfiguration data written to {}".format(
                self.config_file))

            '''
            if purge_cache:
                try:
                    with open(
                        os.path.realpath(
                            self.video_cache),
                        'r') as cache_file:
                        cache_data = cache_file.read()

                    matches = re.findall(
                        r"(^"+re.escape(
                            os.path.realpath(
                                self.source_video))+".*$)",
                        cache_data,
                        re.M)
                    if len(matches):
                        for match in matches:
                            cache_data = cache_data.replace(match, "")

                    with open(
                        os.path.realpath(
                            self.video_cache),
                        'w') as cache_file:
                        cache_file.write(cache_data)
                except FileNotFoundError:
                    pass

                print("\n\nFile cache modified at",
                      "{}".format(self.video_cache))
            '''

    def __get_values(self):
        participant_config = OrderedDict(sorted(
            self.participant_config.items(),
            key=lambda x: x[0].lower()))

        for name, data in participant_config.items():
            participant_config[name] = OrderedDict(sorted(
                data.items(),
                key=lambda x: x[0].lower()))

        output = {'font': self.font,
                  'font_size': self.font_size,
                  'heading_font': self.heading_font,
                  'heading_font_size': self.heading_font_size,
                  'heading_color': self.heading_color,
                  'backdrop': self.backdrop,
                  'logo': self.logo,
                  'logo_height': self.logo_height,
                  'logo_width': self.logo_width,
                  'series_logo': self.series_logo,
                  'show_champion': self.show_champion,
                  'heading_text': self.heading_text,
                  'subheading_text': self.subheading_text,
                  'margin': self.margin,
                  'column_margin': self.column_margin,
                  'source_video': self.source_video,
                  'source_telemetry': self.source_telemetry,
                  'output_video': self.output_video,
                  'participant_config': participant_config,
                  'point_structure': self.point_structure,
                  'video_threshold': self.video_threshold,
                  'video_gaptime': self.video_gaptime,
                  'video_skipstart': self.video_skipstart,
                  'video_skipend': self.video_skipend,
                  'video_cache': self.video_cache,
                  'sync_racestart': self.sync_racestart}
        return OrderedDict(sorted(
            output.items(), 
            key=lambda x: x[0].lower()))

    @staticmethod
    def __process_telemetry(source_telemetry, telemetry_file):
        with open(source_telemetry+telemetry_file, 'w') as csvfile:
            with tqdm(
                desc="Processing:",
                total=len(glob(source_telemetry+'pdata*'))) \
                    as progress_bar:
                for tele_file in natsorted(
                        glob(source_telemetry+'pdata*')):
                    with open(tele_file, 'rb') as pack_file:
                        pack_data = pack_file.read()
                        if len(pack_data) == 1367:
                            pack_string = "HB"
                            pack_string += "B"
                            pack_string += "bb"
                            pack_string += "BBbBB"
                            pack_string += "B"
                            pack_string += "21f"
                            pack_string += "H"
                            pack_string += "B"
                            pack_string += "B"
                            pack_string += "hHhHHBBBBBbffHHBBbB"
                            pack_string += "22f"
                            pack_string += "8B12f8B8f12B4h20H16f4H"
                            pack_string += "2f"
                            pack_string += "2B"
                            pack_string += "bbBbbb"

                            pack_string += "hhhHBBBBf"*56

                            pack_string += "fBBB"

                        elif len(pack_data) == 1028:
                            pack_string = "HBB"

                            pack_string += "64s"*16

                        elif len(pack_data) == 1347:
                            pack_string = "HB64s64s64s64s"

                            pack_string += "64s"*16

                            pack_string += "64x"

                        csvfile.write(",".join(str(
                            x,
                            encoding='utf-8', errors='ignore').\
                            replace('\x00', '') \
                            if isinstance(x, bytes) \
                            else str(x).replace('\x00', '') \
                            for x in unpack(
                                pack_string, pack_data)+\
                                    (tele_file,))+"\n")
                        progress_bar.update()

    def __get_participants(self, source_telemetry, telemetry_file):
        try:
            tele_file = open(source_telemetry+telemetry_file, 'r')
        except FileNotFoundError:
            self.__process_telemetry(source_telemetry, telemetry_file)
            tele_file = open(source_telemetry+telemetry_file, 'r')
        finally:
            index = 0
            with open(source_telemetry+telemetry_file) as csv_file:
                for index, _ in enumerate(csv_file):
                    pass
            number_lines = index+1
            csvdata = csv.reader(tele_file)

        new_data = list()
        participants = 0
        self.participant_configurations = list()

        with tqdm(desc="Analyzing telemetry:", total=number_lines) \
                as progress_bar:
            for row in csvdata:
                if len(row) == 687 and int(row[4]) != -1:
                    participants = int(row[4])
                if len(row) == 687:
                    pass
                elif len(row) == 23:
                    for index, participant_name in enumerate(
                            row[6:6+min(16, participants)]):
                        if len(participant_name):
                            new_data.append(participant_name)
                elif len(row) == 20:
                    for index, participant_name in enumerate(
                            row[3:3+min(16, participants)],
                            int(row[2])):
                        if len(participant_name):
                            new_data.append(participant_name)
                else:
                    raise ValueError("ValueError: Unrecognized or",
                                     "malformed packet.")

                if participants > 0 and \
                        len(new_data) >= participants:
                    try:
                        if new_data != \
                                self.participant_configurations\
                                    [-1][:-1]:
                            self.participant_configurations.append(
                                new_data+[participants])
                    except IndexError:
                        self.participant_configurations.append(
                            new_data+[participants])
                    finally:
                        new_data = list()
                progress_bar.update()

        self.participant_lookup = {
            x: [x] for x in self.participant_configurations[0][:-1]}

        for participant_row in self.participant_configurations[1:]:
            for participant_name in participant_row[:-1]:
                matches = [(
                    k,
                    participant_name,
                    os.path.commonprefix(" ".join(
                        (" ".join(
                            self.participant_lookup[k]),
                         participant_name)).split())) \
                    for k in self.participant_lookup.keys() \
                        if len(os.path.commonprefix(" ".join(
                            (" ".join(
                                self.participant_lookup[k]),
                             participant_name)).split()))]
                if len(matches):
                    max_length = max([len(prefix) \
                        for *rest, prefix in matches])
                    match_row = [(k, n, p) \
                        for k, n, p in matches \
                        if len(p) == max_length]

                    for key, name, participant in match_row:
                        if name not in self.participant_lookup[key]:
                            self.participant_lookup[key].append(name)
                            if len(participant) < len(key):
                                self.participant_lookup[participant] = \
                                    self.participant_lookup.pop(key)
                else:
                    self.participant_lookup[participant_name] = \
                        [participant_name]

        self.participant_lookup = {
            value:key for key, lookup \
                in self.participant_lookup.items() for value in lookup}
        self.participants = {value for value \
            in self.participant_lookup.values()}

    @staticmethod
    def __finish_array(array, previous_array=None, length=0):
        if previous_array:
            array = array+previous_array[len(array):]
        else:
            try:
                array += [array[-1]]*(length-len(array))
            except IndexError:
                array = [None for x in range(length)]
        return array

    def __load_configuration(self, configuration):
        with open(os.path.realpath(configuration), 'r') as config_file:
            try:
                json_data = json.load(config_file)
            except ValueError as exception:
                raise exception

        self.font = json_data['font']
        self.font_size = json_data['font_size']
        self.heading_font = json_data['heading_font']
        self.heading_font_size = json_data['heading_font_size']
        self.heading_color = tuple(json_data['heading_color'])

        self.backdrop = json_data['backdrop']
        self.logo = json_data['logo']
        self.logo_height = json_data['logo_height']
        self.logo_width = json_data['logo_width']
        self.series_logo = json_data['series_logo']

        self.show_champion = json_data['show_champion']

        self.heading_text = json_data['heading_text']
        self.subheading_text = json_data['subheading_text']

        self.margin = json_data['margin']
        self.column_margin = json_data['column_margin']

        self.source_video = json_data['source_video']
        self.source_telemetry = json_data['source_telemetry']
        self.telemetry_file = 'tele.csv'
        self.output_video = json_data['output_video']

        self.participant_config = {k:v \
            for k, v \
            in json_data['participant_config'].items()}

        self.point_structure = json_data['point_structure']

        self.video_threshold = json_data['video_threshold']
        self.video_gaptime = json_data['video_gaptime']
        self.video_skipstart = json_data['video_skipstart']
        self.video_skipend = json_data['video_skipend']
        self.video_cache = json_data['video_cache']

        self.sync_racestart = json_data['sync_racestart']

if __name__ == "__main__":
    CONFIG = Configuration()
