"""
Integration testing of StaticBase.py
"""
import json
import os

from PIL import Image

from replayenhancer.RaceData import RaceData
from replayenhancer.DefaultCards \
    import RaceResults, SeriesStandings, StartingGrid


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

    starting_grid = StartingGrid(
        sorted(race_data.starting_grid, key=lambda x: x.position),
        **configuration)
    Image.fromarray(starting_grid.to_frame()).save(
        output_prefix + "_starting_grid.png")

    while True:
        try:
            race_data.get_data()
        except StopIteration:
            break

    results = RaceResults(
        sorted(race_data.classification, key=lambda x: x.position),
        **configuration)
    Image.fromarray(results.to_frame()).save(
        output_prefix + '_results.png')

    series_standings = SeriesStandings(
        race_data.classification,
        **configuration)
    Image.fromarray(series_standings.to_frame()).save(
        output_prefix + '_series_standings.png')

if __name__ == '__main__':
    test_race(
        'assets/race1-descriptor',
        'assets/race1.json',
        'outputs/race_1')
