"""
Tests ReplayEnhancer.py
"""
from json import JSONDecodeError
from unittest.mock import patch, sentinel, mock_open
import unittest

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
        mock_json.side_effect = JSONDecodeError("Boom goes the dynamite",
                                                "Fake File",
                                                42)

        with patch('replayenhancer.ReplayEnhancer.open', mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        self.assertRaises(JSONDecodeError)

    @patch('os.path.realpath', autospec=True)
    def test_init_bad_file(self, mock_realpath):
        mock_realpath.side_effect = FileNotFoundError()

        with patch('replayenhancer.ReplayEnhancer.open', mock_open(read_data="blah"), create=True) as m:
            instance = ReplayEnhancer(sentinel.configuration_file)
        self.assertRaises(FileNotFoundError)

