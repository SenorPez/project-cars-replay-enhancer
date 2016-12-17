"""
Tests DefaultCards.py
"""

import unittest
from unittest.mock import MagicMock, PropertyMock, patch, sentinel

import numpy
from PIL import ImageFont

from replayenhancer.DefaultCards \
    import RaceResults, SeriesStandings, StartingGrid, SeriesChampion


class TestRaceResults(unittest.TestCase):
    """
    Unit tests for Race Results card.
    """

    @patch('replayenhancer.RaceData.Driver', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_no_config(self, mock_classification_entry, mock_driver):
        mock_driver.laps_complete = 6
        mock_driver.race_time = 42.00
        mock_driver.stops = 0
        mock_classification_entry.driver = mock_driver
        instance = RaceResults([mock_classification_entry])
        expected_result = RaceResults
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.Driver', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_config(self, mock_classification_entry, mock_driver):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'DarkNitro',
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        mock_driver.laps_complete = 6
        mock_driver.race_time = 42.00
        mock_driver.stops = 0
        mock_classification_entry.driver = mock_driver
        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = RaceResults
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.Driver', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_best_lap(self, mock_classification_entry,
                                         mock_driver):
        driver_name = 'Kobernulf_Monnur'
        position = 1
        best_lap = 42.0

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)

        mock_driver.laps_complete = 6
        mock_driver.race_time = 42.00
        mock_driver.stops = 0
        mock_classification_entry.driver = mock_driver

        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = '20'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.RaceData.Driver', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_not_best_lap(self, mock_classification_entry,
                                             mock_driver):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 56.0

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=42.0)

        mock_driver.laps_complete = 6
        mock_driver.race_time = 42.00
        mock_driver.stops = 0
        mock_classification_entry.driver = mock_driver

        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = '15'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.RaceData.Driver', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_no_point_structure(
            self, mock_classification_entry, mock_driver):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 42.0

        mock_driver.laps_complete = 6
        mock_driver.race_time = 42.00
        mock_driver.stops = 0
        mock_classification_entry.driver = mock_driver
        instance = RaceResults([mock_classification_entry])
        expected_result = '0'
        self.assertEqual(
            instance.calc_points((driver_name, position, best_lap)),
            expected_result)

    def test_method_format_time_below_min(self):
        time = 42
        expected_result = '42.000'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_below_min_truncate(self):
        time = 42.1234
        expected_result = '42.123'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_below_min_round(self):
        time = 42.9876
        expected_result = '42.988'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_below_hour(self):
        time = 84
        expected_result = '1:24.000'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_below_hour_truncate(self):
        time = 84.1234
        expected_result = '1:24.123'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_below_hour_round(self):
        time = 84.9876
        expected_result = '1:24.988'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time(self):
        time = 3702
        expected_result = '1:01:42.000'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_truncate(self):
        time = 3702.1234
        expected_result = '1:01:42.123'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_round(self):
        time = 3702.9876
        expected_result = '1:01:42.988'
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_passed_none(self):
        time = None
        expected_result = ""
        self.assertEqual(RaceResults.format_time(time), expected_result)

    def test_method_format_time_passed_string(self):
        time = "ERROR"
        expected_result = ""
        self.assertEqual(RaceResults.format_time(time), expected_result)


class TestStartingGrid(unittest.TestCase):
    """
    Unit tests for Starting Grid card.
    """

    @patch('replayenhancer.RaceData.StartingGridEntry', autospec=True)
    def test_init_no_config(self, mock_starting_grid_entry):
        instance = StartingGrid(mock_starting_grid_entry)
        expected_result = StartingGrid
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.StartingGridEntry', autospec=True)
    def test_init_config(self, mock_starting_grid_entry):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'DarkNitro',
                    'points': 0
                }
            }
        }
        instance = StartingGrid([mock_starting_grid_entry], **configuration)
        expected_result = StartingGrid
        self.assertIsInstance(instance, expected_result)


class TestSeriesStandings(unittest.TestCase):
    """
    Unit Tests for Series Standings card.
    """

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_no_config(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = ('Kobernulf Monnur', 1, 42.0)

        instance = SeriesStandings(mock_classification_entry)
        expected_result = SeriesStandings
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_config(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = ('Kobernulf Monnur', 1, 42.0)

        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'Dark Nitro',
                    'points': 15
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = SeriesStandings([mock_classification_entry], **configuration)
        expected_result = SeriesStandings
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_series_points(self, mock_classification_entry, mock_sort_data):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 42.0

        mock_sort_data.return_value = (driver_name, position, best_lap)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)

        configuration = {
            'points_lookup': {
                'Kobernulf Monnur': 15
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = SeriesStandings([mock_classification_entry])
        expected_result = '35'
        self.assertEqual(
            instance.calc_series_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_series_points_no_entry(self, mock_classification_entry, mock_sort_data):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 42.0

        mock_sort_data.return_value = (driver_name, position, best_lap)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = SeriesStandings([mock_classification_entry])
        expected_result = '20'
        self.assertEqual(
            instance.calc_series_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_series_rank_first(self, mock_classification_entry, mock_sort_data):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 42.0

        mock_sort_data.return_value = (driver_name, position, best_lap)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=(driver_name, position, best_lap))
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value=driver_name)

        configuration = {
            'points_lookup': {
                'Kobernulf Monnur': 15
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = SeriesStandings([mock_classification_entry])
        expected_result = '1'
        self.assertEqual(
            instance.calc_series_rank(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry')
    def test_method_calc_series_rank_tie_second(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = [
            ('First Place', 1, 42.0),
            ('Second Place', 2, 42.0),
            ('Third Place', 3, 42.0)
        ]

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('First Place', 1, 42.0),
            driver_name='First Place')
        first_place = patcher.start()

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('Second Place', 2, 42.0),
            driver_name='Second Place')
        second_place = patcher.start()

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('Third Place', 3, 42.0),
            driver_name='Third Place')
        third_place = patcher.start()

        configuration = {
            'points_lookup': {
                'First Place': 10,
                'Second Place': 5,
                'Third Place': 5
            },
            'point_structure': [0, 10, 6, 6]
        }

        instance = SeriesStandings([first_place, second_place, third_place])
        expected_result = '2'
        self.assertEqual(
            instance.calc_series_rank(
                ('Third Place', 3, 42.0),
                **configuration),
            expected_result)\

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry')
    def test_method_calc_series_rank_third(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = [
            ('First Place', 1, 42.0),
            ('Second Place', 2, 42.0),
            ('Third Place', 3, 42.0)
        ]

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('First Place', 1, 42.0),
            driver_name='First Place')
        first_place = patcher.start()

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('Second Place', 2, 42.0),
            driver_name='Second Place')
        second_place = patcher.start()

        patcher = patch(
            'replayenhancer.RaceData.ClassificationEntry',
            best_lap=42.0,
            calc_points_data=('Third Place', 3, 42.0),
            driver_name='Third Place')
        third_place = patcher.start()

        configuration = {
            'points_lookup': {
                'First Place': 10,
                'Second Place': 10,
                'Third Place': 5
            },
            'point_structure': [0, 10, 10, 6]
        }

        instance = SeriesStandings([first_place, second_place, third_place])
        expected_result = '3'
        self.assertEqual(
            instance.calc_series_rank(
                ('Third Place', 3, 42.0),
                **configuration),
            expected_result)


class TestSeriesChampion(unittest.TestCase):
    """
    Unit tests for Series Champion card.
    """

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_no_config(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = ('Kobernulf Monnur', 1, 42.0)

        instance = SeriesChampion([mock_classification_entry])
        expected_result = SeriesChampion
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_config(self, mock_classification_entry, mock_sort_data):
        mock_sort_data.return_value = ('Kobernulf Monnur', 1,  42.0)

        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'Dark Nitro',
                    'points': 15
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = SeriesChampion([mock_classification_entry], **configuration)
        expected_result = SeriesChampion
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_to_frame_no_header(self, mock_classification_entry, mock_sort_data):
        first_place = mock_classification_entry
        type(first_place).calc_points_data = PropertyMock(return_value=(
            'Kobernulf Monnur',
            1,
            42.0))
        type(first_place).driver_name = PropertyMock(return_value=(
            'Kobernulf Monnur'))

        second_place = mock_classification_entry
        type(second_place).calc_points_data = PropertyMock(
            return_value=(
                'Second Place',
                2,
                43.0))
        type(second_place).driver_name = PropertyMock(return_value=(
            'Second Place'))

        third_place = mock_classification_entry
        type(third_place).calc_points_data = PropertyMock(return_value=(
            'Third Place',
            3,
            43.5))
        type(third_place).driver_name = PropertyMock(return_value=(
            'Third Place'))

        mock_sort_data.return_value = [
            ('Kobernulf Monnur', 1, 42.0),
            ('Second Place', 2, 43.0),
            ('Third Place', 3, 43.5)]

        expected_value = numpy.ndarray
        instance = SeriesChampion([first_place, second_place, third_place])
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StaticBase.StaticBase.sort_data', autospec=True)
    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_to_frame_blank_header(self, mock_classification_entry, mock_sort_data):
        first_place = mock_classification_entry
        type(first_place).calc_points_data = PropertyMock(return_value=(
            'Kobernulf Monnur',
            1,
            42.0))
        type(first_place).driver_name = PropertyMock(return_value=(
            'Kobernulf Monnur'))

        second_place = mock_classification_entry
        type(second_place).calc_points_data = PropertyMock(
            return_value=(
                'Second Place',
                2,
                43.0))
        type(second_place).driver_name = PropertyMock(return_value=(
            'Second Place'))

        third_place = mock_classification_entry
        type(third_place).calc_points_data = PropertyMock(return_value=(
            'Third Place',
            3,
            43.5))
        type(third_place).driver_name = PropertyMock(return_value=(
            'Third Place'))

        mock_sort_data.return_value = [
            ('Kobernulf Monnur', 1, 42.0),
            ('Second Place', 2, 43.0),
            ('Third Place', 3, 43.5)]

        configuration = {
            'heading_color': (255, 0, 0)}

        expected_value = numpy.ndarray
        instance = SeriesChampion([first_place, second_place, third_place], **configuration)
        self.assertIsInstance(instance.to_frame(), expected_value)