"""
Integration testing of StartingGrid.py
"""
import json
import os

from PIL import Image

from replayenhancer.RaceData import RaceData
from replayenhancer.StartingGrid import StartingGrid


def test_race_1():
    """
    Full test of data from race 1.
    """
    race_data = RaceData('assets/race1-descriptor')
    configuration = json.load(open('assets/race1.json'))

    if os.environ.get('HEADINGFONTOVERRIDE') is not None:
        configuration['heading_font'] = \
            os.environ['HEADINGFONTOVERRIDE']
    if os.environ.get('DISPLAYFONTOVERRIDE') is not None:
        configuration['font'] = os.environ['DISPLAYFONTOVERRIDE']

    starting_grid = StartingGrid(
        race_data.starting_grid,
        **configuration)
    Image.fromarray(starting_grid.to_frame()).save(
        'outputs/test_race_1.png')

if __name__ == '__main__':
    test_race_1()