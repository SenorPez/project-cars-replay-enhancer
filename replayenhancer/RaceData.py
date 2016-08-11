"""
Provides classes for the reading and processing of captured Project
CARS telemetry data.
"""
from glob import glob
from hashlib import md5
from itertools import tee
import json
import os.path

from natsort import natsorted
from tqdm import tqdm

from replayenhancer.AdditionalParticipantPacket \
    import AdditionalParticipantPacket \
    as AdditionalParticipantPacket
from replayenhancer.REParticipantPacket \
    import REParticipantPacket \
    as ParticipantPacket
from replayenhancer.RETelemetryDataPacket \
    import RETelemetryDataPacket \
    as TelemetryDataPacket


class RaceData:
    """
    Holds data regarding the race.
    """
    def __init__(self, telemetry_directory, *,
                 descriptor_filename='descriptor.json'):
        self._driver_name_lookup = dict()
        self._driver_index_lookup = list()

        self._classification = list()
        self._starting_grid = list()
        self._current_drivers = list()

        self._elapsed_time = 0.0
        self._add_time = 0.0
        self._last_packet = None
        self._next_packet = None

        self._descriptor_filename = descriptor_filename
        self._telemetry_directory = telemetry_directory
        self._telemetry_data = TelemetryData(
            telemetry_directory,
            descriptor_filename=descriptor_filename)

    @property
    def classification(self):
        """
        Returns classification data at the current time.
        """
        return self._classification

    @property
    def current_drivers(self):
        """
        Returns best guess names for drivers currently in the race.
        """
        return self._current_drivers

    @current_drivers.setter
    def current_drivers(self, value):
        self._current_drivers = value

    @property
    def driver_name_lookup(self):
        """
        Returns a dictionary that maps telemetry names (keys) to best
        guess names (values).
        """
        last_drivers = list()

        if len(self._driver_name_lookup):
            return self._driver_name_lookup
        else:
            driver_data = TelemetryData(
                self._telemetry_directory,
                descriptor_filename=self._descriptor_filename)
            progress = tqdm(
                desc='Getting Drivers',
                total=driver_data.packet_count,
                unit='packets')
            packet = None

            while True:
                try:
                    if packet.num_participants != len(last_drivers):
                        drivers = self._get_drivers(
                            driver_data,
                            packet.num_participants,
                            progress=progress)

                        self.driver_name_lookup = (
                            drivers,
                            last_drivers,
                            packet.num_participants)

                        last_drivers = drivers
                    else:
                        packet = next(driver_data)
                        progress.update()

                except AttributeError:
                    packet = next(driver_data)
                    progress.update()

                except StopIteration:
                    progress.close()
                    return self._driver_name_lookup

    @driver_name_lookup.setter
    def driver_name_lookup(self, value):
        drivers, last_drivers, count = value
        if len(last_drivers) < count:
            for driver in drivers:
                self._driver_name_lookup = \
                    self._set_driver(
                        self._driver_name_lookup,
                        driver)
                self._driver_index_lookup = drivers
        else:
            for index, driver in enumerate(drivers):
                if last_drivers[index] \
                        != drivers[index]:
                    self._driver_name_lookup = \
                        self._set_driver(
                            self._driver_name_lookup,
                            drivers[index],
                            last_drivers[-1])
                else:
                    self._driver_name_lookup = \
                        self._set_driver(
                            self._driver_name_lookup,
                            drivers[index])

    @property
    def drivers(self):
        """
        Returns best guess names for all drivers in race.
        """
        return set(self.driver_name_lookup.values())

    @property
    def elapsed_time(self):
        """
        Returns the calculated elapsed time.
        """
        return self._elapsed_time

    @property
    def starting_grid(self):
        """
        Returns the starting grid for the race.
        """
        if len(self._starting_grid):
            return self._starting_grid
        else:
            grid_data = TelemetryData(
                self._telemetry_directory,
                descriptor_filename=self._descriptor_filename)
            progress = tqdm(
                desc='Calculating Starting Grid',
                total=grid_data.packet_count,
                unit='packets')
            packet = None

            while packet is None or packet.packet_type != 0:
                packet = next(grid_data)

            drivers = self._get_drivers(
                grid_data,
                packet.num_participants,
                progress=progress)

            self._starting_grid = [
                StartingGridEntry(
                    participant_info.race_position,
                    index,
                    drivers[index] if len(drivers) > index else None)
                for index, participant_info
                in enumerate(packet.participant_info)
                if packet.participant_info[index].is_active]\
                    [:packet.num_participants]

            progress.close()
            return self._starting_grid

    @property
    def telemetry_data(self):
        """
        Returns the telemetry data. Can be used as an iterator.
        """
        return self._telemetry_data

    def get_data(self):
        """
        Retrieves the next telemetry packet.
        """
        self._last_packet = self._next_packet
        self._next_packet = None
        while self._next_packet is None \
                or self._next_packet.packet_type != 0:
            self._next_packet = next(self.telemetry_data)

        if self._next_packet.current_time == -1.0:
            self._elapsed_time = 0.0
            self._add_time = 0.0
            self._last_packet = None
        else:
            if self._last_packet is not None \
                    and self._last_packet.current_time > \
                    self._next_packet.current_time:
                self._add_time += self._last_packet.current_time

            self._elapsed_time = \
                self._add_time + self._next_packet.current_time

        if (self._next_packet is not None
                and self._last_packet is None) \
                or self._next_packet.num_participants != \
                    self._last_packet.num_participants:
            data, _ = tee(self.telemetry_data, 2)
            self._current_drivers = self._get_drivers(
                data,
                self._next_packet.num_participants)
            del data

        return self._next_packet

    @staticmethod
    def _get_drivers(telemetry_data, count, *, progress=None):
        drivers = list()
        packet = next(telemetry_data)
        if progress is not None:
            progress.update()

        while len(drivers) < count:
            if packet.packet_type == 0 \
                    and packet.num_participants != count:
                raise ValueError(
                    "Participants not populated before break.")
            elif packet.packet_type == 1 or packet.packet_type == 2:
                drivers.extend(packet.name)
            packet = next(telemetry_data)
            if progress is not None:
                progress.update()

        return drivers[:count]

    @staticmethod
    def _set_driver(driver_lookup, driver_name_1, driver_name_2=None):
        if driver_name_2 is not None:
            common = os.path.commonprefix([driver_name_1,
                                           driver_name_2])
            driver_lookup[driver_name_1] = common
            driver_lookup[driver_name_2] = common
        elif driver_name_1 not in driver_lookup:
            driver_lookup[driver_name_1] = driver_name_1
        return driver_lookup


class ClassificationEntry:
    """
    Represents an entry on the classification table.
    """
    def __init__(self, driver_index, driver_name, sector_times):
        self._driver_index = driver_index
        self._driver_name = driver_name
        self._sector_times = sector_times

    @property
    def best_lap(self):
        """
        Best Lap by driver.
        """
        return min(self.lap_times)

    @property
    def best_sector_1(self):
        """
        Best Sector 1 time by driver.
        """
        return min([data.time for data in self.sector_times
                    if data.sector == 1])

    @property
    def best_sector_2(self):
        """
        Best Sector 2 time by driver.
        """
        return min([data.time for data in self.sector_times
                    if data.sector == 2])

    @property
    def best_sector_3(self):
        """
        Best Sector 3 time by driver.
        """
        return min([data.time for data in self.sector_times
                    if data.sector == 3])

    @property
    def laps_completed(self):
        """
        Number of laps completed by driver.
        """
        return len(self.lap_times)

    @property
    def lap_times(self):
        """
        List of lap times for driver.
        """
        return [sum(times) for times in zip(
            *[iter([data.time for data in self.sector_times])])]

    @property
    def race_time(self):
        """
        Total race time for driver.
        """
        return sum([data.time for data in self.sector_times])

    @property
    def sector_times(self):
        """
        Sector times for driver.
        """
        return self._sector_times


class SectorTime:
    """
    Represents a sector time.
    """
    def __init__(self, time, sector, valid):
        self._time = time
        self._sector = sector
        self._valid = valid

    @property
    def sector(self):
        """
        Sector number: 1, 2, or 3
        """
        return self._sector

    @sector.setter
    def sector(self, value):
        if value < 1 or value > 3:
            raise ValueError("Invalid sector number.")
        else:
            self._sector = value

    @property
    def time(self):
        """
        Returns sector time.
        """
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def valid(self):
        """
        Returns if sector is valid.
        """
        return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value


class StartingGridEntry:
    """
    Represents an entry on the starting grid.
    """
    def __init__(self, position, driver_index, driver_name):
        self._position = position
        self._driver_index = driver_index
        self._driver_name = driver_name

    @property
    def driver_index(self):
        """
        Index position of driver.
        """
        return self._driver_index

    @property
    def driver_name(self):
        """
        Telemetry-read name of driver.
        """
        return self._driver_name

    @property
    def position(self):
        """
        Starting position of driver.
        """
        return self._position


class TelemetryData:
    """
    Reads a directory of telemetry data and returns it as requested.
    """
    def __init__(self, telemetry_directory, *,
                 reverse=False,
                 descriptor_filename='descriptor.json'):
        if not os.path.isdir(telemetry_directory):
            raise NotADirectoryError

        self._packet_count = len(
            glob(telemetry_directory + os.sep + 'pdata*'))
        descriptor = None
        try:
            with open(os.path.join(
                os.path.realpath(telemetry_directory),
                os.path.relpath(descriptor_filename))) \
                    as descriptor_file:
                descriptor = json.load(descriptor_file)
        except (FileNotFoundError, ValueError):
            descriptor = self._build_descriptor(
                telemetry_directory,
                descriptor_filename)
        finally:
            self._telemetry_data = self._get_telemetry_data(
                telemetry_directory,
                descriptor,
                reverse=reverse)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._telemetry_data)

    @property
    def packet_count(self):
        """
        Returns the number of packets in the directory.
        """
        return self._packet_count

    def _build_descriptor(self, telemetry_directory,
                          descriptor_filename):
        descriptor = {
            'race_end': None,
            'race_finish': None,
            'race_start': None}
        telemetry_data = self._get_telemetry_data(
            telemetry_directory,
            reverse=True)
        progress = tqdm(
            desc='Analyzing Telemetry Data',
            total=self.packet_count,
            unit='packets')

        # Exhaust packets after the race end.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and packet.race_state == 3:
                break

        descriptor['race_end'] = packet.data_hash

        # Exhaust packets after the race finish.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and packet.race_state == 2:
                break

        descriptor['race_finish'] = packet.data_hash

        # Exhaust packets after the green flag.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and (
                    packet.race_state == 0 or
                    packet.race_state == 1):
                break

        # Exhaust packets after the race start, except one.
        try:
            while True:
                old_packet = packet
                packet = next(telemetry_data)
                progress.update()
                if packet.packet_type == 0 and (
                        packet.session_state != 5 or
                        packet.game_state != 2):
                    break
        # None found (no restarts?) so use the first packet.
        # It is already on `old_packet`.
        except StopIteration:
            pass

        progress.close()
        descriptor['race_start'] = old_packet.data_hash

        with open(os.path.join(
            os.path.realpath(telemetry_directory),
            os.path.relpath(descriptor_filename)), 'w') \
                as descriptor_file:
            json.dump(descriptor, descriptor_file)

        return descriptor

    @staticmethod
    def _get_telemetry_data(telemetry_directory, descriptor=None, *,
                            reverse=False):
        find_start = False if descriptor is None else True
        find_populate = False

        for packet in natsorted(
                glob(telemetry_directory+os.sep+'pdata*'),
                reverse=reverse):
            with open(packet, 'rb') as packet_file:
                packet_data = packet_file.read()

            if find_start and \
                    md5(packet_data).hexdigest() == \
                    descriptor['race_start']:
                find_start = False
                find_populate = True
            elif find_start and \
                    md5(packet_data).hexdigest() != \
                    descriptor['race_start']:
                continue
            elif find_populate and \
                    len(packet_data) == 1367:
                packet = TelemetryDataPacket(packet_data)
                if not any([
                        participant.race_position
                        for participant
                        in packet.participant_info]
                           [:packet.num_participants]):
                    continue
                else:
                    find_populate = False
                    yield packet
            elif len(packet_data) == 1367:
                yield TelemetryDataPacket(packet_data)
            elif len(packet_data) == 1347:
                yield ParticipantPacket(packet_data)
            elif len(packet_data) == 1028:
                yield AdditionalParticipantPacket(packet_data)
