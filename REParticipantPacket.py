"""
Provides a class for a Participant Info Packet, customized for use by
the Project CARS Replay Enhancer.
"""

from Packet import Packet

class REParticipantPacket(Packet):
    """
    Represents a trimmed ParticipantPacket for use by the Project
    CARS Replay Enhancers. We trim out unwanted data in order to save
    time and memory.
    """
    def __init__(self, packet_data):
        unpacked_data = self.unpack_data(packet_data)

        try:
            self.build_version_number = int(unpacked_data.popleft())

            self.test_packet_type(unpacked_data.popleft())

            self.name = list()
            for _ in range(16):
                self.name.append(
                    str(
                        unpacked_data.popleft(),
                        encoding='utf-8',
                        errors='strict').replace(
                            '\x00',
                            ''))

        except ValueError:
            raise

    @property
    def packet_type(self):
        return 1

    @property
    def packet_length(self):
        return 1347

    @property
    def packet_string(self):
        packet_string = "HB64x64x64x64x"
        packet_string += "64s"*16
        packet_string += "64x"

        return packet_string

    def __str__(self):
        return "REParticipantPacket"
