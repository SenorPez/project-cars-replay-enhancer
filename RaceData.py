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

        self.last_time = None
        self.time_adjust = 0.0
        self.add_time = 0.0

    def add(self, packet):
        """
        Adds a new packet to the data set.
        """
        if packet.packet_type == 0:
            self.__add_telemetry_packet(packet)

    def __add_telemetry_packet(self, packet):
        if float(packet.current_time) == -1:
            self.telemetry_data.append(
                -1)
        else:
            if self.last_time is None:
                self.time_adjust = float(packet.current_time)
            elif float(packet.current_time) < self.last_time:
                self.add_time = self.last_time + self.add_time

            self.telemetry_data.append(
                packet.current_time+self.add_time-self.time_adjust)
            self.last_time = packet.current_time

    def __str__(self):
        return str(self.telemetry_data)
