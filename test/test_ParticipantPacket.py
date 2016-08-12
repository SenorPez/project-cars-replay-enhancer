"""
Tests ParticipantPacket.py
"""

import os
import struct
import sys
import unittest

from replayenhancer.ParticipantPacket import ParticipantPacket


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid ParticipantPcaket.
    """
    packet_file = 'assets/race21/pdata4'
    packet = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            cls.packet = ParticipantPacket(packet_data.read())

    @classmethod
    def tearDownClass(cls):
        del cls.packet

    def test_property_data_hash(self):
        self.assertEqual(
            self.packet.data_hash,
            "04a1c8929837d8675d8ecd7a66242870")

    def test_property_build_version_number(self):
        self.assertIsInstance(self.packet.build_version_number, int)

    def test_property_car_name(self):
        self.assertIsInstance(self.packet.car_name, str)

    def test_property_car_class_name(self):
        self.assertIsInstance(self.packet.car_class_name, str)

    def test_property_track_location(self):
        self.assertIsInstance(self.packet.track_location, str)

    def test_property_track_variation(self):
        self.assertIsInstance(self.packet.track_variation, str)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_name_values(self):
        for name in self.packet.name:
            with self.subTest(name=name):
                self.assertIsInstance(name, str)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_name_values_nosubtest(self):
        for name in self.packet.name:
            self.assertIsInstance(name, str)

    def test_property_packet_type(self):
        self.assertEqual(self.packet.packet_type, 1)

    def test_property_packet_length(self):
        self.assertEqual(self.packet.packet_length, 1347)

    def test_property_packet_string(self):
        self.assertEqual(
            self.packet.packet_string,
            "HB64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64s64x")

    def test_method_str(self):
        self.assertEqual(str(self.packet), "ParticipantPacket")

    def test_method_repr(self):
        self.assertEqual(str(self.packet), "ParticipantPacket")


class TestTelemetryDataPacket(unittest.TestCase):
    """
    Unit tests for a Telemetry Data Packet incorrectly placed into a
    Participant Packet.
    """
    packet_file = 'assets/race21/pdata11'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = ParticipantPacket(packet_data.read())


class TestAdditionalParticipantPacket(unittest.TestCase):
    """
    Unit tests for an Additional Participant Packet incorrectly placed
    into a Participant Packet.
    """
    packet_file = 'assets/race21/pdata9'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = ParticipantPacket(packet_data.read())


class TestGarbageData(unittest.TestCase):
    """
    Unit tests for data that is complete garbage.
    Most things are, after all.
    """
    def test_initialization(self):
        with self.assertRaises(struct.error):
            garbage = os.urandom(1000)
            self.packet = ParticipantPacket(garbage)