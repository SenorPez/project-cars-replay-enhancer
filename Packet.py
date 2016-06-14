"""
Provides base class for the UDP Packets output by Project CARS.
"""

import abc
from collections import deque
from struct import unpack

class Packet(metaclass=abc.ABCMeta):
    """
    Defines base Packet class for UDP Packets output by Project CARS.
    """
    @abc.abstractmethod
    def __str__(self):
        """String representation of the packet."""

    @abc.abstractproperty
    def packet_string(self):
        """Define the binary unpacking string for the packet."""

    @abc.abstractproperty
    def packet_type(self):
        """Define the packet type number of the packet."""

    @abc.abstractproperty
    def packet_length(self):
        """Define the packet length of the raw packet data."""

    def __repr__(self):
        return self.__str__()

    def unpack_data(self, packet_data):
        """
        Unpacks the binary data according to the string that
        represents the data structure.
        """
        return deque(unpack(self.packet_string, packet_data))

    def test_packet_type(self, packet_type):
        """
        Tests the packet type against the defined packet type
        """
        try:
            packet_type = int(packet_type) & int('00000011', 2)
            if packet_type != self.packet_type:
                raise ValueError(
                    "Incorrect packet type detected." + \
                    "Packet type is {}".format(packet_type) + \
                    "Packet type should be {}".format(
                        self.packet_type))
        except ValueError:
            raise
        else:
            return True
