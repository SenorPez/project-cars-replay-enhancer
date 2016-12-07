"""
Tests AdditionalParticipantPacket.py
"""

import unittest
from hashlib import md5
from struct import pack
from unittest.mock import sentinel

from replayenhancer.AdditionalParticipantPacket \
    import AdditionalParticipantPacket


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid AdditionalParticipantPacket.
    """
    expected_build_version = abs(id(sentinel.build_version))
    while expected_build_version > 65535:
        expected_build_version //= 2

    expected_packet_type = 2

    expected_offset = abs(id(sentinel.offset))
    while expected_offset > 255:
        expected_offset //= 2

    expected_name = list()
    expected_name.extend([str(id(sentinel.name)) for _ in range(16)])

    packet_length = 1028
    packet_string = "HBB"
    packet_string += "64s"*16

    test_data = list()
    test_data.append(expected_build_version)
    test_data.append(expected_packet_type)
    test_data.append(expected_offset)
    test_data.extend([name.encode('utf-8') for name in expected_name])

    test_binary_data = pack(packet_string, *test_data)

    def test_init(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = AdditionalParticipantPacket
        self.assertIsInstance(instance, expected_result)

    def test_init_wrong_packet_type(self):
        test_data = self.test_data
        test_data[1] = 1  # Set incorrect packet type.

        test_binary_data = pack(self.packet_string, *test_data)

        with self.assertRaises(ValueError):
            AdditionalParticipantPacket(test_binary_data)

    def test_property_build_version(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = self.expected_build_version
        self.assertEqual(instance.build_version_number, expected_result)

    def test_property_data_hash(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = md5(self.test_binary_data).hexdigest()
        self.assertEqual(instance.data_hash, expected_result)

    def test_property_name(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = type(self.expected_name)
        self.assertIsInstance(instance.name, expected_result)

    def test_property_name_values(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_offset(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = self.expected_offset
        self.assertEqual(instance.offset, expected_result)

    def test_property_packet_type(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = self.expected_packet_type
        self.assertEqual(instance.packet_type, expected_result)

    def test_method_repr(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(repr(instance), expected_result)

    def test_method_str(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(str(instance), expected_result)
