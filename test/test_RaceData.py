"""
Tests RaceData.py.
"""
import unittest
from unittest.mock import MagicMock, PropertyMock, patch, sentinel

from replayenhancer.RaceData import RaceData, Driver


class TestRaceData(unittest.TestCase):
    """
    Tests against the RaceData object.
    """
    instance = None

    def setUp(self):
        with patch('replayenhancer.RaceData.TelemetryData') \
                as mock_telemetry_data, \
                patch('replayenhancer.RaceData.RaceData.get_data') \
                as mock_get_data:
            mock_telemetry_data.return_value = sentinel.telemetry_data
            mock_get_data.return_value = sentinel.get_data
            self.instance = RaceData(sentinel.directory)

        mock_driver_1 = MagicMock(spec=Driver)
        type(mock_driver_1).best_lap = PropertyMock(return_value=24.88)
        type(mock_driver_1).best_sector_1 = PropertyMock(return_value=2.83)
        type(mock_driver_1).best_sector_2 = PropertyMock(return_value=13.64)
        type(mock_driver_1).best_sector_3 = PropertyMock(return_value=8.37)
        type(mock_driver_1).index = PropertyMock(return_value=1)

        mock_driver_2 = MagicMock(spec=Driver)
        type(mock_driver_2).best_lap = PropertyMock(return_value=29.77)
        type(mock_driver_2).best_sector_1 = PropertyMock(return_value=3.12)
        type(mock_driver_2).best_sector_2 = PropertyMock(return_value=15.93)
        type(mock_driver_2).best_sector_3 = PropertyMock(return_value=10.67)
        type(mock_driver_2).index = PropertyMock(return_value=2)

        mock_driver_3 = MagicMock(spec=Driver)
        type(mock_driver_3).best_lap = PropertyMock(return_value=30.12)
        type(mock_driver_3).best_sector_1 = PropertyMock(return_value=3.15)
        type(mock_driver_3).best_sector_2 = PropertyMock(return_value=16.23)
        type(mock_driver_3).best_sector_3 = PropertyMock(return_value=10.70)
        type(mock_driver_3).index = PropertyMock(return_value=None)

        self.driver_data = {
            "Kobernulf Monnur": mock_driver_1,
            "Scott Winstead": mock_driver_2,
            "Timon Putzker": mock_driver_3
        }
        self.instance._drivers = self.driver_data

    def test_init(self):
        expected_result = RaceData
        self.assertIsInstance(self.instance, expected_result)

    def test_init_directory(self):
        expected_result = sentinel.directory
        self.assertEqual(self.instance._telemetry_directory, expected_result)

    def test_init_descriptor(self):
        expected_result = "descriptor.json"
        self.assertEqual(self.instance._descriptor_filename, expected_result)

    def test_init_custom_descriptor(self):
        with patch('replayenhancer.RaceData.TelemetryData') \
                as mock_telemetry_data, \
                patch('replayenhancer.RaceData.RaceData.get_data') \
                as mock_get_data:
            mock_telemetry_data.return_value = sentinel.telemetry_data
            mock_get_data.return_value = sentinel.get_data
            instance = RaceData(sentinel.directory, descriptor_filename=sentinel.descriptor)

        expected_result = sentinel.descriptor
        self.assertEqual(instance._descriptor_filename, expected_result)

    def test_property_all_drivers(self):
        expected_result = self.driver_data
        self.assertDictEqual(self.instance.all_drivers, expected_result)

    def test_property_all_drivers_empty(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.all_drivers)

    def test_property_best_lap(self):
        expected_result = 24.88
        self.assertEqual(self.instance.best_lap, expected_result)

    def test_property_best_lap_no_laps(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.best_lap)

    def test_property_best_lap_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_lap)

    def test_property_best_sector_1(self):
        expected_result = 2.83
        self.assertEqual(self.instance.best_sector_1, expected_result)

    def test_property_best_sector_1_no_laps(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.best_sector_1)

    def test_property_best_sector_1_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_1)

    def test_property_best_sector_2(self):
        expected_result = 13.64
        self.assertEqual(self.instance.best_sector_2, expected_result)

    def test_property_best_sector_2_no_laps(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.best_sector_2)

    def test_property_best_sector_2_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_2)

    def test_property_best_sector_3(self):
        expected_result = 8.37
        self.assertEqual(self.instance.best_sector_3, expected_result)

    def test_property_best_sector_3_no_laps(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.best_sector_3)

    def test_property_best_sector_3_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_3)

    def test_property_current_drivers(self):
        expected_result = {k:v for k, v in self.driver_data.items() if v.index is not None}
        self.assertDictEqual(self.instance.current_drivers, expected_result)

    def test_property_current_drivers_empty(self):
        self.instance._drivers = dict()
        self.assertIsNone(self.instance.current_drivers)

    @unittest.skip("Need further implmentation.")
    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_classification(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = list
        self.assertIsInstance(instance.classification, expected_result)

    @unittest.skip("Not sure why this broke?"
                   "Further implementation needed.")
    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_elapsed_time(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = float
        self.assertIsInstance(instance.elapsed_time, expected_result)

    @unittest.skip("Further implementation needed.")
    def test_property_starting_grid(self):
        pass

    @unittest.skip("Not sure why this broke?"
                   "Further implementation needed.")
    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_telemetry_data(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = sentinel.telemetry_data
        self.assertEqual(instance.telemetry_data, expected_result)

    @unittest.skip("Further implementation needed.")
    def test_method_get_data(self):
        pass


class TestDriver(unittest.TestCase):
    """
    Unit tests for Driver object.
    """

    def test_init(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = Driver
        self.assertIsInstance(instance, expected_result)

    def test_property_best_lap_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.best_lap)

    def test_property_best_lap_valid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (35.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 115.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_lap, expected_value)

    def test_property_best_lap_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, True),
            (35.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 117.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_lap, expected_value)

    def test_property_best_lap_all_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, True),
            (35.000, 1, True),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertIsNone(instance.best_lap)

    def test_property_best_lap_uneven(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (35.000, 1, False),
            (43.000, 2, False)
        ]
        expected_value = 115.000

        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_lap, expected_value)

    def test_property_best_lap_bad_first_sector(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (16.000, 3, False),
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (35.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 115.000

        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_lap, expected_value)

    def test_property_best_sector_1_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.best_sector_1)

    def test_property_best_sector_1_valid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 30.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_1, expected_value)

    def test_property_best_sector_1_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, True),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 33.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_1, expected_value)

    def test_property_best_sector_1_all_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, True),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, True),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = None
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_1, expected_value)

    def test_property_best_sector_2_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.best_sector_2)

    def test_property_best_sector_2_valid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 43.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_2, expected_value)

    def test_property_best_sector_2_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, True),
            (39.000, 3, False)
        ]
        expected_value = 45.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_2, expected_value)

    def test_property_best_sector_2_all_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, True),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, True),
            (39.000, 3, False)
        ]
        expected_value = None
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_2, expected_value)

    def test_property_best_sector_3_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.best_sector_3)

    def test_property_best_sector_3_valid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, False)
        ]
        expected_value = 39.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_3, expected_value)

    def test_property_best_sector_3_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, False),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, True)
        ]
        expected_value = 40.000
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_3, expected_value)

    def test_property_best_sector_3_all_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        test_data = [
            (30.000, 1, False),
            (45.000, 2, False),
            (40.000, 3, True),
            (33.000, 1, False),
            (43.000, 2, False),
            (39.000, 3, True)
        ]
        expected_value = None
        for data in test_data:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(*data)
                sector_time.time = data[0]
                sector_time.sector = data[1]
                sector_time.invalid = data[2]
                instance.add_sector_time(sector_time)

        self.assertEqual(instance.best_sector_3, expected_value)

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

    def test_property_sector_times(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = list
        self.assertIsInstance(instance.sector_times, expected_result)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_property_sector_times_values(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        times = [
            sentinel.time_1,
            sentinel.time_2,
            sentinel.time_3,
            sentinel.time_4,
            sentinel.time_5,
            sentinel.time_6
        ]
        expected_value = list()
        for sector, time in enumerate(times, 1):
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(
                    time,
                    sector % 3,
                    False)
                sector_time.sector = sector % 3
                sector_time.time = time
                sector_time.invalid = False

                instance.add_sector_time(sector_time)
                expected_value.append(sector_time)

        self.assertListEqual(instance.sector_times, expected_value)

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
        sectors = [
            (sentinel.time_s1, 1, False),
            (sentinel.time_s2, 2, False),
            (sentinel.time_s2, 2, True),
            (sentinel.time_s3, 3, False)
        ]

        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                if instance._invalidate_next_sector_count > 0:
                    sector_time.invalid = True
                else:
                    sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 3)
        self.assertTrue(all([sector_time.invalid for sector_time in instance._sector_times]))

    def test_method_add_sector_time_invalidate_later_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_l1s1, 1, False),
            (sentinel.time_l1s2, 2, False),
            (sentinel.time_l1s3, 3, False),
            (sentinel.time_l2s1, 1, False),
            (sentinel.time_l2s2, 2, False),
            (sentinel.time_l2s2, 2, True),
            (sentinel.time_l2s3, 3, True)
        ]

        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = True if instance._invalidate_next_sector_count > 0 else invalid

                instance.add_sector_time(sector_time)

        # First lap should still be valid.
        result = [
            sector_time.invalid
            for sector_time in instance._sector_times[:3]]
        self.assertTrue(not any(result))

        # Second lap should be invalid.
        result = [
            sector_time.invalid
            for sector_time in instance._sector_times[3:]]
        self.assertTrue(all(result))

if __name__ == "__main__":
    unittest.main()
