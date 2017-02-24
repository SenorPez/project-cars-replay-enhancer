"""
Tests StaticBase.py
"""
import unittest
from unittest.mock import sentinel, MagicMock, PropertyMock

from replayenhancer.StaticBase import DisplayLine, DisplayColumn, StaticBase


class TestStaticBase(unittest.TestCase):
    """
    Tests against the StaticBase object.
    """
    def test_init(self):
        instance = StaticBase(sentinel.data)

        expected_result = StaticBase
        self.assertIsInstance(instance, expected_result)


class TestDisplayColumn(unittest.TestCase):
    """
    Tests against DisplayColumn object.
    """
    def test_init_defaults(self):
        instance = DisplayColumn(sentinel.attribute)

        expected_result = DisplayColumn
        self.assertIsInstance(instance, expected_result)


class TestDisplayLine(unittest.TestCase):
    """
    Tests against DisplayLine object.
    """
    def tearDown(self):
        DisplayLine.reset()

    def test_init_no_headings(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_init_headings(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None
        mock_column.heading = 'heading'

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data, make_headings=True)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_init_with_column_default(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = 'default'
        mock_column.formatter = None
        mock_column.lookup = PropertyMock(side_effect=KeyError)
        mock_column.heading = 'heading'

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_init_with_column_no_formatter(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.heading = 'heading'
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_init_with_column_formatter_args(self):
        mock_formatter = MagicMock()
        mock_formatter.return_value = sentinel.formatted

        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = mock_formatter
        mock_column.formatter_args = {'test': 25}
        mock_column.heading = 'heading'
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_init_with_column_formatter_no_args(self):
        mock_formatter = MagicMock()
        mock_formatter.return_value = sentinel.formatted

        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = mock_formatter
        mock_column.formatter_args = None
        mock_column.heading = 'heading'
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        expected_result = DisplayLine
        self.assertIsInstance(instance, expected_result)

    def test_next(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        mock_font = MagicMock()
        mock_font.getsize.return_value = (20, 20)

        instance = DisplayLine([mock_column], mock_data)
        instance.column_widths(mock_font, [])
        iterator = iter(instance)

        expected_result = tuple
        self.assertIsInstance(next(iterator), expected_result)

    def test_next_stop(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)
        iterator = iter(instance)

        with self.assertRaises(StopIteration):
            next(iterator)

    def test_method_column_widths_heading_line_and_colspan(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 2
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None
        mock_column.heading = "Heading"

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data, make_headings=True)

        expected_result = [0]
        self.assertListEqual(
            instance.column_widths(sentinel.font, None),
            expected_result)

    def test_method_column_widths_string_bigger(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        mock_font = MagicMock()
        mock_font.getsize.return_value = (20, 20)

        column_widths = [10]

        instance = DisplayLine([mock_column], mock_data)
        instance._column_widths = column_widths

        expected_result = [20]
        self.assertListEqual(
            instance.column_widths(mock_font, column_widths),
            expected_result)

    def test_method_column_widths_string_smaller(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        mock_font = MagicMock()
        mock_font.getsize.return_value = (20, 20)

        column_widths = [40]

        instance = DisplayLine([mock_column], mock_data)
        instance._column_widths = column_widths

        expected_result = [40]
        self.assertListEqual(
            instance.column_widths(mock_font, column_widths),
            expected_result)

    def test_method_column_widths_string_new_column(self):
        mock_column_1 = MagicMock(spec=DisplayColumn)
        mock_column_1.align = 'left'
        mock_column_1.attribute = 'test'
        mock_column_1.colspan = 1
        mock_column_1.default = None
        mock_column_1.formatter = None
        mock_column_1.lookup = None

        mock_column_2 = MagicMock(spec=DisplayColumn)
        mock_column_2.align = 'left'
        mock_column_2.attribute = 'test'
        mock_column_2.colspan = 1
        mock_column_2.default = None
        mock_column_2.formatter = None
        mock_column_2.lookup = None

        mock_data = MagicMock(test="test")

        mock_font = MagicMock()
        mock_font.getsize.return_value = (20, 20)

        column_widths = [40]

        instance = DisplayLine([mock_column_1, mock_column_2], mock_data)
        instance._column_widths = column_widths

        expected_result = [40, 20]
        self.assertListEqual(
            instance.column_widths(mock_font, column_widths),
            expected_result)

    def test_method_column_widths_object_bigger(self):
        mock_line_data = MagicMock()
        mock_line_data.size = (20, 20)

        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = PropertyMock(return_value=mock_line_data)
        mock_column.formatter_args = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        column_widths = [10]

        instance = DisplayLine([mock_column], mock_data)
        instance._column_widths = column_widths

        expected_result = [20]
        self.assertListEqual(
            instance.column_widths(sentinel.font, column_widths),
            expected_result)

    def test_method_column_widths_object_smaller(self):
        mock_line_data = MagicMock()
        mock_line_data.size = (20, 20)

        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = PropertyMock(return_value=mock_line_data)
        mock_column.formatter_args = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        column_widths = [40]

        instance = DisplayLine([mock_column], mock_data)
        instance._column_widths = column_widths

        expected_result = [40]
        self.assertListEqual(
            instance.column_widths(sentinel.font, column_widths),
            expected_result)

    def test_method_column_widths_object_new_column(self):
        mock_line_data = MagicMock()
        mock_line_data.size = (20, 20)

        mock_column_1 = MagicMock(spec=DisplayColumn)
        mock_column_1.align = 'left'
        mock_column_1.attribute = 'test'
        mock_column_1.colspan = 1
        mock_column_1.default = None
        mock_column_1.formatter = PropertyMock(return_value=mock_line_data)
        mock_column_1.formatter_args = None
        mock_column_1.lookup = None

        mock_column_2= MagicMock(spec=DisplayColumn)
        mock_column_2.align = 'left'
        mock_column_2.attribute = 'test'
        mock_column_2.colspan = 1
        mock_column_2.default = None
        mock_column_2.formatter = PropertyMock(return_value=mock_line_data)
        mock_column_2.formatter_args = None
        mock_column_2.lookup = None

        mock_data = MagicMock(test="test")

        column_widths = [40]

        instance = DisplayLine([mock_column_1, mock_column_2], mock_data)
        instance._column_widths = column_widths

        expected_result = [40, 20]
        self.assertListEqual(
            instance.column_widths(sentinel.font, column_widths),
            expected_result)

    def test_method_reset(self):
        mock_column = MagicMock(spec=DisplayColumn)
        mock_column.align = 'left'
        mock_column.attribute = 'test'
        mock_column.colspan = 1
        mock_column.default = None
        mock_column.formatter = None
        mock_column.lookup = None

        mock_data = MagicMock(test="test")

        instance = DisplayLine([mock_column], mock_data)

        DisplayLine.reset()

        expected_result = list()
        self.assertListEqual(instance._column_widths, expected_result)


# class TestStaticBase(unittest.TestCase):
#     """
#     Tests against the StaticBase object.
#     """
#     test_data = [
#         StartingGridEntry(1, 0, "Kobernulf Monnur"),
#         StartingGridEntry(2, 1, "Testy McTest")
#     ]
#
#     def test_init(self):
#         instance = StaticBase(self.test_data)
#         expected_value = StaticBase
#         self.assertIsInstance(instance, expected_value)
#
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame(self, mock_mpy):
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_header(self, mock_mpy, mock_font):
#         mock_font.return_value = ImageFont.load_default()
#         configuration = {
#             'heading_color': [255, 0, 0],
#             'heading_font_color': [255, 255, 255],
#             'heading_font': sentinel.font,
#             'heading_font_size': sentinel.font_size,
#             'heading_text': "Lorem Ipsum",
#             'subheading_text': "For one, for all"
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_incomplete_header(self,
#                                                     mock_mpy,
#                                                     mock_font):
#         mock_font.return_value = ImageFont.load_default()
#         configuration = {
#             'heading_color': [255, 0, 0],
#             'heading_font_color': [255, 255, 255],
#             'heading_text': "Lorem Ipsum",
#             'subheading_text': "For one, for all"
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_bad_header(self, mock_mpy, mock_font):
#         mock_font.side_effect = OSError
#         configuration = {
#             'heading_color': [255, 0, 0],
#             'heading_font_color': [255, 255, 255],
#             'heading_text': "Lorem Ipsum",
#             'subheading_text': "For one, for all"
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_font(self, mock_mpy, mock_font):
#         mock_font.return_value = ImageFont.load_default()
#         configuration = {
#             'font': sentinel.font,
#             'font_size': sentinel.font_size,
#             'font_color': [0, 0, 0]
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_incomplete_font(self,
#                                                   mock_mpy,
#                                                   mock_font):
#         mock_font.return_value = ImageFont.load_default()
#         configuration = {
#             'font': sentinel.font
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_bad_font(self, mock_mpy, mock_font):
#         mock_font.side_effect = OSError()
#         configuration = {
#             'font': sentinel.font
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_margin(self, mock_mpy):
#         configuration = {
#             'margin': 20
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_column_margin(self, mock_mpy):
#         configuration = {
#             'column_margin': 10
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.Image.open', autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_backdrop(self, mock_mpy, mock_img):
#         mock_img.return_value = Image.new('L', (800, 800))
#         configuration = {
#             'backdrop': sentinel.backdrop
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.Image.open', autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_with_backdrop_and_logo(self,
#                                                     mock_mpy,
#                                                     mock_img):
#         mock_img.return_value = Image.new('L', (800, 800))
#         configuration = {
#             'backdrop': sentinel.backdrop,
#             'logo': sentinel.logo,
#             'logo_height': 150,
#             'logo_width': 150
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)
#
#     @patch('replayenhancer.StaticBase.ImageFont.truetype',
#            autospec=True)
#     @patch('replayenhancer.StaticBase.PIL_to_npimage', autospec=True)
#     def test_method_to_frame_full_configuration(self,
#                                                 mock_mpy,
#                                                 mock_font):
#         mock_font.return_value = ImageFont.load_default()
#         configuration = {
#             'heading_color': [255, 0, 0],
#             'heading_font_color': [255, 255, 255],
#             'heading_font': sentinel.font,
#             'heading_font_size': sentinel.font_size,
#             'heading_text': "Lorem Ipsum",
#             'subheading_text': "For one, for all",
#             'font': sentinel.font,
#             'font_size': sentinel.font_size,
#             'margin': 20,
#             'column_margin': 10
#         }
#         mock_mpy.return_value = numpy.array(sentinel.test)
#         instance = StaticBase(self.test_data, **configuration)
#         expected_value = numpy.ndarray
#         self.assertIsInstance(instance.to_frame(), expected_value)

if __name__ == '__main__':
    unittest.main()
