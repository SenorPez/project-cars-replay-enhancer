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
        **configuration
    )
    starting_grid.add_column('position', 'Pos.')
    starting_grid.add_lookup(
        'driver_name',
        'name_lookup',
        'ERROR',
        'Driver')
    starting_grid.add_lookup('driver_name', 'team_lookup', '', 'Team')
    starting_grid.add_lookup('driver_name', 'car_lookup', '', 'Car')
    starting_grid.add_lookup(
        'driver_name',
        'points_lookup',
        0,
        'Points')

    Image.fromarray(starting_grid.to_frame()).save(
        output_filename+"_starting_grid.png")

    while True:
        try:
            race_data.get_data()
        except StopIteration:
            break

    results = StaticBase(
        sorted(race_data.classification, key=lambda x: x.position),
        **configuration
    )
    results.add_column('position', 'Pos.')
    results.add_lookup('driver_name', 'name_lookup', 'ERROR', 'Driver')
    results.add_lookup('driver_name', 'team_lookup', '', 'Team')
    results.add_lookup('driver_name', 'car_lookup', '', 'Car')
    results.add_column('laps_complete', 'Laps')
    results.add_column(
        'race_time',
        'Time',
        formatter=results.format_time)
    results.add_column(
        'best_lap',
        'Best Lap',
        formatter=results.format_time)
    results.add_column(
        'best_sector_1',
        'Best S1',
        formatter=results.format_time)
    results.add_column(
        'best_sector_2',
        'Best S2',
        formatter=results.format_time)
    results.add_column(
        'best_sector_3',
        'Best S3',
        formatter=results.format_time)
    results.add_column(
        'points',
        'Points',
        formatter=results.calc_points)

    Image.fromarray(results.to_frame()).save(
        output_filename+'_results.png')

    series_standings = StaticBase(
        race_data.classification,
        **configuration
    )
    series_standings.sort_data(
        lambda x: (
            -int(series_standings.calc_series_points(x.v_points)),
            x.driver_name))
    series_standings.add_column(
        'v_points',
        'Rank',
        formatter=results.calc_series_rank)
    series_standings.add_lookup(
        'driver_name',
        'name_lookup',
        'ERROR',
        'Driver')
    series_standings.add_lookup(
        'driver_name',
        'team_lookup',
        '',
        'Team')
    series_standings.add_lookup('driver_name', 'car_lookup', '', 'Car')
    series_standings.add_column(
        'v_points',
        'Points',
        formatter=results.calc_series_points)

    Image.fromarray(series_standings.to_frame()).save(
        output_filename+'_series_standings.png')


if __name__ == '__main__':
    test_race_1(
        'assets/race1-descriptor',
        'assets/race1.json',
        'outputs/race_1')
