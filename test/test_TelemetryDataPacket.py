"""Tests TelemetryDataPacket.py

"""
import unittest
from collections import deque

from replayenhancer.TelemetryDataPacket import ParticipantInfo


class TestParticipantInfo(unittest.TestCase):
    """Unit tests against the ParticipantInfo object.

    """
    from random import choice, random, randrange
    expected_world_position = [
        randrange(100)+choice([0, 0.25, 0.50, 0.75]),
        randrange(100),
        randrange(100) + choice([0, 0.25, 0.50, 0.75])]
    expected_current_lap_distance = randrange(100)
    expected_is_active = 1
    expected_race_position = randrange(56)
    expected_invalid_lap = 0
    expected_laps_completed = randrange(50)
    expected_current_lap = expected_laps_completed + 1
    expected_sector = randrange(1, 4)
    expected_last_sector_time = random()

    @classmethod
    def binary_data(cls, **kwargs):
        test_data = list()

        try:
            world_position = kwargs['world_position']
        except KeyError:
            world_position = cls.expected_world_position

        test_data.extend([int(num) for num in world_position])

        try:
            test_data.append(kwargs['current_lap_distance'])
        except KeyError:
            test_data.append(cls.expected_current_lap_distance)

        try:
            is_active = kwargs['is_active']
        except KeyError:
            is_active = cls.expected_is_active

        try:
            race_position = kwargs['race_position']
        except KeyError:
            race_position = cls.expected_race_position

        test_data.append((is_active << 7) + race_position)

        try:
            invalid_lap = kwargs['invalid_lap']
        except KeyError:
            invalid_lap = cls.expected_invalid_lap

        try:
            laps_completed = kwargs['laps_completed']
        except KeyError:
            laps_completed = cls.expected_laps_completed

        test_data.append((invalid_lap << 7) + laps_completed)

        try:
            test_data.append(kwargs['current_lap'])
        except KeyError:
            test_data.append(cls.expected_current_lap)

        try:
            sector = kwargs['sector']
        except KeyError:
            sector = cls.expected_sector

        x_acc = int(((world_position[0] - int(world_position[0])) * 100) / 25)
        z_acc = int(((world_position[2] - int(world_position[2])) * 100) / 25)
        test_data.append((z_acc << 5) + (x_acc << 3) + sector)

        try:
            test_data.append(kwargs['last_sector_time'])
        except KeyError:
            test_data.append(cls.expected_last_sector_time)

        return deque(tuple(test_data))

    def test_init(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = ParticipantInfo
        self.assertIsInstance(instance, expected_result)

    def test_property_current_lap(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_current_lap
        self.assertEqual(instance.current_lap, expected_result)

    def test_property_current_lap_distance(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_current_lap_distance
        self.assertEqual(instance.current_lap_distance, expected_result)

    def test_property_invalid_lap_false(self):
        instance = ParticipantInfo(self.binary_data(invalid_lap=0))
        self.assertFalse(instance.invalid_lap)

    def test_property_invalid_lap_true(self):
        instance = ParticipantInfo(self.binary_data(invalid_lap=1))
        self.assertTrue(instance.invalid_lap)

    def test_property_invalid_lap_false_negative_at_race_start(self):
        instance = ParticipantInfo(self.binary_data(
            invalid_lap=1,
            sector=3,
            last_sector_time=-123))
        self.assertFalse(instance.invalid_lap)

    def test_property_is_active_false(self):
        instance = ParticipantInfo(self.binary_data(is_active=0))
        self.assertFalse(instance.is_active)

    def test_property_is_active_true(self):
        instance = ParticipantInfo(self.binary_data(is_active=1))
        self.assertTrue(instance.is_active)

    def test_property_laps_completed(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_laps_completed
        self.assertEqual(instance.laps_completed, expected_result)

    def test_property_last_sector_time(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_last_sector_time
        self.assertEqual(instance.last_sector_time, expected_result)

    def test_property_race_position(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_race_position
        self.assertEqual(instance.race_position, expected_result)

    def test_property_sector(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_sector
        self.assertEqual(instance.sector, expected_result)

    def test_property_world_position(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_world_position
        self.assertListEqual(instance.world_position, expected_result)