"""
Tests AdditionalParticipantPacket.py
"""

import os
import struct
import sys
import unittest

from replayenhancer.AdditionalParticipantPacket \
    import AdditionalParticipantPacket


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid AdditionalParticipantPacket.
    """
    packet_file = 'assets/race21/pdata9'
    packet = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            cls.packet = AdditionalParticipantPacket(packet_data.read())

    @classmethod
    def tearDownClass(cls):
        del cls.packet

    def test_property_data_hash(self):
        self.assertEqual(
            self.packet.data_hash,
            "cae88077d6f9ed47618239d73b3141be")

    def test_property_build_version_number(self):
        self.assertIsInstance(self.packet.build_version_number, int)

    def test_property_offset(self):
        self.assertIsInstance(self.packet.offset, int)

    def test_property_name(self):
        self.assertIsInstance(self.packet.name, list)

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
        self.assertEqual(self.packet.packet_type, 2)

    def test_property_packet_length(self):
        self.assertEqual(self.packet.packet_length, 1028)

    def test_property_packet_string(self):
        self.assertEqual(
            self.packet.packet_string,
            "HBB" + "64s" * 16)

    def test_method_str(self):
        self.assertEqual(
            str(self.packet),
            "AdditionalParticipantPacket")

    def test_method_repr(self):
        self.assertEqual(
            str(self.packet),
            "AdditionalParticipantPacket")


class TestTelemetryDataPacket(unittest.TestCase):
    """
    Unit tests for a Telemetry Data Packet incorrectly placed into an
    Additional Participant Packet.
    """
    packet_file = 'assets/race21/pdata11'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = AdditionalParticipantPacket(
                    packet_data.read())


class TestParticipantPacket(unittest.TestCase):
    """
    Unit tests for a Participant Packet incorrectly placed into an
    Additional Participant Packet.
    """
    packet_file = 'assets/race21/pdata4'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = AdditionalParticipantPacket(
                    packet_data.read())


class TestGarbageData(unittest.TestCase):
    """
    Unit tests for data that is complete garbage.
    It's a nice metaphor for life.
    """
    def test_initialization(self):
        with self.assertRaises(struct.error):
            garbage = os.urandom(1000)
            self.packet = AdditionalParticipantPacket(garbage)