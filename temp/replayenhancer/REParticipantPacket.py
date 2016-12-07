"""
Provides a class for the Participant Info Strings output by
Project CARS.

Customized for use by the Project CARS Replay Enhancer.
"""

from hashlib import md5

from replayenhancer.ParticipantPacket import ParticipantPacket


class REParticipantPacket(ParticipantPacket):
    # pylint: disable=super-init-not-called
    """
    Creates an object from a participant info string packet.

    The participant info string packet has a length of 1347, and is
    packet type 1.

    Customized for use by the Project CARS Replay Enhancer.
    We do not call the parent constructor.
    """
    def __init__(self, packet_data):
        self.data_hash = md5(packet_data).hexdigest()
        unpacked_data = self._unpack_data(packet_data)

        self.build_version_number = int(unpacked_data.popleft())

        self._test_packet_type(unpacked_data.popleft())

        self.name = list()
        for _ in range(16):
            self.name.append(
                str(
                    unpacked_data.popleft(),
                    encoding='utf-8',
                    errors='strict').split('\x00', 1)[0])

    @property
    def _packet_string(self):
        packet_string = "HB64x64x64x64x"
        packet_string += "64s"*16
        packet_string += "64x"

        return packet_string

    def __str__(self):
        return "REParticipantPacket"
