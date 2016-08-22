"""
Tests RETelemetryDataPacket.py
"""

import os
import struct
import sys
import unittest

from replayenhancer.RETelemetryDataPacket \
    import RETelemetryDataPacket, REParticipantInfo


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata11'
    packet = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            cls.packet = RETelemetryDataPacket(packet_data.read())

    @classmethod
    def tearDownClass(cls):
        del cls.packet

    def test_property_data_hash(self):
        self.assertEqual(
            self.packet.data_hash,
            "9ddd3e436527473165f0e80d214a6fcd")

    def test_property_build_version_number(self):
        self.assertIsInstance(self.packet.build_version_number, int)

    def test_property_game_state(self):
        self.assertIsInstance(self.packet.game_state, int)

    def test_property_session_state(self):
        self.assertIsInstance(self.packet.session_state, int)

    def test_property_viewed_participant_index(self):
        self.assertIsInstance(self.packet.viewed_participant_index, int)

    def test_property_num_participants(self):
        self.assertIsInstance(self.packet.num_participants, int)


    def test_property_race_state(self):
        self.assertIsInstance(self.packet.race_state, int)

    def test_property_laps_in_event(self):
        self.assertIsInstance(self.packet.laps_in_event, int)

    def test_property_current_time(self):
        self.assertIsInstance(self.packet.current_time, float)

    def test_property_event_time_remaining(self):
        self.assertIsInstance(self.packet.event_time_remaining, float)

    def test_property_track_length(self):
        self.assertIsInstance(self.packet.track_length, float)

    def test_property_packet_type(self):
        self.assertEqual(self.packet.packet_type, 0)

    def test_property_packet_length(self):
        self.assertEqual(self.packet._packet_length, 1367)

    def test_property_packet_string(self):
        self.maxDiff = None
        self.assertEqual(
            self.packet._packet_string,
            "HBBbb4xBB8xf12xf56x2xxx10x6x8x4x4x88x228x8x2x6xhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBfhhh2xBBBBffxxx")

    def test_property_participant_info(self):
        self.assertIsInstance(self.packet.participant_info, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_participant_info_values(self):
        for value in self.packet.participant_info:
            with self.subTest(item=value):
                self.assertIsInstance(value, REParticipantInfo)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_participant_info_values_nosubtest(self):
        for value in self.packet.participant_info:
            self.assertIsInstance(value, REParticipantInfo)

    def test_method_str(self):
        self.assertEqual(str(self.packet), "RETelemetryData")

    def test_method_repr(self):
        self.assertEqual(repr(self.packet), "RETelemetryData")


class TestParticipantInfo(unittest.TestCase):
    """
    Unit tests for the Participant Info object contained in the
    Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata11'
    participant_info = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            packet = RETelemetryDataPacket(packet_data.read())
            cls.participant_info = packet.participant_info

    @classmethod
    def tearDownClass(cls):
        del cls.participant_info

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_position(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.world_position, list)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_position_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.world_position, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_position_values(self):
        for participant in self.participant_info:
            for value in participant.world_position:
                with self.subTest(item=(participant, value)):
                    self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_postion_values_nosubtest(self):
        for participant in self.participant_info:
            for value in participant.world_position:
                self.assertIsInstance(value, float)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_is_active(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.is_active, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_is_active_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.is_active, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_race_position(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.race_position, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_race_position_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.race_position, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_invalid_lap(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.invalid_lap, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_invalid_lap_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.invalid_lap, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_laps_completed(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.laps_completed, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_laps_completed_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.laps_completed, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_current_lap(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.current_lap, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_current_lap_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.current_lap, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_sector(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.sector, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_sector_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.sector, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_last_sector_time(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(
                    participant.last_sector_time,
                    float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_last_sector_time_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.last_sector_time, float)


class TestAdditionalParticipantPacket(unittest.TestCase):
    """
    Unit tests for an Additional Participant Packet incorrectly placed
    into a Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata9'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = RETelemetryDataPacket(packet_data.read())


class TestParticipantPacket(unittest.TestCase):
    """
    Unit tests for a Participant Packet incorrectly placed into a
    Telemetry Data Packet
    """
    packet_file = 'assets/race21/pdata4'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = RETelemetryDataPacket(packet_data.read())


class TestGarbageData(unittest.TestCase):
    """
    Unit tests for data that is complete garbage.
    Everything turns to garbage.
    """

    def test_initialization(self):
        with self.assertRaises(struct.error):
            garbage = os.urandom(1000)
            self.packet = RETelemetryDataPacket(garbage)


class TestIncorrectPacketType(unittest.TestCase):
    """
    Unit tests data that is the correct length but has the wrong value
    for packet type.
    Note that this is a somewhat weak sanity check. Completely random
    garbage data that is the correct length may fool this from time to
    time.
    """
    packet_length = RETelemetryDataPacket._packet_length

    def test_initialization(self):
        with self.assertRaises(ValueError):
            mostly_garbage = os.urandom(2) \
                             + (1).to_bytes(1, sys.byteorder) \
                             + os.urandom(self.packet_length - 3)
            self.packet = RETelemetryDataPacket(mostly_garbage)
