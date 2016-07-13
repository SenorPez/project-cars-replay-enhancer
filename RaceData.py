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
    _participant_list = dict()
    _update_indexes = set()
    _telemetry_waiting = list()

    def __init__(self, telemetry_directory,
                 descriptor_file='descriptor.json'):
        self.telemetry_directory = telemetry_directory
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

        self.sector_times = [list() for _ in range(56)]
        self.valid_laps = [set() for _ in range(56)]
        self.invalid_laps = [set() for _ in range(56)]

        self.telemetry_data = self.__get_telemetry_data(
            race_start=self.descriptor['race_start'])
        self.packet = None
        self.packet = self.get_data()
        #import pdb; pdb.set_trace()

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

        #Exhaust packets after the race finish.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and \
                    packet.race_state == 2:
                break

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
        last_packet = None
        new_packet = None

        for packet in natsorted(
                glob(self.telemetry_directory+os.sep+'pdata*'),
                reverse=reverse):
            with open(packet, 'rb') as packet_file:
                packet_data = packet_file.read()

            if md5(packet_data).hexdigest() == race_start and \
                    find_start:
                find_start = False
            elif md5(packet_data).hexdigest() != race_start and \
                    find_start:
                continue

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

    def get_data(self, at_time=None):
        """
        Returns the telemetry data. If at_time is provided, the
        time index is used to determine which data packet to return.
        If no index is provided, the first data is provided.
        """
        if self.packet is None:
            packet = next(self.telemetry_data)
            self.packet = packet
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
                len(self._participant_list) >= \
                self.packet.num_participants:
            self.packet = packet
        else:
            self.packet = packet
            self._participant_list = dict()
            self.__rebuild_participants()

        for index, name in self._participant_list.items():
            self.packet.participant_info[index].name = name
            self.packet.participant_info[index].index = index

            for telemetry_packet, _ in self._telemetry_waiting:
                telemetry_packet.participant_info[index].name = name
                telemetry_packet.participant_info[index].index = index

        for participant_index in range(56):
            participant_info = \
                self.packet.participant_info[participant_index]

            if participant_info.race_position == 1:
                self.leader_index = participant_index

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

    def __rebuild_participants(self):
        self._telemetry_waiting = list()
        self._participant_list = dict()
        while len(self._participant_list) < \
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
                self._participant_list[i] = name
        elif packet.packet_type == 2:
            for i, name in enumerate(packet.name, packet.offset):
                self._participant_list[i] = name

    def get_participant_index(self, participant_name):
        """
        Given participant_name, finds the corresponding index.
        """
        matches = [(index, name) for index, name \
            in self._participant_list.items() \
            if name == participant_name]

        index, _ = matches[0]
        return index

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
