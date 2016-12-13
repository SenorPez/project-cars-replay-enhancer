"""
Provides a class for the Participant Info Strings output by
Project CARS
"""

from hashlib import md5

from replayenhancer.Packet import Packet


class ParticipantPacket(Packet):
    """
    Creates an object from a participant info string packet.

    The participant info string packet has a length of 1347, and is
    packet type 1.
    """
    def __init__(self, packet_data):
        self.data_hash = md5(packet_data).hexdigest()
        unpacked_data = self._unpack_data(packet_data)

        self.build_version_number = int(unpacked_data.popleft())

        self._test_packet_type(unpacked_data.popleft())

        self.car_name = str(
            unpacked_data.popleft(),
            encoding='utf-8',
            errors='strict').split('\x00', 1)[0]
        self.car_class_name = str(
            unpacked_data.popleft(),
            encoding='utf-8',
            errors='strict').split('\x00', 1)[0]
        self.track_location = str(
            unpacked_data.popleft(),
            encoding='utf-8',
            errors='strict').split('\x00', 1)[0]
        self.track_variation = str(
            unpacked_data.popleft(),
            encoding='utf-8',
            errors='strict').split('\x00', 1)[0]

        self.name = list()
        for _ in range(16):
            self.name.append(
                str(
                    unpacked_data.popleft(),
                    encoding='utf-8',
                    errors='strict').split('\x00', 1)[0])

    @property
    def packet_type(self):
        return 1

    @property
    def _packet_string(self):
        packet_string = "HB64s64s64s64s"
        packet_string += "64s"*16
        packet_string += "64x"

        return packet_string

    def __str__(self):
        return "ParticipantPacket"
