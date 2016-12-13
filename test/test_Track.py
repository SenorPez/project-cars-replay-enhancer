"""Tests Track.py

"""


import unittest
from unittest.mock import mock_open, patch

from replayenhancer.Track import Track


class TestTrack(unittest.TestCase):
    """Unit tests against the Track object.

    """
    track_data = {
        "Test Track:Short": {
            "display_name": "Test Track Short",
            "length": 42.0,
            "pit_entry": [0, 0],
            "pit_exit": [100, 100],
            "pit_radius": 2
        },

        "Test Track:Kart": {
            "display_name": "Test Track Kart",
            "length": 15.0
        }
    }

    def test_init(self):
        with patch('replayenhancer.Track.open', mock_open()), \
                patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            expected_result = Track
            self.assertIsInstance(instance, expected_result)

    def test_init_no_json(self):
        with patch('replayenhancer.Track.open', mock_open()) as mock_open_error:
            mock_open_error.side_effect = FileNotFoundError
            instance = Track(42.0)
            expected_result = Track
            self.assertIsInstance(instance, expected_result)

    def test_init_bad_json(self):
        with patch('replayenhancer.Track.open', mock_open()), \
                patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.side_effect = ValueError
            with self.assertRaises(ValueError):
                _ = Track(42.0)

    def test_at_pit_entry_exact_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
                patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_entry((0, 0)))

    def test_at_pit_entry_close_x_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_entry((1, 0)))

    def test_at_pit_entry_edge_x_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_entry((2, 0)))

    def test_at_pit_entry_far_x_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_entry((3, 0)))

    def test_at_pit_entry_close_y_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_entry((0, 1)))

    def test_at_pit_entry_exact_y_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_entry((0, 2)))

    def test_at_pit_entry_far_y_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_entry((0, 3)))

    def test_at_pit_entry_no_pits(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(15.0)
            self.assertFalse(instance.at_pit_entry((0, 0)))

    def test_at_pit_entry_no_json(self):
        with patch('replayenhancer.Track.open', mock_open()) as mock_open_error:
            mock_open_error.side_effect = FileNotFoundError
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_entry((0, 0)))

    def test_at_pit_exit_exact_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_exit((100, 100)))

    def test_at_pit_exit_close_x_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_exit((101, 100)))

    def test_at_pit_exit_edge_x_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_exit((102, 100)))

    def test_at_pit_exit_far_x_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_exit((103, 100)))

    def test_at_pit_exit_close_y_true(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertTrue(instance.at_pit_exit((100, 101)))

    def test_at_pit_exit_edge_y_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_exit((100, 102)))

    def test_at_pit_exit_far_y_false(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_exit((100, 103)))

    def test_at_pit_exit_no_pits(self):
        with patch('replayenhancer.Track.open', mock_open()), \
             patch('replayenhancer.Track.load') as mock_json_load:
            mock_json_load.return_value = self.track_data
            instance = Track(15.0)
            self.assertFalse(instance.at_pit_exit((100, 100)))

    def test_at_pit_exit_no_json(self):
        with patch('replayenhancer.Track.open', mock_open()) as mock_open_error:
            mock_open_error.side_effect = FileNotFoundError
            instance = Track(42.0)
            self.assertFalse(instance.at_pit_exit((0, 0)))
