"""
Tests DefaultCards.py
"""

import unittest
from unittest.mock import PropertyMock, patch, sentinel

from replayenhancer.DefaultCards \
    import RaceResults, SeriesStandings, StartingGrid, SeriesChampion


class TestRaceResults(unittest.TestCase):
    """
    Unit tests for Race Results card.
    """

    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_no_config(self, mock_classification_entry):
        instance = RaceResults(mock_classification_entry)
        expected_result = RaceResults
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_init_config(self, mock_classification_entry):
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
        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = RaceResults
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_best_lap(self, mock_classification_entry):
        driver_name = 'Kobernulf_Monnur'
        position = 1
        best_lap = 42.0

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=best_lap)

        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = '20'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_not_best_lap(self, mock_classification_entry):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 56.0

        configuration = {
            'point_structure': [5, 15, 12, 10, 8, 6, 4, 2, 1]
        }
        type(mock_classification_entry).best_lap = PropertyMock(
            return_value=42.0)

        instance = RaceResults([mock_classification_entry], **configuration)
        expected_result = '15'
        self.assertEqual(
            instance.calc_points(
                (driver_name, position, best_lap),
                **configuration),
            expected_result)

    @patch('replayenhancer.RaceData.ClassificationEntry', autospec=True)
    def test_method_calc_points_no_point_structure(self, mock_classification_entry):
        driver_name = 'Kobernulf Monnur'
        position = 1
        best_lap = 42.0

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