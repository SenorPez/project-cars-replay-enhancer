"""
Provides the Configuration object for creating and modifying
configuration files for the Project CARS Replay Enhancer.
"""

import os
import json

from PIL import ImageFont

class Configuration:
    """
    Creates a Configuration that is written to a JSON file for the
    Project CARS Replay Enhancer
    """

    def __init__(self, previous_file=None):
        self.font = None
        self.heading_font = None
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

        if previous_file:
            self.config_file = os.path.realpath(previous_file)
            self.__load_configuration(previous_file)

        print("Beginning configuration. Press CTRL+C at any time to",
            "abort.")

        try:
            while True:
                print("Enter destination file for configuration.")
                print(".json file extension will be added ",
                    "automatically.")
                print("CAUTION: Existing file contents will be ",
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
                    print("Configuration file location invalid. ",
                        "Please try again.")
                    print("Directories must be created before ",
                        "running script.")

            while True:
                print("Enter source video file.")
                prompt = "({})".format(self.source_video) \
                    if previous_file else ""
                source_video = input(prompt+"--> ")

                if len(source_video) == 0 and previous_file:
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
                    break;
                elif os.path.isdir(os.path.split(
                        os.path.realpath(output_video))[0]):
                    self.output_video = output_video
                    break
                else:
                    print("Configuration file location invalid. ",
                        "Please try again.")
                    print("Directories must be created before ",
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
                    if previous_file else ""
                font_size = input(prompt+"--> ")

                if len(font_size) == 0 and previous_file:
                    break
                elif len(font_size) != 0 and 
                        isinstance(font_size, int):
                    self.font_size = font_size
                    break
                else
                    print("Font size should be an integer value.")

            while True:
                print("Enter path to heading font.")
                prompt = "({})".format(self.heading_font) \
                    if previous_file else ""
                heading_font = input(prompt+"--> ")

                if len(heading_font) == 0 and previous_file:
                    break
                elif os.path.isfile(os.path.realpath(heading_font)):
                    self.heading_font = heading+font
                    break
                else:
                    print("Not a file. Please try again.")

            while True:
                print("Enter size of heading font.")
                prompt = "({})".format(self.heading_font_size) \
                    if previous_file else ""
                heading_font_size = input(prompt+"--> ")

                if len(heading_font_size) == 0 and previous_file:
                    break
                elif len(heading_font_size) != 0 and 
                        isinstance(heading_font_size, int):
                    self.heading_font_size = heading_font_size
                    break
                else
                    print("Heading font size should be an integer ",
                        "value.")

            #TODO: Move to module-specific configuration
            while True:
                print("Enter heading color.")
                print("Color should be enetered as three integers, ",
                    "separated by commas, representing Red, Green, ",
                    "and Blue values.")
                prompt = "({}, {}, {})".format(*self.heading_color) \
                    if previous_file else ""
                heading_color = input(prompt+"--> ")
                
                if len(heading_color) == 0 and previous_file:
                    break
                else:
                    try:
                        heading_color = [int(x)
                            for x in heading_color.split(',')]
                        if all([x >= 0 and x <= 255 \
                                for x in heading_color]):
                            self.heading_color = heading_color
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("Invalid color value.")














                    
        except KeyboardInterrupt:
            print("\n\nExiting. No configuration data written.")
        else:
            with open(os.path.realpath(self.config_file), 'w') as f:
                json.dump(self, f)
            print("\n\nConfiguration data written to {}".format(
                self.config_file))

            

    def __load_configuration(self, configuration):
        with open(os.path.realpath(configuration), 'r') as f:
            try:
                json_data = json.load(f)
            except ValueError as e:
                raise e

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

        self.participant_config = [dict(participant=v['participant'], car=v['car'], team=v['team'], points=v['pints']) for v in json_data['participant_config']]

        self.point_structure = json_data['point_structure']

        self.video_threshold = json_data['video_threshold']
        self.video_gaptime = json_data['video_gaptime']
        self.video_skipstart = json_data['video_skipstart']
        self.video_skipend = json_data['video_skipend']
        self.video_cache = json_data['video_cache']

        self.sync_racestart = json_data['sync_racestart']
