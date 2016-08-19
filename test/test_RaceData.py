"""
Tests RaceData.py.
"""
import collections
import json
import os
import unittest
from unittest.mock import Mock, patch, sentinel

from replayenhancer.RaceData import RaceData, Driver
from replayenhancer.RETelemetryDataPacket \
    import RETelemetryDataPacket as TelemetryDataPacket


# class GroupExists(object):
#     """
#     Common tests against directory and descriptor existence.
#     """
#     def test_directory_exists(self):
#         self.assertTrue(
#             os.path.isdir(self.telemetry_directory))
#
#     def test_descriptor_exists(self):
#         self.assertTrue(
#             os.path.exists(self.descriptor_file))
#
#
# class GroupRace1Telemetry(object):
#     """
#     Common tests against the "race1" telemetry data.
#     """
#     def test_descriptor_race_start(self):
#         self.assertEqual(
#             self.descriptor['race_start'],
#             'c41bc2075b38420283507728b8391387')
#
#     def test_descriptor_race_finish(self):
#         self.assertEqual(
#             self.descriptor['race_finish'],
#             '8fa2d6601799e5dc042737a92d565d5d')
#
#     def test_descriptor_race_end(self):
#         self.assertEqual(
#             self.descriptor['race_end'],
#             'cd14b42cce4e60623462e491d9a77455')
#
#     def test_property_telemetry_data_packet_count(self):
#         self.assertEqual(
#             self.race_data.telemetry_data.packet_count,
#             10992)
#
#     def test_property_telemetry_data_telemetry_data(self):
#         self.assertTrue(
#             isinstance(
#                 self.race_data.telemetry_data,
#                 collections.Iterator))
#
#     def test_property_race_data_driver_lookup(self):
#         self.assertDictEqual(
#             {name: driver.real_name for name, driver
#              in self.race_data.driver_name_lookup.items()},
#             {'Bastian Schubert': 'Bastian Schubert',
#              'Kobernulf Monnur': 'Kobernulf Monnur',
#              'Friedhelm Lipps': 'Friedhelm Lipps',
#              'Brian Vang Villadsen': 'Brian Vang Villadsen',
#              'Thomas Deuerling': 'Thomas Deuerling',
#              'Scott Winstead': 'Scott Winstead',
#              'Jürgen Bell': 'Jürgen Bell',
#              'Gunars Salenieks': 'Gunars Salenieks',
#              'Timon Putzker': 'Timon Putzker',
#              'Wesley Daniel': 'Wesley Daniel',
#              'Don Damis': 'Don Damis',
#              'Jesús Carrillo Resino': 'Jesús Carrillo Resino'})
#
#     def test_property_race_data_drivers(self):
#         self.assertSetEqual(
#             self.race_data.drivers,
#             {'Bastian Schubert',
#              'Kobernulf Monnur',
#              'Friedhelm Lipps',
#              'Brian Vang Villadsen',
#              'Thomas Deuerling',
#              'Scott Winstead',
#              'Jürgen Bell',
#              'Gunars Salenieks',
#              'Timon Putzker',
#              'Wesley Daniel',
#              'Don Damis',
#              'Jesús Carrillo Resino'})
#
#     def test_property_race_data_starting_grid(self):
#         self.assertListEqual(
#             sorted(
#                 [
#                     (
#                         driver.position,
#                         driver.driver_index,
#                         driver.driver_name)
#                     for driver in self.race_data.starting_grid],
#                 key=lambda x: x[0]),
#             sorted([(1, 3, 'Gunars Salenieks'),
#                     (2, 8, 'Scott Winstead'),
#                     (3, 10, 'Thomas Deuerling'),
#                     (4, 1, 'Timon Putzker'),
#                     (5, 7, 'Wesley Daniel'),
#                     (6, 0, 'Kobernulf Monnur'),
#                     (7, 4, 'Brian Vang Villadsen'),
#                     (8, 2, 'Jesús Carrillo Resino'),
#                     (9, 6, 'Jürgen Bell'),
#                     (10, 11, 'Friedhelm Lipps'),
#                     (11, 9, 'Don Damis'),
#                     (12, 5, 'Bastian Schubert')]))
#
#     def test_property_race_data_classification_start(self):
#         self.assertListEqual(
#             sorted(
#                 [(driver.driver_index, driver.driver_name,
#                   driver.laps_completed, driver.race_time,
#                   driver.best_lap, driver.best_sector_1,
#                   driver.best_sector_2, driver.best_sector_3)
#                  for driver in self.race_data.classification],
#                 key=lambda x: (-x[2], x[3])),
#             sorted(list()))
#
#     def test_method_get_data(self):
#         exclude_values = {0.0, 267.9972839355469}
#         previous_et = 0.0
#
#         while True:
#             try:
#                 packet = self.race_data.get_data()
#                 self.assertIsInstance(packet, TelemetryDataPacket)
#                 if self.race_data.elapsed_time not in exclude_values:
#                     self.assertGreaterEqual(
#                         self.race_data.elapsed_time,
#                         previous_et)
#                 previous_et = self.race_data.elapsed_time
#             except StopIteration:
#                 break
#
#     def test_method_get_data_single(self):
#         packet = self.race_data.get_data(5.0)
#         self.assertIsInstance(packet, TelemetryDataPacket)
#         self.assertGreaterEqual(self.race_data.elapsed_time, 5.0)
#
# class GroupFA1Telemetry(object):
#     """
#     Common tests against the "fa1" telemetry data.
#     """
#     def test_descriptor_race_start(self):
#         self.assertEqual(
#             self.descriptor['race_start'],
#             '48d3836084cc549612f17dde1f45398e')
#
#     def test_descriptor_race_finish(self):
#         self.assertEqual(
#             self.descriptor['race_finish'],
#             '1b87076c8f7e262be2c0f521e7565870')
#
#     def test_descriptor_race_end(self):
#         self.assertEqual(
#             self.descriptor['race_end'],
#             'ca2ab04cec038314d4abc125acfb3109')
#
#     def test_property_telemetry_data_packet_count(self):
#         self.assertEqual(
#             self.race_data.telemetry_data.packet_count,
#             26113)
#
#     def test_property_telemetry_data_telemetry_data(self):
#         self.assertTrue(
#             isinstance(
#                 self.race_data.telemetry_data,
#                 collections.Iterator))
#
#     def test_property_race_data_driver_lookup(self):
#         self.maxDiff = None
#         self.assertDictEqual(
#             {name: driver.real_name for name, driver in
#              self.race_data.driver_name_lookup.items()},
#             {'chrand14': 'chrand14',
#              'KdeumilNL': 'KdeumilNL',
#              'tortuepirate42': 'tortuepirate42',
#              'perol825': 'perol825',
#              'Jardelmarigo': 'Jardelmarigo',
#              'Michel--NL': 'Michel--NL',
#              'Michel--NLe42': 'Michel--NL',
#              'Adolfus900': 'Adolfus',
#              'Adolfus6v': 'Adolfus',
#              'PALESCHI6v': 'PALESCHI6v',
#              'Nico451783': 'Nico451783',
#              'Finnovicrift': 'Finnovic',
#              'Finnovic7R': 'Finnovic',
#              'Dri33leE': 'Dri33leE',
#              'renaud8457R': 'renaud8457R',
#              'losfaineantos': 'losfaineantos'})
#
#     def test_property_race_data_drivers(self):
#         self.assertSetEqual(
#             self.race_data.drivers,
#             {'Adolfus',
#              'chrand14',
#              'Dri33leE',
#              'Finnovic',
#              'Jardelmarigo',
#              'KdeumilNL',
#              'losfaineantos',
#              'Michel--NL',
#              'Nico451783',
#              'PALESCHI6v',
#              'perol825',
#              'renaud8457R',
#              'tortuepirate42'})
#
#     def test_property_race_data_starting_grid(self):
#         self.assertListEqual(
#             sorted(
#                 [(driver.position, driver.driver_index,
#                   driver.driver_name)
#                  for driver in self.race_data.starting_grid],
#                 key=lambda x: x[0]),
#             sorted([(1, 0, 'PALESCHI6v'),
#                     (2, 3, 'perol825'),
#                     (3, 11, 'tortuepirate42'),
#                     (4, 2, 'KdeumilNL'),
#                     (5, 9, 'Finnovicrift'),
#                     (6, 1, 'Dri33leE'),
#                     (7, 6, 'Jardelmarigo'),
#                     (8, 7, 'renaud8457R'),
#                     (9, 10, 'Michel--NL'),
#                     (10, 4, 'chrand14'),
#                     (11, 8, 'losfaineantos'),
#                     (12, 12, 'Adolfus900'),
#                     (13, 5, 'Nico451783')]))
#
#     def test_property_race_data_classification_start(self):
#         self.assertListEqual(
#             sorted(
#                 [(driver.driver_index, driver.driver_name,
#                   driver.laps_completed, driver.race_time,
#                   driver.best_lap, driver.best_sector_1,
#                   driver.best_sector_2, driver.best_sector_3)
#                  for driver in self.race_data.classification],
#                 key=lambda x: (-x[2], x[3])),
#             sorted(list()))
#
#     def test_method_get_data(self):
#         exclude_values = {0.0, 574.8817138671875}
#         previous_et = 0.0
#
#         while True:
#             try:
#                 packet = self.race_data.get_data()
#                 self.assertIsInstance(packet, TelemetryDataPacket)
#                 if self.race_data.elapsed_time not in exclude_values:
#                     self.assertGreaterEqual(
#                         self.race_data.elapsed_time,
#                         previous_et)
#                 previous_et = self.race_data.elapsed_time
#             except StopIteration:
#                 break
#
# class TestInvalidDirectory(unittest.TestCase):
#     """
#     Unit tests for a directory that doesn't exist.
#     """
#     def test_invalid_directory(self):
#         self.assertRaises(
#             NotADirectoryError,
#             lambda: RaceData.TelemetryData('fakedir'),
#         )
#
#
# class TestValidDirectoryWithDescriptor(
#         unittest.TestCase,
#         GroupExists,
#         GroupRace1Telemetry):
#     """
#     Unit tests for data that includes a descriptor.
#     """
#     race_data = None
#     telemetry_directory = 'assets/race1-descriptor'
#     descriptor = None
#     descriptor_file = telemetry_directory+os.sep+'descriptor.json'
#
#     @classmethod
#     def setUpClass(cls):
#         cls.race_data = RaceData.RaceData(cls.telemetry_directory)
#         with open(cls.descriptor_file, 'r') as file_pointer:
#             cls.descriptor = json.load(file_pointer)
#
#     @classmethod
#     def tearDownClass(cls):
#         del cls.descriptor
#         del cls.race_data
#
#
# class TestMultiplayerWithDescriptor(
#         unittest.TestCase,
#         GroupExists,
#         GroupFA1Telemetry):
#     """
#     Unit tests for multiplayer data that includes a descriptor.
#     """
#     race_data = None
#     telemetry_directory = 'assets/fa1'
#     descriptor = None
#     descriptor_file = telemetry_directory+os.sep+'descriptor.json'
#
#     @classmethod
#     def setUpClass(cls):
#         cls.race_data = RaceData.RaceData(cls.telemetry_directory)
#         with open(cls.descriptor_file, 'r') as file_pointer:
#             cls.descriptor = json.load(file_pointer)
#
#     @classmethod
#     def tearDownClass(cls):
#         del cls.descriptor
#         del cls.race_data
#
#
# class TestValidDirectoryNoDescriptor(
#         unittest.TestCase,
#         GroupExists,
#         GroupRace1Telemetry):
#     """
#     Unit tests for data that don't include a descriptor.
#     """
#     race_data = None
#     telemetry_directory = 'assets/race1-no-descriptor'
#     descriptor = None
#     descriptor_file = telemetry_directory+os.sep+'descriptor.json'
#
#     @classmethod
#     def setUpClass(cls):
#         cls.race_data = RaceData.RaceData(cls.telemetry_directory)
#         with open(cls.descriptor_file, 'r') as file_pointer:
#             cls.descriptor = json.load(file_pointer)
#
#     @classmethod
#     def tearDownClass(cls):
#         os.remove(cls.descriptor_file)
#         del cls.descriptor
#         del cls.race_data
#

class TestDriver(unittest.TestCase):
    """
    Unit tests for Driver object.
    """
    def test_init(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = Driver
        self.assertIsInstance(instance, expected_result)

    def test_property_index(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.index
        self.assertEqual(instance.index, expected_result)

    def test_property_name(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.name
        self.assertEqual(instance.name, expected_result)

    def test_property_real_name_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.name
        self.assertEqual(instance.real_name, expected_result)

    def test_property_real_name_setter(self):
        instance = Driver(sentinel.index, sentinel.name)
        instance.real_name = sentinel.real_name
        expected_result = sentinel.real_name
        self.assertEqual(instance.real_name, expected_result)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_no_previous(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = -123.0
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 0)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_first(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 1)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_duplicate(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)
        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 1)

    def test_method_add_sector_time_invalidate_first_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [(sentinel.time_1, 1, False), (sentinel.time_2, 2, False), (sentinel.time_3, 3, True)]
        for time, sector, invalid in sectors:
            with patch('replayenhancer.RaceData.SectorTime', autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), len(sectors))
        self.assertTrue(all([sector_time.invalid for sector_time in instance._sector_times]))

    def test_method_add_sector_time_invalidate_later_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [(sentinel.time_1, 1, False), (sentinel.time_2, 2, False), (sentinel.time_3, 3, False), (sentinel.time_4, 1, False), (sentinel.time_5, 2, True)]
        for time, sector, invalid in sectors:
            with patch('replayenhancer.RaceData.SectorTime', autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        # First lap should still be valid.
        result = [sector_time.invalid for sector_time in instance._sector_times[:3]]
        self.assertTrue(not any(result), "Result: {}".format(", ".join([str(x) for x in result])))

        # Second lap should be invalid.
        result = [sector_time.invalid for sector_time in instance._sector_times[3:]]
        self.assertTrue(all(result), "Result: {}".format(", ".join([str(x) for x in result])))


if __name__ == "__main__":
    unittest.main()
