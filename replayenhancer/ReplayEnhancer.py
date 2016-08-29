"""
Provides classes for enhancing Project CARS replays.
"""
import argparse
import json
import os.path
from json import JSONDecodeError

from PIL import ImageFont


class ReplayEnhancer():
    """
    Holds replay configuration.
    """
    def __init__(self, configuration):
        try:
            with open(os.path.realpath(configuration), 'r', encoding='utf-8') as config_file:
                json_data = json.load(config_file)
        except FileNotFoundError as e:
            print("File not found: {}".format(e.filename))
        except JSONDecodeError as e:
            print("JSON Error: {}".format(e.msg),
                  "Error on line number {}".format(e.lineno))
        else:
            self._load_configuration(json_data)

    def _load_configuration(self, json_data):
        """
        Commenting out all elements. Enable as needed by development.
        We'll see what we're not using, that way.
        """
        self.dummy = json_data['dummy']

        # self.margin = json_data['margin']
        # self.column_margin = json_data['column_margin']
        #
        # self.font = ImageFont.truetype(
        #     json_data['font'],
        #     json_data['font_size'])
        # self.font_color = tuple(json_data['font_color'])
        #
        # self.heading_font = ImageFont.truetype(
        #     json_data['heading_font'],
        #     json_data['heading_font_size'])
        # self.heading_font_color = tuple(json_data['heading_font_color'])
        # self.heading_text = json_data['heading_text']
        # self.subheading_text = json_data['subheading_text']
        #
        # self.heading_color = tuple(json_data['heading_color'])
        # self.series_logo = json_data['series_logo']
        #
        # self.backdrop = json_data['backdrop']
        # self.logo = json_data['logo']
        # self.logo_height = json_data['logo_height']
        # self.logo_width = json_data['logo_width']
        #
        # self.result_lines = json_data['result_lines']
        #
        # self.show_champion = json_data['show_champion']
        #
        # self.source_video = json_data['source_video']
        # self.video_skipstart = json_data['video_skipstart']
        # self.video_skipend = json_data['video_skipend']
        # self.sync_racestart = json_data['sync_racestart']
        #
        # self.source_telemetry = json_data['source_telemetry']
        # self.output_video = json_data['output_video']
        #
        # self.name_display = {k:v['display'] for k, v in json_data['participant_config'].items()}
        # additional_names = {k:k for k, v in json_data['additional_participant_config'].items()}
        # self.name_display.update(additional_names)
        #
        # self.short_name_display = {k:v['short_display'] for k, v in json_data['participant_config'].items()}
        # additional_short_names = {k:v['short_display'] for k, v in json_data['additional_participant_config'].items()}
        # self.short_name_display.update(additional_short_names)
        #
        # self.car_data = {k:v['car'] for k, v in json_data['participant_config'].items()}
        # additional_cars = {k:v['car'] for k, v in json_data['additional_participant_config'].items()}
        # self.car_data.update(additional_cars)
        #
        # self.car_classes = json_data['car_classes']
        #
        # self.team_data = {k:v['team'] for k, v in json_data['participant_config'].items()}
        # additional_teams = {k:v['team'] for k, v in json_data['additional_participant_config'].items()}
        # self.team_data.update(additional_teams)
        #
        # self.points = {k:v['points'] for k, v in json_data['participant_config'].items()}
        # additional_points = {k:v['points'] for k, v in json_data['additional_participant_config'].items()}
        # self.points.update(additional_points)
        #
        # self.point_structure = json_data['point_structure']

if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(
            description="Project CARS Replay Enhancer")
        PARSER.add_argument(
            '-v',
            '--version',
            action='version',
            version='Version 0.5')
        PARSER.add_argument('configuration', nargs='?')

        ARGS = PARSER.parse_args()

        ERR_MSG = ""
        if ARGS.configuration is None:
            PARSER.error("\nNo configuration file provided. Aborting.")

    except KeyboardInterrupt:
        print("Aborting Project CARS Replay Enhancer")
        raise
