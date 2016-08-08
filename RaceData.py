"""
Provides a class for the storing and management of
race data.
"""

from copy import deepcopy
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
    def __init__(self, telemetry_directory,
                 replay=None,
                 descriptor_file='descriptor.json',
                 classi=False):
        self._classification = list()
        self._missing_participants = 0
        self._update_indexes = set()
        self._telemetry_waiting = list()
        self._starting_grid = None
        self._track_length = None
        self._final_lap = False
        self._race_finished = set()
        self._classification = list()
        self._dnf_classification = list()
        self._end_sector_times = [list() for _ in range(56)]
        self._dnf_end_sector_times = list()
        self._lap_at_finish = [None for _ in range(56)]
        self._dnf_lap_at_finish = list()

        self.telemetry_directory = telemetry_directory
        self.replay = replay
        self.descriptor_file = descriptor_file
        self.participant_list = dict()

        self.driver_lookup = dict()
        self.get_names()

        self.classi = classi
        self._participant_store = None

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

        self.dnf_sector_times = list()
        self.dnf_valid_laps = list()
        self.dnf_invalid_laps = list()

        self.dnf_lookup = list()

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
        try:
            while True:
                old_packet = packet
                packet = next(telemetry_data)
                progress.update()
                if packet.packet_type == 0 and (
                        packet.session_state != 5 or \
                        packet.game_state != 2):
                    break
        #None found (no restarts?) so use the first packet.
        #It is already on `old_packet`.
        except StopIteration:
            pass

        progress.close()
        self.descriptor['race_start'] = old_packet.data_hash
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
                        in new_packet.participant_info][:new_packet.num_participants]):
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

                # yield TelemetryDataPacket(packet_data)
                yield new_packet
            else:
                raise ValueError("Malformed or unrecognized packet.")

    def race_time(self, driver_index, dataset=None):
        """
        Returns the race time for a driver.
        """
        if dataset is None:
            dataset = self.sector_times

        race_time = sum(self.lap_time(driver_index, dataset=dataset))
        return race_time if race_time != 0 else None

    def lap_time(self, driver_index, lap_number=None, dataset=None):
        """
        Returns lap times for a driver, specified by driver_index.

        Pass lap_number to return a specific lap.
        """
        if dataset is None:
            dataset = self.sector_times

        if max([len(time) for time in dataset]):
            times = dataset
        else:
            times = self._end_sector_times

        sector_times = [time for time, _ in \
            times[driver_index]]
        lap_times = [sum(times) for times in zip(
            *[iter(sector_times)]*3)]

        if lap_number is None:
            return lap_times
        else:
            try:
                return lap_times[lap_number-1]
            except IndexError:
                return 0

    def get_names(self):
        telemetry_data = self.__get_telemetry_data(
            elapsed_time=False)
        packet = next(telemetry_data)
        while packet.packet_type != 0:
            packet = next(telemetry_data)
        old_drivers = list()
        self.driver_matrix = list()
        self.driver_lookup = dict()

        progress = tqdm(
            desc='Getting names',
            total=self.packet_count,
            unit='packets')
        while True:
            try:
                new_drivers = self.pull_names(
                    telemetry_data,
                    packet.num_participants,
                    progress)
                packet = next(telemetry_data)
                while packet.packet_type != 0:
                    packet = next(telemetry_data)
                progress.update()

                if len(new_drivers) < len(old_drivers):
                    """"
                    Someone dropped out.
                    The vacated position is filled by the last
                    position.
                    """
                    for index, name in enumerate(new_drivers):
                        if new_drivers[index] != old_drivers[index]:
                            old_name = old_drivers[-1]
                            new_name = new_drivers[index]
                            compare = os.path.commonprefix(
                                [old_name, new_name])
                            self.driver_lookup[old_name] = compare
                            self.driver_lookup[new_name] = compare
                elif len(new_drivers) > len(old_drivers):
                    """
                    Someone joined.
                    The new person is added in the last position.
                    """
                    for name in new_drivers:
                        self.driver_lookup[name] = name

                old_drivers = new_drivers

            except StopIteration:
                break
        progress.close()

    def pull_names(self, telemetry_data, count, progress_bar=None):
        drivers = list()
        packet = next(telemetry_data)
        if progress_bar is not None:
            progress_bar.update()
        while len(drivers) < count:
            if packet.packet_type == 1 or \
                    packet.packet_type == 2:
                drivers.extend(
                    [name for name in packet.name])
            packet = next(telemetry_data)
            if progress_bar is not None:
                progress_bar.update()
        while (packet.packet_type == 0 and packet.num_participants == count) or \
                packet.packet_type == 1 or \
                packet.packet_type == 2:
            packet = next(telemetry_data)
            if progress_bar is not None:
                progress_bar.update()

        self.driver_matrix.append(drivers[:count])
        return drivers[:count]

    def laps_completed(self, driver_index, dataset=None):
        """
        Returns the number of laps completed.
        """
        if dataset is None:
            dataset = self.sector_times

        return len(self.lap_time(driver_index, dataset=dataset))

    def sector_time(self, sector, driver_index, lap_number=None, dataset=None):
        """
        Returns sector times for a driver, specified by sector and
        driver_index.

        Pass lap_number to return a specific lap.
        """
        if dataset is None:
            dataset = self.sector_times

        if sector < 1 or sector > 3:
            raise ValueError("Invalid Sector Number.")

        if max([len(times) for times in dataset]):
            times = dataset
        else:
            times = self._end_sector_times

        sector_times = [time for time, _ in \
            times[driver_index]][sector-1::3]

        if lap_number is None:
            return sector_times
        else:
            return sector_times[lap_number-1]

    def best_race_time(self, dataset=None):
        """
        Returns the best race time in the race.
        """
        if dataset is None:
            dataset = self.sector_times
        return min([self.race_time(driver_index, dataset=dataset) \
            for driver_index, _ \
            in enumerate(dataset) \
            if self.race_time(driver_index, dataset=dataset) is not None])

    def best_lap_time(self, driver_index=None, dataset=None):
        """
        Returns the best lap time or times in the race.

        Pass driver_index to return the best time or times for
            that index.
        """
        if dataset is None:
            dataset = self.sector_times

        if max([len(times) for times in dataset]):
            times = dataset
        else:
            times = self._end_sector_times

        best_laps = [None if len(sector_times) < 3 \
            else min(self.lap_time(driver_index, dataset=dataset)) \
            for driver_index, sector_times \
            in enumerate(times)]

        if driver_index is None:
            return min([time for time in best_laps \
                if time is not None])
        else:
            return best_laps[driver_index]

    def best_sector_time(self, sector, driver_index=None, dataset=None):
        """
        Returns the best sector time or times in the race.

        sector should be 1, 2, or 3.
        Pass driver_index to return the best time for that index.
        """
        if dataset is None:
            dataset = self.sector_times

        if sector < 1 or sector > 3:
            raise ValueError("Invalid Sector Number.")

        if max([len(times) for times in dataset]):
            times = dataset
        else:
            times = self._end_sector_times

        """
        best_sectors = [
            min(self.sector_time(sector, 0, dataset=[sector_times]))
            for driver_index, sector_times \
            in enumerate(times) \
            if len(sector_times)]
        """
        """
        best_sectors = [
            min(self.sector_time(sector, 0, dataset=[sector_times]))
            if len(self.sector_time(sector, 0, dataset=[sector_times]))
            else None
            for sector_times in times]
        """
        best_sectors = [
            min(self.sector_time(sector, driver_index, dataset=times))
            if len(self.sector_time(sector, driver_index, dataset=times))
            else None
            for driver_index, _
            in enumerate(times)]

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
            previous_points = self.replay.points[self.driver_lookup[driver_name]]
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
            self.participant_list = {index:name for index, name in self.participant_list.items() if index < self._participant_store}
        elif packet.packet_type == 2:
            self.__add_participant_packet(packet)
            self.participant_list = {index:name for index, name in self.participant_list.items() if index < self._participant_store}
        else:
            raise ValueError("Malformed or unknown packet.")

    def __add_telemetry_packet(self, packet):
        if self.packet.num_participants == packet.num_participants and \
                len(self.participant_list) == \
                self.packet.num_participants:
            self.packet = packet
        else:
            self.old_participant_list = deepcopy(self.participant_list)
            self.packet = packet
            self.__rebuild_participants(self.packet.num_participants)

            if len(self.old_participant_list) > len(self.participant_list):
                """"
                Change was caused by someone dropping out.
                Space vacated by dropout is filled by whoever was in the
                last index position.
                """
                change_found = False
                for index in range(len(self.participant_list)):
                    if self.participant_list[index] != self.old_participant_list[index]:
                        change_found = True
                        self.dnf_lookup.append(self.old_participant_list[index])

                        self._dnf_end_sector_times.append(self._end_sector_times[index])
                        self._end_sector_times[index] = self._end_sector_times[len(self.old_participant_list)-1]
                        self._end_sector_times[len(self.old_participant_list)-1] = list()

                        self._dnf_lap_at_finish.append(self._lap_at_finish[index])
                        self._lap_at_finish[index] = self._lap_at_finish[len(self.old_participant_list)-1]
                        self._lap_at_finish[len(self.old_participant_list)-1] = None

                        self.dnf_sector_times.append(self.sector_times[index])
                        self.sector_times[index] = self.sector_times[len(self.old_participant_list)-1]
                        self.sector_times[len(self.old_participant_list)-1] = list()

                        self.dnf_valid_laps.append(self.valid_laps[index])
                        self.valid_laps[index] = self.valid_laps[len(self.old_participant_list)-1]
                        self.valid_laps[len(self.old_participant_list)-1] = set()

                        self.dnf_invalid_laps.append(self.invalid_laps[index])
                        self.invalid_laps[index] = self.invalid_laps[len(self.old_participant_list)-1]
                        self.invalid_laps[len(self.old_participant_list)-1] = set()
                if not change_found:
                    """
                    Drop out was last in the list.
                    """
                    index += 1
                    self.dnf_lookup.append(self.old_participant_list[index])

                    self._dnf_end_sector_times.append(self._end_sector_times[index])
                    self._end_sector_times[index] = list()

                    self._dnf_lap_at_finish.append(self._lap_at_finish[index])
                    self._lap_at_finish[index] = None

                    self.dnf_sector_times.append(self.sector_times[index])
                    self.sector_times[index] = list()

                    self.dnf_valid_laps.append(self.valid_laps[index])
                    self.valid_laps[index] = set()

                    self.dnf_invalid_laps.append(self.invalid_laps[index])
                    self.invalid_laps[index] = set()

        if self.packet.event_type == 'time':
            #TODO: Time.
            pass

        for index, name in self.participant_list.items():
            self.packet.participant_info[index].index = index
            self.packet.participant_info[index].name = name
            if self.replay is None:
                pass
            else:
                """
                try:
                    self.packet.participant_info[index].name = \
                        self.replay.name_display[self.driver_lookup[name]]
                except KeyError:
                    self.packet.participant_info[index].name = name
                """

                try:
                    self.packet.participant_info[index].team = \
                        self.replay.team_data[self.driver_lookup[name]]
                except KeyError:
                    self.packet.participant_info[index].team = None

                try:
                    self.packet.participant_info[index].car = \
                        self.replay.car_data[self.driver_lookup[name]]
                except KeyError:
                    self.packet.participant_info[index].car = None

                try:
                    self.packet.participant_info[index].car_class \
                        = [car_class for car_class, data \
                        in self.replay.car_classes.items() \
                        if self.replay.car_data[self.driver_lookup[name]] \
                        in data['cars']][0]
                except (IndexError, KeyError):
                    self.packet.participant_info[index].car_class = None

                for telemetry_packet, _ in self._telemetry_waiting:
                    telemetry_packet.participant_info[index].name = name
                    telemetry_packet.participant_info[index].index = \
                        index

                    try:
                        telemetry_packet.participant_info[index].team = \
                            self.replay.team_data[self.driver_lookup[name]]
                    except KeyError:
                        telemetry_packet.participant_info[index].team = None

                    try:
                        telemetry_packet.participant_info[index].car = \
                            self.replay.car_data[self.driver_lookup[name]]
                    except KeyError:
                        telemetry_packet.participant_info[index].car = None

                    try:
                        self.packet.participant_info[index].car_class \
                            = [car_class \
                                for car_class, data \
                                in self.replay.car_classes.items() \
                            if self.replay.car_data[self.driver_lookup[name]]
                            in data['cars']][0]
                    except (IndexError, KeyError):
                        self.packet.participant_info[index].car_class \
                            = None

        for participant_index in range(56):
            participant_info = \
                self.packet.participant_info[participant_index]

            if participant_info.race_position == 1 and \
                    participant_index < self.packet.num_participants:
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
                elif participant_info.last_sector_time != 123 \
                        and participant_info.sector != 0:
                    pass
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

    def __rebuild_participants(self, count):
        self._telemetry_waiting = list()
        if self.packet.num_participants > 0:
            self._participant_store = self.packet.num_participants
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
            names = {
                self.replay.name_display[name]
                for name in self.driver_lookup.values()}
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
            names = {
                self.replay.short_name_display[name]
                for name in self.driver_lookup.values()}
            """
            telemetry_data = self.__get_telemetry_data(
                elapsed_time=False)
            names = tqdm(
                {self.replay.short_name_display[self.driver_lookup[name]] \
                    for packet in telemetry_data \
                    if packet.packet_type == 1 or \
                    packet.packet_type == 2 \
                    for name in packet.name \
                    if len(name)},
                desc='Reading Telemetry Data Names',
                total=self.packet_count,
                unit='packets')
            """
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
                if grid_data.packet.participant_info[index].is_active]\
                [:grid_data.packet.num_participants]
            if self.replay is not None:
                self._starting_grid = [(
                    data[0],
                    self.replay.name_display[self.driver_lookup[data[1]]])+tuple(
                    data[2:]) for data
                    in self._starting_grid]
            
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
                descriptor_file=self.descriptor_file,
                classi=True)

            """
            progress = tqdm(
                desc='Determining Classification',
                total=classification_data.packet_count,
                unit='packets')
            """

            while True:
                try:
                    _ = classification_data.get_data(get_next=True)
                    #progress.update()
                except StopIteration:
                    break

            #progress.close()

            self._classification = classification_data._classification
            self._end_sector_times = classification_data.sector_times
            points = classification_data.points
            series_points = classification_data.series_points
            dnf_lookup = classification_data.dnf_lookup
            dnf_sector_times = classification_data.dnf_sector_times
            participant_list = classification_data.participant_list
            _ = self.get_data()
        else:
            points = self.points
            series_points = self.series_points
            dnf_lookup = self.dnf_lookup
            dnf_sector_times = self.dnf_sector_times
            participant_list = self.participant_list

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
                points(
                    finish_position, 
                    driver_name),
                series_points(
                    finish_position,
                    driver_name)
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

        for index, dnf_name in [(index, name) for index, name in participant_list.items() if name not in [data[1] for data in classification]]:
            name = self.replay.name_display[self.driver_lookup[dnf_name]]

            try:
                team = self.replay.team_data[self.driver_lookup[dnf_name]]
            except KeyError:
                team = None

            try:
                car = self.replay.car_data[self.driver_lookup[dnf_name]]
            except KeyError:
                car = None

            try:
                dnf_car_class = [car_class for car_class, data \
                    in self.replay.car_classes.items() \
                    if self.replay.car_data[self.driver_lookup[dnf_name]] \
                    in data['cars']][0]
            except (IndexError, KeyError):
                dnf_car_class = None

            if dnf_car_class == car_class:
                dnf = (
                    "DNF",
                    name,
                    team,
                    car,
                    dnf_car_class,
                    self.laps_completed(index, dataset=self._end_sector_times),
                    self.race_time(index, dataset=self._end_sector_times),
                    self.best_lap_time(index, dataset=self._end_sector_times),
                    self.best_sector_time(1, index, dataset=self._end_sector_times),
                    self.best_sector_time(2, index, dataset=self._end_sector_times),
                    self.best_sector_time(3, index, dataset=self._end_sector_times),
                    0,
                    self.replay.points[self.driver_lookup[dnf_name]])
                classification.append(dnf)

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
                    add_car_class = self.replay.car_class_data[name]
                except KeyError:
                    add_car_class = None

                additional = (
                    None,
                    name,
                    team,
                    car,
                    add_car_class,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    0,
                    self.replay.points[name])

                if car_class == add_car_class:
                    classification.append(additional)

        for index, dnf_name in enumerate(dnf_lookup):
            name = self.replay.name_display[self.driver_lookup[dnf_name]]

            try:
                team = self.replay.team_data[self.driver_lookup[dnf_name]]
            except KeyError:
                team = None

            try:
                car = self.replay.car_data[self.driver_lookup[dnf_name]]
            except KeyError:
                car = None

            try:
                dnf_car_class = [car_class for car_class, data \
                    in self.replay.car_classes.items() \
                    if self.replay.car_data[self.driver_lookup[dnf_name]] \
                    in data['cars']][0]
            except (IndexError, KeyError):
                dnf_car_class = None

            if dnf_car_class == car_class:
                dnf = (
                    "DNF",
                    name,
                    team,
                    car,
                    dnf_car_class,
                    self.laps_completed(0, [dnf_sector_times[index]]),
                    self.race_time(0, [dnf_sector_times[index]]),
                    self.best_lap_time(0, [dnf_sector_times[index]]),
                    self.best_sector_time(1, 0, [dnf_sector_times[index]]),
                    self.best_sector_time(2, 0, [dnf_sector_times[index]]),
                    self.best_sector_time(3, 0, [dnf_sector_times[index]]),
                    0,
                    self.replay.points[self.driver_lookup[dnf_name]])
                classification.append(dnf)

        return classification

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
