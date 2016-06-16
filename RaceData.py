"""
Provides a class for the storing and management of
race data.
"""

from tqdm import tqdm

class RaceData():
    """
    Represents data about the race.
    """

    _missing_participants = 0
    _participant_list = list()

    def __init__(self):
        self.telemetry_data = list()
        #self.participant_data = list()

    @property
    def track_length(self):
        """Returns the track length."""
        return self.telemetry_data[-1].track_length

    def add(self, packet):
        """
        Adds a new packet to the data set.
        """
        if packet.packet_type == 0:
            self.__add_telemetry_packet(packet)
        elif packet.packet_type == 1:
            self.__add_participant_packet(packet)
        elif packet.packet_type == 2:
            self.__add_participant_packet(packet)

    def trim_data(self):
        """
        Trims the data to the extent of the race start, finish,
        and end.
        """
        try:
            race_end = [i for i, data in tqdm(
                reversed(list(enumerate(
                    self.telemetry_data))),
                desc="Detecting Race End") \
                if data.race_state == 3][0] + 1
        except IndexError:
            race_end = len(self.telemetry_data)

        try:
            race_finish = [i for i, data in tqdm(
                reversed(list(enumerate(
                    self.telemetry_data[:race_end]))),
                desc="Detecting Race Finish") \
                if data.race_state == 2][0] + 1
        except IndexError:
            race_finish = len(self.telemetry_data)

        try:
            green_flag = [i for i, data in tqdm(
                reversed(list(enumerate(
                    self.telemetry_data[:race_finish]))),
                desc="Detecting Green Flag") \
                if data.race_state == 0 or data.race_state == 1][0]
            race_start = [i for i, data in tqdm(
                reversed(list(enumerate(
                    self.telemetry_data[:green_flag]))),
                desc="Detecting Race Start") \
                if data.session_state != 5 \
                or data.game_state != 2][0] + 1
        except IndexError:
            race_start = 0

        self.telemetry_data = self.telemetry_data[race_start:race_end]

        saved_names = list()
        for i, data in tqdm(
                reversed(list(enumerate(self.telemetry_data))),
                desc="Updating Names"):
            if not any([x.name for x in data.participant_info]):
                for index, name in enumerate(saved_names):
                    self.telemetry_data[i].\
                        participant_info[index].name = name
            saved_names = [x.name for x in data.participant_info]

    def get_data(self, at_time=None):
        """
        Returns the telemetry data. If at_time is provided, the
        time index is used to determine which data packet to return.
        If no index is provided, the first data is provided.
        """
        if at_time is None:
            output = self.telemetry_data[0]
        else:
            try:
                output = [x for x in self.telemetry_data \
                    if x.elapsed_time > at_time][0]
            except IndexError:
                output = self.telemetry_data[-1]

        return output

    def max_name_dimensions(self, font):
        """
        Determines the maximum dimensions for names involved
        in the race.
        """
        names = {x.name \
            for y in self.telemetry_data \
            for x in y.participant_info \
            if x.name is not None}
        height = max([font.getsize(driver)[1] for driver in names])
        width = max([font.getsize(driver)[0] for driver in names])
        return (width, height)

    def __add_telemetry_packet(self, packet):
        if len(self.telemetry_data):
            packet.previous_packet = self.telemetry_data[-1]

            if self.telemetry_data[-1].num_participants == \
                    packet.num_participants:
                participant_names = \
                    [x.name for x \
                    in self.telemetry_data[-1].participant_info]
                self.telemetry_data.append(packet)

                for i, name in enumerate(participant_names):
                    self.telemetry_data[-1].set_name(name, i)
            else:
                self.telemetry_data.append(packet)
        else:
            self.telemetry_data.append(packet)

    def __add_participant_packet(self, packet):
        if packet.packet_type == 1:
            for i, name in enumerate(packet.name):
                self.telemetry_data[-1].set_name(name, i)
        elif packet.packet_type == 2:
            for i, name in enumerate(packet.name, packet.offset):
                self.telemetry_data[-1].set_name(name, i)

    def __str__(self):
        return str([(x.current_time, x.elapsed_time) \
            for x in self.telemetry_data])
