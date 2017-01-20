"""
Tests RaceData.py.
"""
import sys
import unittest
from unittest.mock import MagicMock, PropertyMock, patch, sentinel

from replayenhancer.RaceData import RaceData, Driver, \
    ClassificationEntry, SectorTime


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
            "Timon Putzkerd": mock_driver_3,
            "Timon Putzkernur": mock_driver_3
        }
        self.instance.drivers = self.driver_data

    def tearDown(self):
        self.instance = None

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

    def test_property_best_lap(self):
        expected_result = 24.88
        self.assertEqual(self.instance.best_lap, expected_result)

    def test_property_best_lap_no_laps(self):
        self.instance.drivers = dict()
        self.assertIsNone(self.instance.best_lap)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported.")
    def test_property_best_lap_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_lap)

    @unittest.skipIf(sys.version_info >= (3, 5), "Not supported.")
    def test_property_best_lap_error_pre35(self):
        with patch('builtins.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_lap)

    def test_property_best_sector_1(self):
        expected_result = 2.83
        self.assertEqual(self.instance.best_sector_1, expected_result)

    def test_property_best_sector_1_no_laps(self):
        self.instance.drivers = dict()
        self.assertIsNone(self.instance.best_sector_1)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported.")
    def test_property_best_sector_1_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_1)

    @unittest.skipIf(sys.version_info >= (3, 5), "Not supported.")
    def test_property_best_sector_1_error_pre35(self):
        with patch('builtins.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_1)

    def test_property_best_sector_2(self):
        expected_result = 13.64
        self.assertEqual(self.instance.best_sector_2, expected_result)

    def test_property_best_sector_2_no_laps(self):
        self.instance.drivers = dict()
        self.assertIsNone(self.instance.best_sector_2)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported.")
    def test_property_best_sector_2_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_2)

    @unittest.skipIf(sys.version_info >= (3, 5), "Not supported.")
    def test_property_best_sector_2_error_pre35(self):
        with patch('builtins.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_2)

    def test_property_best_sector_3(self):
        expected_result = 8.37
        self.assertEqual(self.instance.best_sector_3, expected_result)

    def test_property_best_sector_3_no_laps(self):
        self.instance.drivers = dict()
        self.assertIsNone(self.instance.best_sector_3)

    @unittest.skipIf(sys.version_info < (3, 5), "Not supported.")
    def test_property_best_sector_3_error(self):
        with patch('replayenhancer.RaceData.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_3)

    @unittest.skipIf(sys.version_info >= (3, 5), "Not supported.")
    def test_property_best_sector_3_error_pre35(self):
        with patch('builtins.min') as mock_min:
            mock_min.side_effect = ValueError
            self.assertIsNone(self.instance.best_sector_3)

    @unittest.skip("I'm not smart enough to do this.")
    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_classification(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = list
        self.assertIsInstance(instance.classification, expected_result)

    def test_property_current_lap(self):
        mock_driver_1 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_1).current_lap = PropertyMock(return_value=3)

        mock_driver_2 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_2).current_lap = PropertyMock(return_value=3)

        mock_driver_3 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_3).current_lap = PropertyMock(return_value=2)

        mock_driver_4 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_4).current_lap = PropertyMock(return_value=1)

        self.instance._next_packet = MagicMock('replayenhancer.RETelemetryDataPacket.RETelemetryDataPacket', laps_in_event=10, participant_info=[
            mock_driver_1, mock_driver_2, mock_driver_3, mock_driver_4])

        expected_value = 3
        self.assertEqual(self.instance.current_lap, expected_value)

    def test_property_current_lap_overflow(self):
        mock_driver_1 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_1).current_lap = PropertyMock(return_value=11)

        mock_driver_2 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_2).current_lap = PropertyMock(return_value=10)

        mock_driver_3 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_3).current_lap = PropertyMock(return_value=6)

        mock_driver_4 = MagicMock(spec='replayenhancer.RETelemetryDataPacket.REParticipantInfo')
        type(mock_driver_4).current_lap = PropertyMock(return_value=5)

        self.instance._next_packet = MagicMock('replayenhancer.RETelemetryDataPacket.RETelemetryDataPacket', laps_in_event=10, participant_info=[
            mock_driver_1, mock_driver_2, mock_driver_3, mock_driver_4])

        expected_value = 10
        self.assertEqual(self.instance.current_lap, expected_value)

    def test_property_elapsed_time(self):
        expected_result = 0.0
        self.assertEqual(self.instance.elapsed_time, expected_result)

    def test_property_telemetry_data(self):
        expected_result = sentinel.telemetry_data
        self.assertEqual(self.instance.telemetry_data, expected_result)

    def test_property_total_laps(self):
        self.instance._next_packet = MagicMock('replayenhancer.RETelemetryDataPacket.RETelemetryDataPacket', laps_in_event=10)
        expected_value = 10
        self.assertEqual(self.instance.total_laps, expected_value)

    @unittest.skip("I'm not smart enough to do this.")
    def test_method_get_data(self):
        pass


class TestClassificationEntry(unittest.TestCase):
    """
    Unit tests for ClassificationEntry object.
    """
    instance = None

    def setUp(self):
        mock_driver = MagicMock(
            spec=Driver,
            best_lap=24.88,
            best_sector_1=2.83,
            best_sector_2=13.64,
            best_sector_3=8.37,
            laps_complete=3,
            race_time=181.00)
        mock_driver.configure_mock(name="Kobernulf Monnur")
        self.instance = ClassificationEntry(1, mock_driver, True)

    def tearDown(self):
        self.instance = None

    def test_init(self):
        expected_result = ClassificationEntry
        self.assertIsInstance(self.instance, expected_result)

    def test_property_best_lap(self):
        expected_result = 24.88
        self.assertEqual(self.instance.best_lap, expected_result)

    def test_property_best_sector_1(self):
        expected_result = 2.83
        self.assertEqual(self.instance.best_sector_1, expected_result)

    def test_property_best_sector_2(self):
        expected_result = 13.64
        self.assertEqual(self.instance.best_sector_2, expected_result)

    def test_property_best_sector_3(self):
        expected_result = 8.37
        self.assertEqual(self.instance.best_sector_3, expected_result)

    def test_property_driver(self):
        expected_result = Driver
        self.assertIsInstance(self.instance.driver, expected_result)

    def test_property_driver_name(self):
        expected_result = "Kobernulf Monnur"
        self.assertEqual(self.instance.driver_name, expected_result)

    def test_property_viewed_driver(self):
        expected_result = True
        self.assertEqual(self.instance.viewed_driver, expected_result)

    def test_property_laps_complete(self):
        expected_result = 3
        self.assertEqual(self.instance.laps_complete, expected_result)

    def test_property_calc_points_data(self):
        expected_result = ("Kobernulf Monnur", 1, 24.88)
        self.assertTupleEqual(self.instance.calc_points_data, expected_result)

    def test_property_position(self):
        expected_result = 1
        self.assertEqual(self.instance.position, expected_result)

    def test_property_race_time(self):
        expected_result = 181.00
        self.assertEqual(self.instance.race_time, expected_result)


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

    def test_property_index_setter(self):
        instance = Driver(sentinel.index, sentinel.name)
        instance.index = sentinel.new_index
        expected_result = sentinel.new_index
        self.assertEqual(instance.index, expected_result)

    def test_property_laps_complete(self):
        instance = Driver(sentinel.index, sentinel.name)
        times = [
            sentinel.time_1,
            sentinel.time_2,
            sentinel.time_3,
            sentinel.time_4,
            sentinel.time_5,
            sentinel.time_6
        ]
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

        expected_result = 2
        self.assertEqual(instance.laps_complete, expected_result)

    def test_property_laps_complete_empty(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = 0
        self.assertEqual(instance.laps_complete, expected_result)

    def test_property_lap_times(self):
        instance = Driver(sentinel.index, sentinel.name)
        times = [
            5,
            5,
            5,
            10,
            10,
            10
        ]
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

        expected_result = [15, 30]
        self.assertListEqual(instance.lap_times, expected_result)

    def test_property_lap_times_empty(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = list()
        self.assertListEqual(instance.lap_times, expected_result)

    def test_property_last_lap_invalid(self):
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

        self.assertTrue(instance.last_lap_invalid)

    def test_property_last_lap_invalid_previous_invalid(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_l1s1, 1, False),
            (sentinel.time_l1s2, 2, False),
            (sentinel.time_l1s2, 2, True),
            (sentinel.time_l1s3, 3, True),
            (sentinel.time_l2s1, 1, False),
            (sentinel.time_l2s2, 2, False),
            (sentinel.time_l2s3, 3, False)
        ]

        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid
                instance.add_sector_time(sector_time)

        self.assertFalse(instance.last_lap_invalid)

    def test_property_last_lap_invalid_no_laps(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.last_lap_invalid)

    def test_property_last_lap_time(self):
        instance = Driver(sentinel.index, sentinel.name)
        times = [
            5,
            5,
            5,
            10,
            10,
            10
        ]
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

        expected_result = 30
        self.assertEqual(instance.last_lap_time, expected_result)

    def test_property_last_lap_time_no_laps(self):
        instance = Driver(sentinel.index, sentinel.name)
        self.assertIsNone(instance.last_lap_time)

    def test_property_name(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.name
        self.assertEqual(instance.name, expected_result)

    def test_property_name_setter(self):
        instance = Driver(sentinel.index, sentinel.name)
        instance.name = sentinel.new_name
        expected_result = sentinel.new_name
        self.assertEqual(instance.name, expected_result)

    def test_property_race_time(self):
        instance = Driver(sentinel.index, sentinel.name)
        times = [
            5,
            5,
            5,
            10,
            10,
            10
        ]
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

        expected_result = 45
        self.assertEqual(instance.race_time, expected_result)

    def test_property_race_time_no_laps(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = 0.0
        self.assertEqual(instance.race_time, expected_result)

    def test_property_sector_times(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = list
        self.assertIsInstance(instance.sector_times, expected_result)

    def test_property_sector_times_values(self):
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

        self.assertEqual(len(instance.sector_times), 0)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_first(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance.sector_times), 1)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_duplicate(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)
        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance.sector_times), 1)

    def test_method_add_sector_time_invalidate_first_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_s1, 1, False),
            (sentinel.time_s2, 2, False),
            (sentinel.time_s2, 2, True),
            (sentinel.time_s3, 3, True)
        ]

        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        self.assertEqual(len(instance.sector_times), 3)
        self.assertTrue(all([sector_time.invalid for sector_time in instance.sector_times]))

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
                sector_time.invalid = invalid
                instance.add_sector_time(sector_time)

        # First lap should still be valid.
        result = [
            sector_time.invalid
            for sector_time in instance.sector_times[:3]]
        self.assertTrue(not any(result))

        # Second lap should be invalid.
        result = [
            sector_time.invalid
            for sector_time in instance.sector_times[3:]]
        self.assertTrue(all(result))

    def test_method_add_sector_time_invalidate_earlier_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_l1s1, 1, False),
            (sentinel.time_l1s2, 2, False),
            (sentinel.time_l1s2, 2, True),
            (sentinel.time_l1s3, 3, True),
            (sentinel.time_l2s1, 1, False),
            (sentinel.time_l2s2, 2, False),
            (sentinel.time_l2s3, 3, False)
        ]

        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid
                instance.add_sector_time(sector_time)

        # First lap should be invalid.
        result = [
            sector_time.invalid
            for sector_time in instance.sector_times[:3]]
        self.assertTrue(any(result))

        # Second lap should be invalid.
        result = [
            sector_time.invalid
            for sector_time in instance.sector_times[3:]]
        self.assertTrue(not all(result))


class TestSectorTime(unittest.TestCase):
    """
    Unit tests for SectorTime object.
    """
    def setUp(self):
        self.instance = SectorTime(sentinel.time, sentinel.sector, 0)

    def tearDown(self):
        self.instance = None

    def test_init(self):
        expected_result = SectorTime
        self.assertIsInstance(self.instance, expected_result)

    def test_property_sector(self):
        expected_result = sentinel.sector
        self.assertEqual(self.instance.sector, expected_result)

    def test_property_time(self):
        expected_result = sentinel.time
        self.assertEqual(self.instance.time, expected_result)

    def test_property_invalid_false(self):
        self.assertFalse(self.instance.invalid)

    def test_property_invalid_true(self):
        instance = SectorTime(sentinel.time, sentinel.sector, 128)
        self.assertTrue(instance.invalid)

    def test_property_invalid_setter(self):
        self.instance.invalid = sentinel.new_invalid
        expected_result = sentinel.new_invalid
        self.assertEqual(self.instance.invalid, expected_result)

if __name__ == "__main__":
    unittest.main()
