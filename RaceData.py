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
        self.valid_laps = [set() for _ in range(56)]
        self.invalid_laps = [set() for _ in range(56)]

    def lap_time(self, driver_index, lap_number=None):
        """
        Returns lap times for a driver, specified by driver_index.

        Pass lap_number to return a specific lap.
        """
        sector_times = [time for time, _ in \
            self.sector_times[driver_index]]
        lap_times = [sum(times) for times in zip(
            *[iter(sector_times)]*3)]

        if lap_number is None:
            return lap_times
        else:
            return lap_times[lap_number-1]

    def best_lap_time(self, driver_index=None):
        """
        Returns the best lap time or times in the race.

        Pass driver_index to return the best time or times for
            that index.
        """
        best_laps = [None if len(sector_times) < 3 \
            else min(self.lap_time(driver_index)) \
            for driver_index, sector_times \
            in enumerate(self.sector_times)]

        if driver_index is None:
            return min([time for time in best_laps \
                if time is not None])
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

    def prepare_data(self):
        """
        Prepares data for use.
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
            return self.telemetry_data[0]
            #telemetry_data = self.telemetry_data[0]
        else:
            try:
                telemetry_data = [x for x in self.telemetry_data \
                    if x.elapsed_time >= at_time][0]

            except IndexError:
                telemetry_data = [x for x in self.telemetry_data \
                    if x.elapsed_time == \
                    self.telemetry_data[-1].elapsed_time][0]

            for participant_index in range(56):
                participant_info = telemetry_data.\
                    participant_info[participant_index]
                sector_time = (
                    participant_info.last_sector_time,
                    participant_info.sector)

                try:
                    if sector_time != \
                            self.sector_times[participant_index][-1] \
                            and \
                            participant_info.last_sector_time != -123:
                        self.sector_times[participant_index].append(
                            sector_time)
                except IndexError:
                    if participant_info.last_sector_time != -123:
                        self.sector_times[participant_index].append(
                            sector_time)

                if participant_info.invalid_lap:
                    self.invalid_laps[participant_index].add(
                        participant_info.current_lap)
                    self.valid_laps[participant_index].discard(
                        participant_info.current_lap)
                else:
                    self.valid_laps[participant_index].add(
                        participant_info.current_lap)

            return telemetry_data

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
