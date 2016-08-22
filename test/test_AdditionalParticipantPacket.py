"""
Tests AdditionalParticipantPacket.py
"""

import unittest
from _md5 import md5
import struct
from struct import pack, unpack
from unittest.mock import patch, sentinel

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

    def test_method_str(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(str(instance), expected_result)

    def test_method_repr(self):
        instance = AdditionalParticipantPacket(self.test_binary_data)
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(repr(instance), expected_result)

    #
    # def test_property_packet_type(self, mock_packet_data):
    #     instance = AdditionalParticipantPacket(mock_packet_data)
    #     expected_result = 2
    #     self.assertEqual(instance.packet_type, 2)





#     packet_file = 'assets/race21/pdata9'
#     packet = None
#
#     @classmethod
#     def setUpClass(cls):
#         with open(cls.packet_file, 'rb') as packet_data:
#             cls.packet = AdditionalParticipantPacket(packet_data.read())
#
#     @classmethod
#     def tearDownClass(cls):
#         del cls.packet
#
#     def test_property_data_hash(self):
#         self.assertEqual(
#             self.packet.data_hash,
#             "cae88077d6f9ed47618239d73b3141be")
#
#     def test_property_build_version_number(self):
#         self.assertIsInstance(self.packet.build_version_number, int)
#
#     def test_property_offset(self):
#         self.assertIsInstance(self.packet.offset, int)
#
#     def test_property_name(self):
#         self.assertIsInstance(self.packet.name, list)
#
#     @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
#     def test_property_name_values(self):
#         for name in self.packet.name:
#             with self.subTest(name=name):
#                 self.assertIsInstance(name, str)
#
#     @unittest.skipUnless(
#         sys.version_info < (3, 4),
#         "subTest not supported")
#     def test_property_name_values_nosubtest(self):
#         for name in self.packet.name:
#             self.assertIsInstance(name, str)
#
#     def test_property_packet_type(self):
#         self.assertEqual(self.packet.packet_type, 2)
#
#     def test_property_packet_length(self):
#         self.assertEqual(self.packet._packet_length, 1028)
#
#     def test_property_packet_string(self):
#         self.assertEqual(
#             self.packet._packet_string,
#             "HBB" + "64s" * 16)
#
#     def test_method_str(self):
#         self.assertEqual(
#             str(self.packet),
#             "AdditionalParticipantPacket")
#
#     def test_method_repr(self):
#         self.assertEqual(
#             str(self.packet),
#             "AdditionalParticipantPacket")
#
#
# class TestTelemetryDataPacket(unittest.TestCase):
#     """
#     Unit tests for a Telemetry Data Packet incorrectly placed into an
#     Additional Participant Packet.
#     """
#     packet_file = 'assets/race21/pdata11'
#     packet = None
#
#     def test_initialization(self):
#         with self.assertRaises(struct.error):
#             with open(self.packet_file, 'rb') as packet_data:
#                 self.packet = AdditionalParticipantPacket(
#                     packet_data.read())
#
#
# class TestParticipantPacket(unittest.TestCase):
#     """
#     Unit tests for a Participant Packet incorrectly placed into an
#     Additional Participant Packet.
#     """
#     packet_file = 'assets/race21/pdata4'
#     packet = None
#
#     def test_initialization(self):
#         with self.assertRaises(struct.error):
#             with open(self.packet_file, 'rb') as packet_data:
#                 self.packet = AdditionalParticipantPacket(
#                     packet_data.read())
#
#
# class TestGarbageData(unittest.TestCase):
#     """
#     Unit tests for data that is complete garbage.
#     It's a nice metaphor for life.
#     """
#     def test_initialization(self):
#         with self.assertRaises(struct.error):
#             garbage = os.urandom(1000)
#             self.packet = AdditionalParticipantPacket(garbage)
#
#
# class TestIncorrectPacketType(unittest.TestCase):
#     """
#     Unit tests data that is the correct length but has the wrong value
#     for packet type.
#     Note that this is a somewhat weak sanity check. Completely random
#     garbage data that is the correct length may fool this from time to
#     time.
#     """
#     _packet_length = AdditionalParticipantPacket._packet_length
#
#     def test_initialization(self):
#         with self.assertRaises(ValueError):
#
#             mostly_garbage = os.urandom(2)\
#                              +(0).to_bytes(1, sys.byteorder)\
#                              +os.urandom(self._packet_length-3)
#             self.packet = AdditionalParticipantPacket(mostly_garbage)