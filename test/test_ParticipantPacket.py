"""Tests ParticipantPacket.py

"""
from hashlib import md5
from struct import pack
import unittest

from replayenhancer.ParticipantPacket import ParticipantPacket


class TestParticipantPacket(unittest.TestCase):
    """Unit tests against the ParticipantPacket object.

    """
    expected_build_version_number = 12345
    expected_packet_type = 1

    expected_car_name = "Lotus 98T"
    expected_car_class_name = "Vintage F1"
    expected_track_location = "Test Track"
    expected_track_variation = "Grand Prix"

    expected_name = [
        "Nico Rosberg",
        "Lewis Hamilton",
        "Daniel Ricciardo",
        "Sebastian Vettel",
        "Max Verstappen",
        "Kimi Räikkönen",
        "Sergio Pérez",
        "Valtteri Bottas",
        "Nico Hülkenberg",
        "Fernando Alonso",
        "Felipe Massa",
        "Carlos Sainz Jr.",
        "Romain Grosjean",
        "Daniil Kvyat",
        "Jenson Button",
        "Kevin Magnussen"
    ]

    expected_packet_length = 1347
    packet_string = "HB64s64s64s64s"
    packet_string += "64s" * 16
    packet_string += "64x"

    test_data = list()
    test_data.append(expected_build_version_number)
    test_data.append(expected_packet_type)
    test_data.append(expected_car_name.encode('utf-8'))
    test_data.append(expected_car_class_name.encode('utf-8'))
    test_data.append(expected_track_location.encode('utf-8'))
    test_data.append(expected_track_variation.encode('utf-8'))
    test_data.extend([name.encode('utf-8') for name in expected_name])

    test_binary_data = pack(packet_string, *test_data)

    def test_init(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = ParticipantPacket
        self.assertIsInstance(instance, expected_result)

    def test_init_wrong_packet_length(self):
        test_binary_data = pack("H", 42)

        with self.assertRaises(ValueError):
            ParticipantPacket(test_binary_data)

    def test_init_wrong_packet_type(self):
        test_data = self.test_data
        test_data[1] = 2  # Set incorrect packet type
        test_binary_data = pack(self.packet_string, *test_data)

        with self.assertRaises(ValueError):
            ParticipantPacket(test_binary_data)

    def test_property_build_version_number(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_build_version_number
        self.assertEqual(instance.build_version_number, expected_result)

    def test_property_car_class_name(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_car_class_name
        self.assertEqual(instance.car_class_name, expected_result)

    def test_property_car_name(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_car_name
        self.assertEqual(instance.car_name, expected_result)

    def test_property_data_hash(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = md5(self.test_binary_data).hexdigest()
        self.assertEqual(instance.data_hash, expected_result)

    def test_property_name(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_packet_type(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_packet_type
        self.assertEqual(instance.packet_type, expected_result)

    def test_property_track_location(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_track_location
        self.assertEqual(instance.track_location, expected_result)

    def test_property_track_variation(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = self.expected_track_variation
        self.assertEqual(instance.track_variation, expected_result)

    def test_method_repr(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = "ParticipantPacket"
        self.assertEqual(repr(instance), expected_result)

    def test_method_str(self):
        instance = ParticipantPacket(self.test_binary_data)
        expected_result = "ParticipantPacket"
        self.assertEqual(str(instance), expected_result)
