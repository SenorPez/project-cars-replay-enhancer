"""
Provides a class for the Additional Participant Info Strings output
by Project CARS
"""

from hashlib import md5

from replayenhancer.Packet import Packet


class AdditionalParticipantPacket(Packet):
    """
    Creates an object from an additional participant info string
    packet.

    The additional participant info string packet has a length of
    1028, and is packet type 2.
    """
    def __init__(self, packet_data):
        self.data_hash = md5(packet_data).hexdigest()
        unpacked_data = self._unpack_data(packet_data)

        try:
            self.build_version_number = int(unpacked_data.popleft())

            self._test_packet_type(unpacked_data.popleft())

            self.offset = int(unpacked_data.popleft())

            self.name = list()
            for _ in range(16):
                self.name.append(
                    str(
                        unpacked_data.popleft(),
                        encoding='utf-8',
                        errors='strict').split('\x00', 1)[0])

        except ValueError:
            raise

    @property
    def packet_type(self):
        return 2

    @property
    def _packet_string(self):
        packet_string = "HBB"
        packet_string += "64s"*16

        return packet_string

    def __str__(self):
        return "AdditionalParticipantPacket"
