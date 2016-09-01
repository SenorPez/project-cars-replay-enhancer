"""
Integration testing of StaticBase.py
"""
import json
import os

from PIL import Image

from replayenhancer.RaceData import RaceData
from replayenhancer.StaticBase import StaticBase


def test_race_1(telemetry_data, config_file, output_filename):
    """
    Full test of data from race 1.
    """
    race_data = RaceData(telemetry_data)
    configuration = json.load(open(config_file))

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    starting_grid = StaticBase(
        sorted(race_data.starting_grid, key=lambda x: x.position),
        **configuration)
    results = StaticBase(
        sorted(race_data.starting_grid, key=lambda x: x.driver_name),
        **configuration)
    Image.fromarray(starting_grid.to_frame()).save(
        output_filename+"_starting_grid_.png")
    Image.fromarray(results.to_frame()).save(
        output_filename+"_results.png")

if __name__ == '__main__':
    test_race_1(
        'assets/race1-descriptor',
        'assets/race1.json',
        'outputs/race_1')
