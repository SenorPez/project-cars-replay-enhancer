"""
Tests ReplayEnhancer.py
"""
import unittest
from unittest.mock import patch, sentinel, mock_open, MagicMock

try:
    from json import JSONDecodeError
except ImportError:
    pass

from replayenhancer.ReplayEnhancer import ReplayEnhancer


class TestReplayEnhancer(unittest.TestCase):
    """
    Tests against the ReplayEnhancer object.
    """
    @patch('json.load', autospec=True)
    @patch('os.path.realpath', autospec=True)
    def test_init(self, mock_realpath, mock_json):
        mock_realpath.return_value = sentinel.configuration_file_path
        mock_json.return_value = {
            'dummy': sentinel.dummy
        }

        with patch('replayenhancer.ReplayEnhancer.open', mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        expected_value = ReplayEnhancer
        self.assertIsInstance(instance, expected_value)

    @patch('json.load', autospec=True)
    @patch('os.path.realpath', autospec=True)
    def test_init_bad_json(self, mock_realpath, mock_json):
        mock_realpath.return_value = sentinel.configuration_file_path

        try:
            mock_json.side_effect = JSONDecodeError("Boom goes the dynamite",
                                                    "Fake File",
                                                    42)
            with patch('replayenhancer.ReplayEnhancer.open',
                       mock_open(read_data="blah"), create=True) as m:
                instance = ReplayEnhancer(sentinel.configuration_file)
                self.assertRaises(JSONDecodeError)
        except NameError:
            mock_json.side_effect = [ValueError("JSON Decoding Error")]
            with patch('replayenhancer.ReplayEnhancer.open',
                       mock_open(read_data="blah"), create=True) as m:
                instance = ReplayEnhancer(sentinel.configuration_file)
                self.assertRaises(ValueError)

    @patch('os.path.realpath', autospec=True)
    def test_init_bad_file(self, mock_realpath):
        mock_realpath.side_effect = FileNotFoundError()

        with patch('replayenhancer.ReplayEnhancer.open', mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        self.assertRaises(FileNotFoundError)

    @patch('moviepy.editor.VideoFileClip', autospec=True)
    @patch('json.load', autospec=True)
    @patch('os.path.realpath', autospec=True)
    def test_property_video(self, mock_realpath, mock_json, mock_mpy):
        mock_realpath.return_value = sentinel.configuration_file_path
        mock_json.return_value = {
            'source_video': sentinel.source_video,
            'video_skipstart': sentinel.video_skipstart,
            'video_skipend': sentinel.video_skipend
        }

        mock_mpy.return_value.subclip.return_value = sentinel.video_clipped

        with patch('replayenhancer.ReplayEnhancer.open',
                   mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        expected_value = sentinel.video_clipped
        self.assertEqual(instance.video, expected_value)    \

    @patch('moviepy.editor.VideoFileClip', autospec=True)
    @patch('json.load', autospec=True)
    @patch('os.path.realpath', autospec=True)
    def test_property_video_size(self, mock_realpath, mock_json, mock_mpy):
        mock_realpath.return_value = sentinel.configuration_file_path
        mock_json.return_value = {
            'source_video': sentinel.source_video,
            'video_skipstart': sentinel.video_skipstart,
            'video_skipend': sentinel.video_skipend
        }

        mock_mpy.return_value.subclip.return_value.size = (sentinel.video_width, sentinel.video_height)

        with patch('replayenhancer.ReplayEnhancer.open',
                   mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        expected_value = (sentinel.video_width, sentinel.video_height)

        self.assertTupleEqual(instance.video_size, expected_value)


