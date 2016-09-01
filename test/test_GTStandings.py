"""
Tests GTStandings.py
"""

import unittest
import unittest.mock as mock

from PIL import Image, ImageFont
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

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_init(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        expected_value = StandingsLine
        self.assertIsInstance(instance, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._name_color
        self.assertTupleEqual(instance.name_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_text_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._name_text_color
        self.assertTupleEqual(instance.name_text_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_color_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_name_color
        self.assertTupleEqual(instance.name_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_text_color_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_name_text_color
        self.assertTupleEqual(instance.name_text_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_text_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)

    @mock.patch('PIL.ImageFont.ImageFont')
    @mock.patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_color_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    @mock.patch('PIL.ImageFont.ImageFont', autospec=True)
    @mock.patch(
        'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
        autospec=True)
    def test_property_position_text_color_viewed(self, mock_driver, mock_font):
        instance = StandingsLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)

    @mock.patch(
        'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
        autospec=True)
    def test_method_render_not_viewed(self, mock_driver):
        font = ImageFont.load_default()
        mock_driver.race_position = 1
        mock_driver.name = "Kobernulf Monnur"
        instance = StandingsLine(mock_driver, font, (100, 100))
        expected_value = Image.Image
        self.assertIsInstance(instance._render(), expected_value)

    @mock.patch(
        'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
        autospec=True)
    def test_method_render_viewed(self, mock_driver):
        font = ImageFont.load_default()
        mock_driver.race_position = 1
        mock_driver.name = "Kobernulf Monnur"
        instance = StandingsLine(mock_driver, font, (100, 100))
        instance._viewed = True
        expected_value = Image.Image
        self.assertIsInstance(instance._render(), expected_value)
