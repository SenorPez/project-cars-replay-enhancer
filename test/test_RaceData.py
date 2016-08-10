"""
Tests RaceData.py.
"""
import json
import os
import unittest

from replayenhancer import RaceData


class GroupExists(object):
    """
    Common tests against directory and descriptor existence.
    """
    def test_directory_exists(self):
        self.assertTrue(
            os.path.isdir(self.telemetry_directory))

    def test_descriptor_exists(self):
        self.assertTrue(
            os.path.exists(self.descriptor_file))


class GroupRace1Telemetry(object):
    """
    Common tests against the "race1" telemetry data.
    """
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

    def test_property_telemetry_data_packet_count(self):
        self.assertEqual(
            self.race_data.telemetry_data.packet_count,
            10992)

    def test_property_telemetry_data_telemetry_data(self):
        self.assertEqual(
            type(self.race_data.telemetry_data.telemetry_data),
            type((x for x in range(10))))

    def test_property_race_data_driver_lookup(self):
        self.assertDictEqual(
            self.race_data.driver_lookup,
            {'Bastian Schubert': 'Bastian Schubert',
             'Kobernulf Monnur': 'Kobernulf Monnur',
             'Friedhelm Lipps': 'Friedhelm Lipps',
             'Brian Vang Villadsen': 'Brian Vang Villadsen',
             'Thomas Deuerling': 'Thomas Deuerling',
             'Scott Winstead': 'Scott Winstead',
             'Jürgen Bell': 'Jürgen Bell',
             'Gunars Salenieks': 'Gunars Salenieks',
             'Timon Putzker': 'Timon Putzker',
             'Wesley Daniel': 'Wesley Daniel',
             'Don Damis': 'Don Damis',
             'Jesús Carrillo Resino': 'Jesús Carrillo Resino'})

    def test_property_race_data_drivers(self):
        self.assertSetEqual(
            self.race_data.drivers,
            {'Bastian Schubert',
             'Kobernulf Monnur',
             'Friedhelm Lipps',
             'Brian Vang Villadsen',
             'Thomas Deuerling',
             'Scott Winstead',
             'Jürgen Bell',
             'Gunars Salenieks',
             'Timon Putzker',
             'Wesley Daniel',
             'Don Damis',
             'Jesús Carrillo Resino'})


class TestInvalidDirectory(unittest.TestCase):
    """
    Unit tests for a directory that doesn't exist.
    """
    def test_invalid_directory(self):
        self.assertRaises(
            NotADirectoryError,
            lambda: RaceData.TelemetryData('fakedir'),
        )


class TestValidDirectoryDescriptor(
        unittest.TestCase,
        GroupExists,
        GroupRace1Telemetry):
    """
    Unit tests for data that includes a descriptor.
    """
    race_data = None
    telemetry_directory = 'assets/race1-descriptor'
    descriptor = None
    descriptor_file = telemetry_directory+os.sep+'descriptor.json'

    @classmethod
    def setUpClass(cls):
        cls.race_data = RaceData.RaceData(cls.telemetry_directory)
        cls.descriptor = json.load(open(cls.descriptor_file))

    @classmethod
    def tearDownClass(cls):
        del cls.descriptor
        del cls.race_data


class TestValidDataNoDescriptor(
        unittest.TestCase,
        GroupExists,
        GroupRace1Telemetry):
    """
    Unit tests for data that don't include a descriptor.
    """
    race_data = None
    telemetry_directory = 'assets/race1-no-descriptor'
    descriptor = None
    descriptor_file = telemetry_directory+os.sep+'descriptor.json'

    @classmethod
    def setUpClass(cls):
        cls.race_data = RaceData.RaceData(cls.telemetry_directory)
        cls.descriptor = json.load(open(cls.descriptor_file))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.descriptor_file)
        del cls.descriptor
        del cls.race_data


if __name__ == "__main__":
    unittest.main()
