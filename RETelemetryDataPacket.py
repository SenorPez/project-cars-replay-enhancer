"""
Provides a class for a Telemetry Data Packet, customized for use by
the Project CARS Replay Enhancer.
"""

from Packet import Packet

class RETelemetryDataPacket(Packet):
    """
    Represents a trimmed TelemetryDataPacket for use by the Project
    CARS Replay Enhancer. We trim out unwanted data in order to save
    time and memory.
    """

    _last_time = None
    _elapsed_time = 0.0
    _add_time = 0.0

    def __init__(self, packet_data):
        unpacked_data = self.unpack_data(packet_data)

        try:
            self.build_version_number = int(unpacked_data.popleft())

            self.test_packet_type(unpacked_data.popleft())

            self.current_time = float(unpacked_data.popleft())

        except ValueError:
            raise

    @property
    def packet_type(self):
        return 0

    @property
    def packet_length(self):
        return 1367

    @property
    def packet_string(self):
        """
        Original definition:
        packet_string = "HB"
        packet_string += "B"
        packet_string += "bb"
        packet_string += "BBbBB"
        packet_string += "B"
        packet_string += "21f"
        packet_string += "H"
        packet_string += "B"
        packet_string += "B"
        packet_string += "hHhHHBBBBBbffHHBBbB"
        packet_string += "22f"
        packet_string += "8B12f8B8f12B4h20H16f4H"
        packet_string += "2f"
        packet_string += "2B"
        packet_string += "bbBbbb"

        packet_string += "hhhHBBBBf"*56

        packet_string += "fBBB"
        """
        packet_string = "HB"
        packet_string += "9x"
        packet_string += "8x"
        packet_string += "f"
        packet_string += "1343x"

        return packet_string

    def previous_packet(self, packet):
        """
        Takes the previous packet, to calculate the elapsed time.
        This is a set-only property.
        """
        if self.current_time == -1.0:
            self._elapsed_time = 0.0
            self._add_time = 0.0
        else:
            self._add_time = packet.add_time
            if packet.current_time > self.current_time:
                self._add_time += packet.current_time

            self._elapsed_time = self._add_time + self.current_time
    previous_packet = property(None, previous_packet)

    @property
    def add_time(self):
        """
        Returns the time adjustment, used for calculating elapsed
        time.
        """
        return self._add_time

    @property
    def elapsed_time(self):
        """Returns the calculated elapsed time."""
        return self._elapsed_time

    def __str__(self):
        return "RETelemetryData"
