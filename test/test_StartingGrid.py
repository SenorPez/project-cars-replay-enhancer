"""
Tests StartingGrid.py
"""
import unittest
from unittest.mock import patch, sentinel

import numpy
from PIL import Image, ImageFont

from replayenhancer.StartingGrid import StartingGrid
from replayenhancer.StartingGridEntry import StartingGridEntry


class TestStartingGrid(unittest.TestCase):
    """
    Tests against the StartingGrid object.
    """
    test_data = [
        StartingGridEntry(1, 0, "Kobernulf Monnur"),
        StartingGridEntry(2, 1, "Testy McTest")
    ]

    def test_init(self):
        instance = StartingGrid(self.test_data)
        expected_value = StartingGrid
        self.assertIsInstance(instance, expected_value)

    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_make_mask(self, mock_mpy):
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.make_mask(), expected_value)

    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame(self, mock_mpy):
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StartingGrid.ImageFont.truetype',
           autospec=True)
    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_header(self, mock_mpy, mock_font):
        mock_font.return_value = ImageFont.load_default()
        configuration = {
            'heading_color': [255, 0, 0],
            'heading_font_color': [255, 255, 255],
            'heading_font': sentinel.font,
            'heading_font_size': sentinel.font_size,
            'heading_text': "Lorem Ipsum",
            'subheading_text': "For one, for all"
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StartingGrid.ImageFont.truetype',
           autospec=True)
    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_incomplete_header(self,
                                                    mock_mpy,
                                                    mock_font):
        mock_font.return_value = ImageFont.load_default()
        configuration = {
            'heading_color': [255, 0, 0],
            'heading_font_color': [255, 255, 255],
            'heading_text': "Lorem Ipsum",
            'subheading_text': "For one, for all"
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StartingGrid.ImageFont.truetype',
           autospec=True)
    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_font(self, mock_mpy, mock_font):
        mock_font.return_value = ImageFont.load_default()
        configuration = {
            'font': sentinel.font,
            'font_size': sentinel.font_size,
            'font_color': [0, 0, 0]
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StartingGrid.ImageFont.truetype',
           autospec=True)
    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_incomplete_font(self,
                                                  mock_mpy,
                                                  mock_font):
        mock_font.return_value = ImageFont.load_default()
        configuration = {
            'font': sentinel.font
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_margin(self, mock_mpy):
        configuration = {
            'margin': 20
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_with_column_margin(self, mock_mpy):
        configuration = {
            'column_margin': 10
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)


    @patch('replayenhancer.StartingGrid.ImageFont.truetype',
           autospec=True)
    @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
    def test_method_to_frame_full_configuration(self, mock_mpy, mock_font):
        mock_font.return_value = ImageFont.load_default()
        configuration = {
            'heading_color': [255, 0, 0],
            'heading_font_color': [255, 255, 255],
            'heading_font': sentinel.font,
            'heading_font_size': sentinel.font_size,
            'heading_text': "Lorem Ipsum",
            'subheading_text': "For one, for all",
            'font': sentinel.font,
            'font_size': sentinel.font_size,
            'margin': 20,
            'column_margin': 10
        }
        mock_mpy.return_value = numpy.array(sentinel.test)
        instance = StartingGrid(self.test_data, **configuration)
        expected_value = numpy.ndarray
        self.assertIsInstance(instance.to_frame(), expected_value)

if __name__ == '__main__':
    unittest.main()
