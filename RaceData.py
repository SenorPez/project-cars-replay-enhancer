"""
Provides a class for the storing and management of
race data.
"""

from hashlib import md5
import json
import os.path

from glob import glob
from natsort import natsorted
from tqdm import tqdm

from AdditionalParticipantPacket import AdditionalParticipantPacket
from REParticipantPacket import REParticipantPacket \
    as ParticipantPacket
from RETelemetryDataPacket import RETelemetryDataPacket \
    as TelemetryDataPacket

class RaceData():
    """
    Represents data about the race.
    """

    _missing_participants = 0
    _update_indexes = set()
    _telemetry_waiting = list()
    _starting_grid = None
    _track_length = None
    _final_lap = False
    _race_finished = set()
    _classification = list()

    _lap_at_finish = [None for _ in range(56)]

    def __init__(self, telemetry_directory,
                 replay=None,
                 descriptor_file='descriptor.json'):
        self.telemetry_directory = telemetry_directory
        self.replay = replay
        self.descriptor_file = descriptor_file
        self.participant_list = dict()

        try:
            with open(os.path.join(
                os.path.realpath(self.telemetry_directory),
                os.path.relpath(descriptor_file))) as desc_file:
                self.descriptor = json.load(desc_file)
        except FileNotFoundError:
            self.__build_descriptor(descriptor_file)
        except ValueError:
            self.__build_descriptor(descriptor_file)

        self.leader_index = None

        self.elapsed_time = 0.0
        self.add_time = 0.0

        self.max_name_dimensions_value = None
        self.max_short_name_dimensions_value = None

        self.sector_times = [list() for _ in range(56)]
        self.valid_laps = [set() for _ in range(56)]
        self.invalid_laps = [set() for _ in range(56)]

        self.telemetry_data = self.__get_telemetry_data(
            race_start=self.descriptor['race_start'])
        self.packet = None

    def __build_descriptor(self,
                           descriptor_file='descriptor.json'):
        self.descriptor = {
            'race_end': None,
            'race_finish': None,
            'race_start': None}
        telemetry_data = self.__get_telemetry_data(
            reverse=True,
            elapsed_time=False)
        progress = tqdm(
            desc='Analyzing Telemetry Data',
            total=self.packet_count,
            unit='packets')

        #Exhaust packets after the race end.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and \
                    packet.race_state == 3:
                break

        self.descriptor['race_end'] = packet.data_hash

        #Exhaust packets after the race finish.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and \
                    packet.race_state == 2:
                break

        self.descriptor['race_finish'] = packet.data_hash

        #Exhaust packets after the green flag.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and (
                    packet.race_state == 0 or \
                    packet.race_state == 1):
                break

        #Exhaust packets before the race start.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and (
                    packet.session_state != 5 or \
                    packet.game_state != 2):
                break

        progress.close()
        self.descriptor['race_start'] = packet.data_hash
        with open(os.path.join(
            os.path.realpath(self.telemetry_directory),
            os.path.relpath(descriptor_file)), 'w') as desc_file:
            json.dump(self.descriptor, desc_file)

    @property
    def packet_count(self):
        """
        Returns the number of packets in a telemetry directory.
        """
        return len(glob(self.telemetry_directory+os.sep+'pdata*'))

    def __get_telemetry_data(self, reverse=False, \
                             race_start=None, elapsed_time=True):
        find_start = False if race_start is None else True
        find_populate = False
        last_packet = None
        new_packet = None

        for packet in natsorted(
                glob(self.telemetry_directory+os.sep+'pdata*'),
                reverse=reverse):
            with open(packet, 'rb') as packet_file:
                packet_data = packet_file.read()

            #TODO: This seems messy. Maybe clean?
            if md5(packet_data).hexdigest() == race_start and \
                    find_start:
                find_start = False
                find_populate = True
            elif md5(packet_data).hexdigest() != race_start and \
                    find_start:
                continue

            if find_populate and len(packet_data) == 1367:
                new_packet = TelemetryDataPacket(packet_data)
                if not any([participant.race_position \
                        for participant \
                        in new_packet.participant_info]):
                    continue
                else:
                    find_populate = False

            if len(packet_data) == 1347:
                yield ParticipantPacket(packet_data)
            elif len(packet_data) == 1028:
                yield AdditionalParticipantPacket(packet_data)
            elif len(packet_data) == 1367:
                last_packet = new_packet
                new_packet = TelemetryDataPacket(packet_data)

                if elapsed_time:
                    if new_packet.current_time == -1.0:
                        self.elapsed_time = 0.0
                        self.add_time = 0.0
                        last_packet = None
                    else:
                        if last_packet is not None and \
                                last_packet.current_time > \
                                new_packet.current_time:
                            self.add_time += last_packet.current_time

                        self.elapsed_time = \
                            self.add_time + new_packet.current_time

                yield TelemetryDataPacket(packet_data)
            else:
                raise ValueError("Malformed or unrecognized packet.")

    def race_time(self, driver_index):
        """
        Returns the race time for a driver.
        """
        race_time = sum(self.lap_time(driver_index))
        return race_time if race_time != 0 else None

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

    def laps_completed(self, driver_index):
        """
        Returns the number of laps completed.
        """
        return len(self.lap_time(driver_index))

    def sector_time(self, sector, driver_index, lap_number=None):
        """
        Returns sector times for a driver, specified by sector and
        driver_index.

        Pass lap_number to return a specific lap.
        """
        if sector < 1 or sector > 3:
            raise ValueError("Invalid Sector Number.")

        sector_times = [time for time, _ in \
            self.sector_times[driver_index]][sector-1::3]

        if lap_number is None:
            return sector_times
        else:
            return sector_times[lap_number-1]

    def best_race_time(self):
        """
        Returns the best race time in the race.
        """
        return min([self.race_time(driver_index) \
            for driver_index, _ \
            in enumerate(self.sector_times) \
            if self.race_time(driver_index) is not None])

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

    def best_sector_time(self, sector, driver_index=None):
        """
        Returns the best sector time or times in the race.

        sector should be 1, 2, or 3.
        Pass driver_index to return the best time for that index.
        """
        if sector < 1 or sector > 3:
            raise ValueError("Invalid Sector Number.")

        best_sectors = [
            min(self.sector_time(sector, driver_index))
            for driver_index, sector_times \
            in enumerate(self.sector_times) \
            if len(sector_times)]

        if driver_index is None:
            return min([time for time in best_sectors \
                if time is not None])
        else:
            return best_sectors[driver_index]

    def points(self, finish_position, driver_name=None):
        """
        Returns the number of points earned in the race.
        """
        if self.replay is None:
            return 0

        finish_position_points = 0
        try:
            finish_position_points = \
                self.replay.point_structure[finish_position]
        except IndexError:
            pass

        fast_lap_points = 0
        if driver_name is not None and \
                self.best_lap_time(
                        self.get_participant_index(driver_name)) \
                        == self.best_lap_time():
            fast_lap_points = self.replay.point_structure[0]

        return finish_position_points+fast_lap_points

    def series_points(self, finish_position, driver_name=None):
        """
        Returns the number of series points.
        """
        if self.replay is None:
            return 0

        previous_points = 0
        try:
            previous_points = self.replay.points[driver_name]
        except IndexError:
            pass

        return self.points(
            finish_position,
            driver_name)+previous_points

    def get_data(self, at_time=None, get_next=False):
        """
        Returns the telemetry data. If at_time is provided, the
        time index is used to determine which data packet to return.

        If get_next is provided, the next packet in the data set is
        returned.

        If no index is provided, the first data is provided.
        """
        if self.packet is None:
            packet = next(self.telemetry_data)
            self.packet = packet
        elif get_next:
            packet = next(self.telemetry_data)
        elif at_time is None:
            return self.packet
        elif len(self._telemetry_waiting):
            self._telemetry_waiting = \
                [(packet, elapsed_time) for packet, elapsed_time \
                in self._telemetry_waiting if elapsed_time >= at_time]
            try:
                packet, self.elapsed_time = \
                    self._telemetry_waiting.pop(0)
            except IndexError:
                try:
                    while self.elapsed_time <= at_time:
                        packet = next(self.telemetry_data)
                except StopIteration:
                    return self.packet
        else:
            try:
                while self.elapsed_time <= at_time:
                    packet = next(self.telemetry_data)

            except StopIteration:
                return self.packet

        try:
            self.__dispatch(packet)
        except UnboundLocalError:
            pass
        return self.packet

    def __dispatch(self, packet):
        if packet.packet_type == 0:
            self.__add_telemetry_packet(packet)
        elif packet.packet_type == 1:
            self.__add_participant_packet(packet)
        elif packet.packet_type == 2:
            self.__add_participant_packet(packet)
        else:
            raise ValueError("Malformed or unknown packet.")

    def __add_telemetry_packet(self, packet):
        if self.packet.num_participants == packet.num_participants and \
                len(self.participant_list) >= \
                self.packet.num_participants:
            self.packet = packet
        else:
            self.packet = packet
            self.participant_list = dict()
            self.__rebuild_participants()

        if self.packet.event_type == 'time':
            #TODO: Time.
            pass

        for index, name in self.participant_list.items():
            self.packet.participant_info[index].name = name
            self.packet.participant_info[index].index = index

            try:
                self.packet.participant_info[index].team = \
                    self.replay.team_data[name]
            except (AttributeError, KeyError):
                self.packet.participant_info[index].team = None

            try:
                self.packet.participant_info[index].car = \
                    self.replay.car_data[name]
            except (AttributeError, KeyError):
                self.packet.participant_info[index].car = None

            try:
                self.packet.participant_info[index].car_class \
                    = [car_class for car_class, data \
                    in self.replay.car_classes.items() \
                    if self.replay.car_data[name] in data['cars']][0]
            except (AttributeError, KeyError):
                self.packet.participant_info[index].car_class = None

            for telemetry_packet, _ in self._telemetry_waiting:
                telemetry_packet.participant_info[index].name = name
                telemetry_packet.participant_info[index].index = index

                try:
                    telemetry_packet.participant_info[index].team = \
                        self.replay.team_data[name]
                except (AttributeError, KeyError):
                    telemetry_packet.participant_info[index].team = None

                try:
                    telemetry_packet.participant_info[index].car = \
                        self.replay.car_data[name]
                except (AttributeError, KeyError):
                    telemetry_packet.participant_info[index].car = None

                try:
                    self.packet.participant_info[index].car_class \
                        = [car_class \
                            for car_class, data \
                            in self.replay.car_classes.items() \
                        if self.replay.car_data[name] \
                        in data['cars']][0]
                except (AttributeError, KeyError):
                    self.packet.participant_info[index].car_class = None

        for participant_index in range(56):
            participant_info = \
                self.packet.participant_info[participant_index]

            if participant_info.race_position == 1:
                self.leader_index = participant_index

                if self.packet.event_type == 'laps' and \
                        participant_info.laps_completed >= \
                        self.packet.event_duration:
                    self._final_lap = True

                    if not any(self._lap_at_finish):
                        self._lap_at_finish = [
                            self.packet.participant_info[index].\
                            current_lap \
                            for index in range(56)]
                        #Need to decrement the P1 lap so that it's
                        #processed below.
                        self._lap_at_finish[participant_index] -= 1

            sector_time = (
                participant_info.last_sector_time,
                participant_info.sector)

            try:
                if sector_time != \
                        self.sector_times[participant_index][-1] \
                        and \
                        participant_info.last_sector_time != -123 \
                        and \
                        participant_info.sector != 0:
                    self.sector_times[participant_index].append(
                        sector_time)
            except IndexError:
                if participant_info.last_sector_time != -123 and \
                        participant_info.sector != 0:
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

            if participant_info.sector == 1 and \
                    self._final_lap and \
                    participant_index not in self._race_finished and \
                    participant_info.current_lap > \
                    self._lap_at_finish[participant_index]:
                classification = (
                    participant_index,
                    self.packet.participant_info[participant_index].\
                        name,
                    self.packet.participant_info[participant_index].\
                        team,
                    self.packet.participant_info[participant_index].\
                        car,
                    self.packet.participant_info[participant_index].\
                        car_class,
                    self.laps_completed(participant_index),
                    self.race_time(participant_index),
                    self.best_lap_time(participant_index),
                    self.best_sector_time(1, participant_index),
                    self.best_sector_time(2, participant_index),
                    self.best_sector_time(3, participant_index))

                self._classification.append(classification)
                self._race_finished.add(participant_index)

    def __rebuild_participants(self):
        self._telemetry_waiting = list()
        self.participant_list = dict()
        while len(self.participant_list) < \
                self.packet.num_participants:
            packet = next(self.telemetry_data)

            if packet.packet_type == 0:
                self._telemetry_waiting.append(
                    (packet, self.elapsed_time))
            elif packet.packet_type == 1:
                self.__dispatch(packet)
            elif packet.packet_type == 2:
                self.__dispatch(packet)
            else:
                raise ValueError("Malformed or unknown packet.")

    def __add_participant_packet(self, packet):
        if packet.packet_type == 1:
            for i, name in enumerate(packet.name):
                self.participant_list[i] = name
        elif packet.packet_type == 2:
            for i, name in enumerate(packet.name, packet.offset):
                self.participant_list[i] = name

    def get_participant_index(self, participant_name):
        """
        Given participant_name, finds the corresponding index.
        """
        matches = [(index, name) for index, name \
            in self.participant_list.items() \
            if name == participant_name]

        index, _ = matches[0]
        return index

    def process_all(self):
        """
        Processes all packets in telemetry directory.
        Should probably be used only for testing. Maybe.
        """
        progress = tqdm(
            desc='Processing All Telemetry Data',
            total=self.packet_count,
            unit='packets')

        while True:
            try:
                _ = self.get_data(get_next=True)
                progress.update()
            except StopIteration:
                break

        progress.close()

    def max_name_dimensions(self, font):
        """
        Determines the maximum dimensions for names involved
        in the race.
        """
        if self.max_name_dimensions_value is None:
            telemetry_data = self.__get_telemetry_data(
                elapsed_time=False)
            names = tqdm(
                {name for packet in telemetry_data \
                    if packet.packet_type == 1 or \
                    packet.packet_type == 2 for name in packet.name},
                desc='Reading Telemetry Data Names',
                total=self.packet_count,
                unit='packets')
            height = max([font.getsize(driver)[1] for driver in names])
            width = max([font.getsize(driver)[0] for driver in names])
            self.max_name_dimensions_value = (width, height)

        return self.max_name_dimensions_value

    def max_short_name_dimensions(self, font):
        """
        Determines the maximum dimensions for names involved
        in the race.
        """
        if self.max_short_name_dimensions_value is None:
            telemetry_data = self.__get_telemetry_data(
                elapsed_time=False)
            names = tqdm(
                {self.replay.short_name_display[name] \
                    for packet in telemetry_data \
                    if packet.packet_type == 1 or \
                    packet.packet_type == 2 \
                    for name in packet.name \
                    if len(name)},
                desc='Reading Telemetry Data Names',
                total=self.packet_count,
                unit='packets')
            height = max([font.getsize(driver)[1] for driver in names])
            width = max([font.getsize(driver)[0] for driver in names])
            self.max_short_name_dimensions_value = (width, height)

        return self.max_short_name_dimensions_value

    @property
    def starting_grid(self):
        """
        Returns the starting grid for the replay.
        """
        if self._starting_grid is None:
            grid_data = RaceData(
                self.telemetry_directory,
                replay=self.replay,
                descriptor_file=self.descriptor_file)
            _ = grid_data.get_data()

            self._starting_grid = [(
                grid_data.packet.participant_info[index].\
                    race_position,
                grid_data.packet.participant_info[index].name,
                grid_data.packet.participant_info[index].team,
                grid_data.packet.participant_info[index].car,
                grid_data.packet.participant_info[index].\
                    car_class) for \
                index, name in grid_data.participant_list.items() \
                if grid_data.packet.participant_info[index].is_active]

        return self._starting_grid

    @property
    def classification(self):
        """
        Returns the classification data.
        """
        return self.class_classification(None)

    def class_classification(self, car_class):
        """
        Returns the classification data for the specified class.
        """
        if self.packet is None or \
                len(self._classification) < \
                self.packet.num_participants:
            classification_data = RaceData(
                self.telemetry_directory,
                replay=self.replay,
                descriptor_file=self.descriptor_file)

            progress = tqdm(
                desc='Determining Classification',
                total=classification_data.packet_count,
                unit='packets')

            while True:
                try:
                    _ = classification_data.get_data(get_next=True)
                    progress.update()
                except StopIteration:
                    break

            progress.close()
            self._classification = classification_data._classification

            points = classification_data.points
            series_points = classification_data.series_points

            if car_class is None:
                classification = sorted(
                    [data for data in self._classification \
                        if data[0] is not None],
                    key=lambda x: (-x[5], x[6]))
            else:
                classification = sorted(
                    [data for data in self._classification \
                        if data[0] is not None \
                        and data[4] == car_class],
                    key=lambda x: (-x[5], x[6]))
            classification = [(finish_position, driver_name)+\
                tuple(rest)+\
                (
                    points(finish_position, driver_name),
                    series_points(finish_position, driver_name)
                ) \
                for finish_position, (
                    driver_index,
                    driver_name,
                    rest) \
                in enumerate([
                    (
                        data[0],
                        data[1],
                        data[2:]
                    ) for data in classification], 1)]

            if self.replay is not None:
                for name in self.replay.additional_participants:
                    try:
                        team = self.replay.team_data[name]
                    except KeyError:
                        team = None

                    try:
                        car = self.replay.car_data[name]
                    except KeyError:
                        car = None

                    try:
                        car_class = self.replay.car_class_data[name]
                    except KeyError:
                        car_class = None

                    additional = (
                        None,
                        name,
                        team,
                        car,
                        car_class,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        0,
                        self.replay.points[name])
                    classification.append(additional)
            self._classification = classification

        return self._classification

    @property
    def track_length(self):
        """
        Returns the track length.
        """
        if self._track_length is None:
            track_data = RaceData(
                self.telemetry_directory,
                descriptor_file=self.descriptor_file)
            _ = track_data.get_data()

            self._track_length = track_data.packet.track_length

        return self._track_length
