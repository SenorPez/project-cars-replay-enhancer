"""
Tests SeriesStandingsWithChange.py
"""
import unittest
from unittest.mock import MagicMock, PropertyMock, sentinel, patch

import numpy

from replayenhancer.RaceData import ClassificationEntry
from replayenhancer.SeriesStandingsWithChange import SeriesStandingsWithChange


class TestSeriesStandingsWithChange(unittest.TestCase):
    """
    Tests against the SeriesStandingsWithChange object.
    """
    def test_init_no_config(self):
        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=('Kobernulf Monnur', 1, 42.0))

        instance = SeriesStandingsWithChange([mock_classification_entry])

        expected_result = SeriesStandingsWithChange
        self.assertIsInstance(instance, expected_result)

    def test_init_config(self):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'points': 25
                }
            },
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=('Kobernulf Monnur', 1, 42.0))

        instance = SeriesStandingsWithChange(
            [mock_classification_entry],
            **configuration)

        expected_result = SeriesStandingsWithChange
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.SeriesStandingsWithChange.ImageFont.truetype',
           autospec=True)
    def test_init_config_font_attribute_error(self, mock_truetype):
        configuration = {
            'font': sentinel.font,
            'font_size': 10
        }

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=('Kobernulf Monnur', 1, 42.0))

        mock_truetype.side_effect = AttributeError

        instance = SeriesStandingsWithChange(
            [mock_classification_entry],
            **configuration)

        expected_result = SeriesStandingsWithChange
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.SeriesStandingsWithChange.ImageFont.truetype',
           autospec=True)
    def test_init_config_font_os_error(self, mock_truetype):
        configuration = {
            'font': sentinel.font,
            'font_size': 10
        }

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=('Kobernulf Monnur', 1, 42.0))

        mock_truetype.side_effect = OSError

        instance = SeriesStandingsWithChange(
            [mock_classification_entry],
            **configuration)

        expected_result = SeriesStandingsWithChange
        self.assertIsInstance(instance, expected_result)

    @unittest.skip("TODO: Implement superclass testing.")
    def test_property_row_colors(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_calc_series_points(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_calc_series_rank(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_calc_points(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_format_time(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_add_column(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_add_lookup(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_car_class_formatter(self):
        self.fail()

    @unittest.skip("TODO: Implement superclass testing.")
    def test_method_sort_data(self):
        self.fail()

    def test_method_to_frame_no_changes(self):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'points': 25
                }
            },
        }

        mock_classification_entry = MagicMock(spec=ClassificationEntry)
        driver_name = 'Kobernulf Monnur'
        type(mock_classification_entry).calc_points_data = PropertyMock(
            return_value=(driver_name, 1, 42.0))
        type(mock_classification_entry).driver_name = driver_name

        instance = SeriesStandingsWithChange(
            [mock_classification_entry],
            **configuration)

        expected_result = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_result)

    def test_method_to_frame_with_changes(self):
        configuration = {
            'participant_config': {
                'Kobernulf Monnur': {
                    'points': 20
                },
                'Testy McTest': {
                    'points': 25
                }
            },
            'point_structure': [0, 20, 5]
        }

        mock_classification_entry_1 = MagicMock(spec=ClassificationEntry)
        best_lap = 42.0
        driver_name = 'Kobernulf Monnur'
        type(mock_classification_entry_1).best_lap = best_lap
        type(mock_classification_entry_1).calc_points_data = PropertyMock(
            return_value=(driver_name, 1, best_lap))
        type(mock_classification_entry_1).driver_name = driver_name

        mock_classification_entry_2 = MagicMock(spec=ClassificationEntry)
        best_lap = 42.0
        driver_name = 'Testy McTest'
        type(mock_classification_entry_2).best_lap = best_lap
        type(mock_classification_entry_2).calc_points_data = PropertyMock(
            return_value=(driver_name, 2, 42.0))
        type(mock_classification_entry_2).driver_name = driver_name

        instance = SeriesStandingsWithChange(
            [mock_classification_entry_1, mock_classification_entry_2],
            **configuration)

        expected_result = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_result)
