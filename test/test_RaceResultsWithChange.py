"""
Tests RaceResultsWithChange.py
"""
import unittest
from unittest.mock import MagicMock, PropertyMock, patch, sentinel

import numpy

from replayenhancer.RaceData import Driver, ClassificationEntry, \
    StartingGridEntry
from replayenhancer.RaceResultsWithChange import RaceResultsWithChange


class TestRaceResultsWithChange(unittest.TestCase):
    """
    Tests against the RaceResultsWithChange object.
    """

    def test_init_no_config(self):
        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry])

        expected_result = RaceResultsWithChange
        self.assertIsInstance(instance, expected_result)

    def test_init_config(self):
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
        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry],
            **configuration)
        expected_result = RaceResultsWithChange
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceResultsWithChange.ImageFont.truetype',
           autospec=True)
    def test_init_config_font_attribute_error(self, mock_truetype):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'DarkNitro',
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1],
            'font': sentinel.font,
            'font_size': 10
        }
        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        mock_truetype.side_effect = AttributeError

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry],
            **configuration)
        expected_result = RaceResultsWithChange
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceResultsWithChange.ImageFont.truetype',
           autospec=True)
    def test_init_config_font_os_error(self, mock_truetype):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'display': 'Senor Pez',
                    'car': '125cc Shifter Kart',
                    'team': 'DarkNitro',
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1],
            'font': sentinel.font,
            'font_size': 10
        }
        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        mock_truetype.side_effect = AttributeError

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry],
            **configuration)
        expected_result = RaceResultsWithChange
        self.assertIsInstance(instance, expected_result)

    def test_property_row_colors(self):
        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry])
        expected_result = [
            (192, 192, 192, 255),
            (255, 255, 255, 255)
        ]
        self.assertListEqual(instance.row_colors, expected_result)

    def test_method_calc_points_best_lap(self):
        driver_name = 'Kobernulf_Monnur'
        position = 1
        best_lap = 42.0

        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry).position = PropertyMock(
            return_value=1)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry],
            **configuration)
        expected_result = '20'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    def test_method_calc_points_not_best_lap(self):
        driver_name = 'Kobernulf_Monnur'
        position = 1
        driver_best_lap = 42.0
        race_best_lap = 11.0

        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value=driver_name)
        type(mock_classification_entry).position = PropertyMock(
            return_value=position)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=driver_best_lap)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value=driver_name)
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry],
            **configuration)
        expected_result = '15'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, race_best_lap),
                **configuration),
            expected_result)

    def test_method_calc_points_no_point_structure(self):
        driver_name = 'Kobernulf_Monnur'
        position = 1
        driver_best_lap = 42.0
        race_best_lap = 11.0

        mock_driver = MagicMock(spec=Driver)
        type(mock_driver).laps_complete = PropertyMock(return_value=6)
        type(mock_driver).race_time = PropertyMock(return_value=42.0)
        type(mock_driver).stops = PropertyMock(return_value=0)

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).driver = PropertyMock(
            return_value=mock_driver)
        type(mock_classification_entry).driver_name = PropertyMock(
            return_value=driver_name)
        type(mock_classification_entry).position = PropertyMock(
            return_value=position)
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=driver_best_lap)

        mock_starting_grid_entry = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry).driver_name = PropertyMock(
            return_value=driver_name)
        type(mock_starting_grid_entry).position = PropertyMock(
            return_value=2)

        instance = RaceResultsWithChange(
            [mock_classification_entry],
            [mock_starting_grid_entry])
        expected_result = '0'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, race_best_lap)),
            expected_result)

    def test_method_format_time_below_min(self):
        time = 42
        expected_result = '42.000'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_below_min_truncate(self):
        time = 42.1234
        expected_result = '42.123'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_below_min_round(self):
        time = 42.9876
        expected_result = '42.988'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_below_hour(self):
        time = 84
        expected_result = '1:24.000'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_below_hour_truncate(self):
        time = 84.1234
        expected_result = '1:24.123'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_below_hour_round(self):
        time = 84.9876
        expected_result = '1:24.988'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time(self):
        time = 3702
        expected_result = '1:01:42.000'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_truncate(self):
        time = 3702.1234
        expected_result = '1:01:42.123'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_round(self):
        time = 3702.9876
        expected_result = '1:01:42.988'
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_passed_none(self):
        time = None
        expected_result = ""
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    def test_method_format_time_passed_string(self):
        time = "ERROR"
        expected_result = ""
        self.assertEqual(
            RaceResultsWithChange.format_time(time), expected_result)

    @unittest.skip("No test.")
    def test_method_add_column(self):
        self.fail()

    @unittest.skip("No test.")
    def test_method_add_lookup(self):
        self.fail()

    @unittest.skip("No test.")
    def test_method_car_class_formatter(self):
        self.fail()

    @unittest.skip("No test.")
    def test_method_sort_data(self):
        self.fail()

    def test_method_to_frame_no_changes(self):
        mock_driver_1 = MagicMock(spec=Driver)
        type(mock_driver_1).laps_complete = PropertyMock(return_value=6)
        type(mock_driver_1).race_time = PropertyMock(return_value=42.0)
        type(mock_driver_1).stops = PropertyMock(return_value=0)

        mock_driver_2 = MagicMock(spec=Driver)
        type(mock_driver_2).laps_complete = PropertyMock(return_value=6)
        type(mock_driver_2).race_time = PropertyMock(return_value=45.0)
        type(mock_driver_2).stops = PropertyMock(return_value=0)

        mock_classification_entry_1 = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry_1).driver = PropertyMock(
            return_value=mock_driver_1)
        type(mock_classification_entry_1).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry_1).position = PropertyMock(
            return_value=1)

        mock_classification_entry_2 = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry_2).driver = PropertyMock(
            return_value=mock_driver_2)
        type(mock_classification_entry_2).driver_name = PropertyMock(
            return_value='Testy McTest')
        type(mock_classification_entry_2).position = PropertyMock(
            return_value=2)

        mock_starting_grid_entry_1 = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry_1).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry_1).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry_1).position = PropertyMock(
            return_value=1)

        mock_starting_grid_entry_2 = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry_2).driver_index = PropertyMock(
            return_value=1)
        type(mock_starting_grid_entry_2).driver_name = PropertyMock(
            return_value='Testy McTest')
        type(mock_starting_grid_entry_2).position = PropertyMock(
            return_value=2)

        instance = RaceResultsWithChange(
            [mock_classification_entry_1, mock_classification_entry_2],
            [mock_starting_grid_entry_2, mock_starting_grid_entry_1])
        expected_result = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_result)

    def test_method_to_frame_with_changes(self):
        mock_driver_1 = MagicMock(spec=Driver)
        type(mock_driver_1).laps_complete = PropertyMock(return_value=6)
        type(mock_driver_1).race_time = PropertyMock(return_value=42.0)
        type(mock_driver_1).stops = PropertyMock(return_value=0)

        mock_driver_2 = MagicMock(spec=Driver)
        type(mock_driver_2).laps_complete = PropertyMock(return_value=6)
        type(mock_driver_2).race_time = PropertyMock(return_value=45.0)
        type(mock_driver_2).stops = PropertyMock(return_value=0)

        mock_classification_entry_1 = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry_1).driver = PropertyMock(
            return_value=mock_driver_1)
        type(mock_classification_entry_1).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_classification_entry_1).position = PropertyMock(
            return_value=1)

        mock_classification_entry_2 = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry_2).driver = PropertyMock(
            return_value=mock_driver_2)
        type(mock_classification_entry_2).driver_name = PropertyMock(
            return_value='Testy McTest')
        type(mock_classification_entry_2).position = PropertyMock(
            return_value=2)

        mock_starting_grid_entry_1 = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry_1).driver_index = PropertyMock(
            return_value=0)
        type(mock_starting_grid_entry_1).driver_name = PropertyMock(
            return_value='Kobernulf Monnur')
        type(mock_starting_grid_entry_1).position = PropertyMock(
            return_value=2)

        mock_starting_grid_entry_2 = MagicMock(spec=StartingGridEntry)
        type(mock_starting_grid_entry_2).driver_index = PropertyMock(
            return_value=1)
        type(mock_starting_grid_entry_2).driver_name = PropertyMock(
            return_value='Testy McTest')
        type(mock_starting_grid_entry_2).position = PropertyMock(
            return_value=1)

        instance = RaceResultsWithChange(
            [mock_classification_entry_1, mock_classification_entry_2],
            [mock_starting_grid_entry_2, mock_starting_grid_entry_1])
        expected_result = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_result)
