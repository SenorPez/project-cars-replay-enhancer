"""
Tests GTStandings.py
"""

import unittest
from unittest.mock import MagicMock, patch

from replayenhancer.GTStandings import Animation, GTStandings, PitStopFlyout, StandingLine


class TestPitStopFlyout(unittest.TestCase):
    """Unit tests for PitStopFlyout object.

    """
    def test_init(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        expected_result = PitStopFlyout
        self.assertIsInstance(instance, expected_result)

    def test_init_margin(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location, margin=42)
        expected_result = PitStopFlyout
        self.assertIsInstance(instance, expected_result)

    def test_init_ups(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location, ups=60)
        expected_result = PitStopFlyout
        self.assertIsInstance(instance, expected_result)

    def test_method_close_flyout(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        instance.close_flyout()
        expected_result = Animation
        self.assertIsInstance(instance.animations[-1], expected_result)

    def test_method_close_flyout_set_persist(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        instance.close_flyout()
        self.assertFalse(instance.persist)

    def test_method_close_flyout_set_is_closing(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        instance.close_flyout()
        self.assertTrue(instance.is_closing)

    @patch('PIL.ImageDraw.Draw', autospec=True)
    @patch('PIL.Image', autospec=True)
    def test_method_to_frame(self, mock_image, mock_draw):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        mock_image.new = MagicMock(spec='numpy.ndarray', autospec=True)
        font.getsize = MagicMock(return_value=(20, 20))
        mock_draw.text = MagicMock(spec='numpy.ndarray')

        instance = PitStopFlyout(race_data, driver, font, size, location)
        from PIL.Image import Image as expected_value
        self.assertIsInstance(instance.to_frame(), expected_value)

    def test_method_update_not_stopped(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        for time in range(16):
            instance.update((time*10, 1, time*10), time)

    def test_method_update_stopped_no_time(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        for _ in range(16):
            instance.update(location)

    def test_method_update_stopped_ascending_time(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        for time in range(16):
            instance.update(location, time)

    def test_method_update_stopped_reset_time(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        for time in range(8):
            instance.update(location, time + 8)
        for time in range(8):
            instance.update(location, time)

    def test_property_text_color_pit_in(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData',
                              autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (100, 1, 100)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        expected_result = (255, 0, 0, 255)
        self.assertTupleEqual(instance.text_color, expected_result)

    def test_property_text_color_pit_out(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (0, 1, 0)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        for time in range(16):
            instance.update(location, time)

        expected_result = (255, 255, 255, 255)
        self.assertTupleEqual(instance.text_color, expected_result)

    def test_field_is_closing(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (0, 1, 0)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        self.assertFalse(instance.is_closing)

    def test_field_is_closing_set_true(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (0, 1, 0)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        instance.is_closing = True
        self.assertTrue(instance.is_closing)

    def test_field_persist(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (0, 1, 0)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        self.assertTrue(instance.persist)

    def test_field_persist_set_false(self):
        race_data = MagicMock(spec='replayenhancer.RaceData.RaceData', autospec=True)
        driver = MagicMock(spec='replayenhancer.RaceData.Driver', autospec=True)
        font = MagicMock(spec='PIL.ImageFont', autospec=True)
        size = (100, 100)
        location = (0, 1, 0)

        instance = PitStopFlyout(race_data, driver, font, size, location)
        instance.persist = False
        self.assertFalse(instance.persist)




@unittest.skip("Need to rewrite based on new GTStandings module.")
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

    # def test_method_to_frame(self):
    #     instance = GTStandings()
    #     expected_value = PIL_to_npimage(
    #         Image.new('RGBA', (100, 100)).convert('RGB'))
    #     assert_array_equal(instance.to_frame(), expected_value)

    def test_method_update(self):
        instance = GTStandings()
        expected_value = None
        self.assertEqual(instance.update(), expected_value)

@unittest.skip("Need to rewrite based on new GTStandings module.")
class TestStandingLine(unittest.TestCase):
    """
    Unit tests for the StandingLine object.
    """

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_init(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        expected_value = StandingLine
        self.assertIsInstance(instance, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._name_color
        self.assertTupleEqual(instance.name_color, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_text_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._name_text_color
        self.assertTupleEqual(instance.name_text_color, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_color_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_name_color
        self.assertTupleEqual(instance.name_color, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_name_text_color_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_name_text_color
        self.assertTupleEqual(instance.name_text_color, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_text_color_not_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = False
        expected_value = instance._position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)

    @patch('PIL.ImageFont.ImageFont')
    @patch('replayenhancer.RETelemetryDataPacket.REParticipantInfo')
    def test_property_position_color_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_position_color
        self.assertTupleEqual(instance.position_color, expected_value)

    @patch('PIL.ImageFont.ImageFont', autospec=True)
    @patch(
        'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
        autospec=True)
    def test_property_position_text_color_viewed(self, mock_driver, mock_font):
        instance = StandingLine(mock_driver, mock_font, (100, 100))
        instance._viewed = True
        expected_value = instance._viewed_position_text_color
        self.assertTupleEqual(
            instance.position_text_color,
            expected_value)

    # @patch(
    #     'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
    #     autospec=True)
    # def test_method_render_not_viewed(self, mock_driver):
    #     font = ImageFont.load_default()
    #     mock_driver.race_position = 1
    #     mock_driver.name = "Kobernulf Monnur"
    #     instance = StandingLine(mock_driver, font, (100, 100))
    #     expected_value = Image.Image
    #     self.assertIsInstance(instance._render(), expected_value)
    #
    # @patch(
    #     'replayenhancer.RETelemetryDataPacket.REParticipantInfo',
    #     autospec=True)
    # def test_method_render_viewed(self, mock_driver):
    #     font = ImageFont.load_default()
    #     mock_driver.race_position = 1
    #     mock_driver.name = "Kobernulf Monnur"
    #     instance = StandingLine(mock_driver, font, (100, 100))
    #     instance._viewed = True
    #     expected_value = Image.Image
    #     self.assertIsInstance(instance._render(), expected_value)
