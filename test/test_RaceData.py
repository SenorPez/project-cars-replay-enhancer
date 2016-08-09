import json
import os
import unittest

from replayenhancer import RaceData


class TestInvalidDirectory(unittest.TestCase):
    """
    Unit tests for a directory that doesn't exist.
    """
    telemetry_data = None

    def test_invalid_directory(self):
        self.assertRaises(
            NotADirectoryError,
            lambda: RaceData.TelemetryData('fakedir'),
        )

class TestExists(object):
    def test_directory_exists(self):
        self.assertTrue(
            os.path.isdir(self.telemetry_directory))

    def test_descriptor_exists(self):
        self.assertTrue(
            os.path.exists(self.descriptor_file))

class TestRace1Telemetry(object):
    def test_descriptor_race_start(self):
        self.assertEqual(
            self.descriptor['race_start'],
            'c41bc2075b38420283507728b8391387')

    def test_descriptor_race_finish(self):
        self.assertEqual(
            self.descriptor['race_finish'],
            '8fa2d6601799e5dc042737a92d565d5d')

    def test_descriptor_race_end(self):
        self.assertEqual(
            self.descriptor['race_end'],
            'cd14b42cce4e60623462e491d9a77455')

    def test_property_packet_count(self):
        self.assertEqual(self.telemetry_data.packet_count, 10992)

    def test_property_telemetry_data(self):
        self.assertEqual(
            type(self.telemetry_data.telemetry_data),
            type((x for x in range(10))))


class TestValidDirectoryDescriptor(unittest.TestCase, TestExists, TestRace1Telemetry):
    """
    Unit tests for data that doesn't include a descriptor.
    """
    telemetry_data = None
    telemetry_directory = 'assets/race1-descriptor'
    descriptor = None
    descriptor_file = telemetry_directory+os.sep+'descriptor.json'

    @classmethod
    def setUpClass(cls):
        cls.telemetry_data = RaceData.TelemetryData(
            cls.telemetry_directory)
        cls.descriptor = json.load(open(cls.descriptor_file))

    @classmethod
    def tearDownClass(cls):
        del cls.telemetry_data
        del cls.descriptor


class TestValidDataNoDescriptor(unittest.TestCase, TestExists, TestRace1Telemetry):
    """
    Unit tests for data that doesn't include a descriptor.
    """
    telemetry_data = None
    telemetry_directory = 'assets/race1-no-descriptor'
    descriptor = None
    descriptor_file = telemetry_directory+os.sep+'descriptor.json'

    @classmethod
    def setUpClass(cls):
        cls.telemetry_data = RaceData.TelemetryData(
            'assets/race1-no-descriptor')
        cls.descriptor = json.load(open(
            'assets/race1-no-descriptor/descriptor.json'))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.descriptor_file)
        del cls.telemetry_data
        del cls.descriptor

if __name__ == "__main__":
    unittest.main()
