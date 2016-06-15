"""
Provides a class for the storing and management of
race data.
"""

class RaceData():
    """
    Represents data about the race.
    """

    def __init__(self):
        self.telemetry_data = list()

    def add(self, packet):
        """
        Adds a new packet to the data set.
        """
        if packet.packet_type == 0:
            self.__add_telemetry_packet(packet)

    def __add_telemetry_packet(self, packet):
        if len(self.telemetry_data):
            packet.previous_packet = self.telemetry_data[-1]
            #packet.last_time = self.telemetry_data[-1].current_time

        self.telemetry_data.append(packet)

    def __str__(self):
        """
        return str([(x.last_time, x.current_time, x.elapsed_time) \
            for x in self.telemetry_data[:500]])
        """
        return str([(x.current_time, x.elapsed_time) \
            for x in self.telemetry_data])
