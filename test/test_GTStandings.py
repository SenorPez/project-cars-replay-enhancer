"""
Tests GTStandings.py
"""

import unittest

from PIL import Image
from moviepy.video.io.bindings import PIL_to_npimage
from numpy.testing import assert_array_equal

from replayenhancer.GTStandings import GTStandings, StandingsLine


class TestGTStandings(unittest.TestCase):
    """
    Unit tests for a GT Standings object.
    """

    def test_init(self):
        instance = GTStandings()
        expected_value = GTStandings
        self.assertIsInstance(instance, expected_value)

    def test_property_default_clip_t(self):
        instance = GTStandings()
        expected_value = 0
        self.assertEqual(instance.clip_t, expected_value)

    def test_property_clip_t(self):
        instance = GTStandings(11.0)
        expected_value = 11.0
        self.assertEqual(instance.clip_t, expected_value)

    def test_property_default_ups(self):
        instance = GTStandings()
        expected_value = 30
        self.assertEqual(instance.ups, expected_value)

    def test_property_ups(self):
        instance = GTStandings(ups=10)
        expected_value = 10
        self.assertEqual(instance.ups, expected_value)

    def test_method_make_mask(self):
        instance = GTStandings()
        expected_value = PIL_to_npimage(
            Image.new('RGBA', (100, 100)).convert('RGB'))
        assert_array_equal(instance.make_mask(), expected_value)

    def test_method_to_frame(self):
        instance = GTStandings()
        expected_value = PIL_to_npimage(
            Image.new('RGBA', (100, 100)).convert('RGB'))
        assert_array_equal(instance.to_frame(), expected_value)

    def test_method_update(self):
        instance = GTStandings()
        expected_value = None
        self.assertEqual(instance.update(), expected_value)


class TestStandingsLine(unittest.TestCase):
    """
    Unit tests for the StandingsLine object.
    """

    def test_init(self):
        instance = StandingsLine()
        expected_value = StandingsLine
        self.assertIsInstance(instance, expected_value)

    def test_property_position_color_not_viewed(self):
        instance = StandingsLine()
        instance._viewed = False
        expected_value = instance._position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    def test_property_position_text_color_not_viewed(self):
        instance = StandingsLine()
        instance._viewed = False
        expected_value = instance._position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)

    def test_property_position_color_viewed(self):
        instance = StandingsLine()
        instance._viewed = True
        expected_value = instance._viewed_position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    def test_property_position_text_color_viewed(self):
        instance = StandingsLine()
        instance._viewed = True
        expected_value = instance._viewed_position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)