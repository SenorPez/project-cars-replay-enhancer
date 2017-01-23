"""Tests ParticipantPacket.py

"""
import unittest
from hashlib import md5
from struct import pack

from replayenhancer.ParticipantPacket import ParticipantPacket


class TestParticipantPacket(unittest.TestCase):
    """Unit tests against the ParticipantPacket object.

    """
    expected_build_version_number = 12345
    expected_packet_type = 1

    expected_car_name = "F1 W07 Hybrid"
    expected_car_class_name = "F1 2016"
    expected_track_location = "Abu Dhabi"
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

    @classmethod
    def binary_data(cls, **kwargs):
        test_data = list()
        packet_string = "HB64s64s64s64s"
        packet_string += "64s" * 16
        packet_string += "64x"

        try:
            test_data.append(kwargs['build_version_number'])
        except KeyError:
            test_data.append(cls.expected_build_version_number)

        try:
            test_data.append(kwargs['packet_type'])
        except KeyError:
            test_data.append(cls.expected_packet_type)

        try:
            test_data.append(kwargs['car_name'].encode('utf-8'))
        except KeyError:
            test_data.append(cls.expected_car_name.encode('utf-8'))

        try:
            test_data.append(kwargs['car_class_name'].encode('utf-8'))
        except KeyError:
            test_data.append(cls.expected_car_class_name.encode('utf-8'))

        try:
            test_data.append(kwargs['track_location'].encode('utf-8'))
        except KeyError:
            test_data.append(cls.expected_track_location.encode('utf-8'))

        try:
            test_data.append(kwargs['track_variation'].encode('utf-8'))
        except KeyError:
            test_data.append(cls.expected_track_variation.encode('utf-8'))

        try:
            test_data.extend([name.encode('utf-8') for name in kwargs['name']])
        except KeyError:
            test_data.extend(
                [name.encode('utf-8') for name in cls.expected_name])

        return pack(packet_string, *test_data)

    def test_init(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = ParticipantPacket
        self.assertIsInstance(instance, expected_result)

    def test_init_wrong_packet_length(self):
        test_binary_data = pack("H", 42)

        from struct import error
        with self.assertRaises(error):
            ParticipantPacket(test_binary_data)

    def test_init_wrong_packet_type(self):
        with self.assertRaises(ValueError):
            ParticipantPacket(self.binary_data(packet_type=2))

    def test_property_build_version_number(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_build_version_number
        self.assertEqual(instance.build_version_number, expected_result)

    def test_property_car_class_name(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_car_class_name
        self.assertEqual(instance.car_class_name, expected_result)

    def test_property_car_class_name_split_on_null(self):
        instance = ParticipantPacket(self.binary_data(
            car_class_name=self.expected_car_class_name + "\x00Garbage Data"))
        expected_result = self.expected_car_class_name
        self.assertEqual(instance.car_class_name, expected_result)

    def test_property_car_name(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_car_name
        self.assertEqual(instance.car_name, expected_result)

    def test_property_car_name_split_on_null(self):
        instance = ParticipantPacket(self.binary_data(
            car_class_name=self.expected_car_name + "\x00Garbage Data"))
        expected_result = self.expected_car_name
        self.assertEqual(instance.car_name, expected_result)

    def test_property_data_hash(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = md5(self.binary_data()).hexdigest()
        self.assertEqual(instance.data_hash, expected_result)

    def test_property_name(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_name_split_on_null(self):
        instance = ParticipantPacket(self.binary_data(
            name=[name+'\x00Garbage Data' for name in self.expected_name]))
        expected_result = self.expected_name
        self.assertListEqual(instance.name, expected_result)

    def test_property_packet_type(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_packet_type
        self.assertEqual(instance.packet_type, expected_result)

    def test_property_track_location(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_track_location
        self.assertEqual(instance.track_location, expected_result)

    def test_property_track_location_split_on_null(self):
        instance = ParticipantPacket(self.binary_data(
            track_location=self.expected_track_location + "\x00Garbage Data"))
        expected_result = self.expected_track_location
        self.assertEqual(instance.track_location, expected_result)

    def test_property_track_variation(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = self.expected_track_variation
        self.assertEqual(instance.track_variation, expected_result)

    def test_property_track_variation_split_on_null(self):
        instance = ParticipantPacket(self.binary_data(
            track_variation=self.expected_track_variation + "\x00Garbage Data"))
        expected_result = self.expected_track_variation
        self.assertEqual(instance.track_variation, expected_result)

    def test_method_repr(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = "ParticipantPacket"
        self.assertEqual(repr(instance), expected_result)

    def test_method_str(self):
        instance = ParticipantPacket(self.binary_data())
        expected_result = "ParticipantPacket"
        self.assertEqual(str(instance), expected_result)
