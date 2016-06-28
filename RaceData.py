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
    _participant_list = dict()
    _update_indexes = set()

    def __init__(self):
        self.telemetry_data = list()
        self.sector_times = [list() for _ in range(56)]
        self.invalid_laps = [set() for _ in range(56)]

    def lap_time(self, driver_index, lap_number=None):
        """
        Returns lap times for a driver, specified by driver_index.

        Pass lap_number to limit the list to that lap or earlier.
        """
        lap_times = [sum(self.sector_times[driver_index][i:i+3]) \
            for i in range(0, len(self.sector_times[driver_index]), 3)]
        if lap_number is None:
            return lap_times
        else:
            return lap_times[lap_number-1]

    def best_lap_time(self, driver_index=None, lap_number=None):
        """
        Returns the best lap time or times in the race.

        Pass driver_index to return the best time or times for 
            that index.
        Pass lap_number to return the best time or times for that lap
            or earlier.
        """
        best_laps = list()
        for index, _ in enumerate(self.sector_times):
            best_laps.append(min(self.lap_time(index)[:lap_number]))

        if driver_index is None:
            return min([x for x in best_laps if x != 0])
        else:
            return best_laps[driver_index]

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
                self.telemetry_data.append(packet)
                if len(self._participant_list) >= \
                        packet.num_participants:
                    for index, name in self._participant_list.items():
                        self.telemetry_data[-1].\
                            participant_info[index].name = name
                        self.telemetry_data[-1].\
                            participant_info[index].index = index

                        for telemetry_index in self._update_indexes:
                            self.telemetry_data[telemetry_index].\
                                participant_info[index].name = name
                            self.telemetry_data[telemetry_index].\
                                participant_info[index].index = index
                    self._update_indexes = set()

                else:
                    self._update_indexes.add(len(self.telemetry_data))
            else:
                self.telemetry_data.append(packet)
                self._participant_list = dict()
        else:
            self.telemetry_data.append(packet)

        last_packet = self.telemetry_data[-1]
        for index, participant in enumerate(
                last_packet.participant_info):
            if participant.invalid_lap and \
                    participant.last_sector_time != -123:
                self.invalid_laps[index].add(
                    participant.current_lap)

            sector_times = self.sector_times[index]
            try:
                if sector_times[-1] != \
                        participant.last_sector_time and \
                        len(sector_times) % 3 != \
                            participant.sector and \
                        participant.last_sector_time != -123:
                    sector_times.append(participant.last_sector_time)
            except IndexError:
                if participant.last_sector_time != -123:
                    sector_times.append(participant.last_sector_time)

    def __add_participant_packet(self, packet):
        if packet.packet_type == 1:
            for i, name in enumerate(packet.name):
                self._participant_list[i] = name

        elif packet.packet_type == 2:
            for i, name in enumerate(packet.name, packet.offset):
                self._participant_list[i] = name

    def __str__(self):
        return str([(x.current_time, x.elapsed_time) \
            for x in self.telemetry_data])
