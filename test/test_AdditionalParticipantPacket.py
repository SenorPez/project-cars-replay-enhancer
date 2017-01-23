"""Tests AdditionalParticipantPacket.py

"""
import unittest
from hashlib import md5
from struct import pack

from replayenhancer.AdditionalParticipantPacket \
    import AdditionalParticipantPacket


class TestAdditionalParticipantPacket(unittest.TestCase):
    """Unit tests against the AdditionalParticipantPacket object.

    """
    expected_build_version_number = 12345
    expected_packet_type = 2

    expected_offset = 16

    expected_name = [
        "Felipe Nasr",
        "Jolyon Palmer",
        "Pascal Wehrlein",
        "Stoffel Vandoorne",
        "Esteban Gutiérrez",
        "Marcus Ericsson",
        "Esteban Ocon",
        "Rio Haryanto",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]

    expected_packet_length = 1028

    @classmethod
    def binary_data(cls, **kwargs):
        test_data = list()
        packet_string = "HBB"
        packet_string += "64s"*16

        try:
            test_data.append(kwargs['build_version_number'])
        except KeyError:
            test_data.append(cls.expected_build_version_number)

        try:
            test_data.append(kwargs['packet_type'])
        except KeyError:
            test_data.append(cls.expected_packet_type)

        try:
            test_data.append(kwargs['offset'])
        except KeyError:
            test_data.append(cls.expected_offset)

        try:
            test_data.extend([name.encode('utf-8') for name in kwargs['name']])
        except KeyError:
            test_data.extend(
                [name.encode('utf-8') for name in cls.expected_name])

        return pack(packet_string, *test_data)

    def test_init(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = AdditionalParticipantPacket
        self.assertIsInstance(instance, expected_result)

    def test_init_wrong_packet_length(self):
        test_binary_data = pack("H", 42)

        from struct import error
        with self.assertRaises(error):
            AdditionalParticipantPacket(test_binary_data)

    def test_init_wrong_packet_type(self):
        with self.assertRaises(ValueError):
            AdditionalParticipantPacket(self.binary_data(packet_type=1))

    def test_property_build_version_number(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = self.expected_build_version_number
        self.assertEqual(instance.build_version_number, expected_result)

    def test_property_data_hash(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = md5(self.binary_data()).hexdigest()
        self.assertEqual(instance.data_hash, expected_result)

    def test_property_name(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_name_split_on_null(self):
        instance = AdditionalParticipantPacket(self.binary_data(
            name=[name+'\x00Garbage Data' for name in self.expected_name]))
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_offset(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = self.expected_offset
        self.assertEqual(instance.offset, expected_result)

    def test_property_packet_type(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = self.expected_packet_type
        self.assertEqual(instance.packet_type, expected_result)

    def test_method_repr(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(repr(instance), expected_result)

    def test_method_str(self):
        instance = AdditionalParticipantPacket(self.binary_data())
        expected_result = "AdditionalParticipantPacket"
        self.assertEqual(str(instance), expected_result)
