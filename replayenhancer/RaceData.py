"""
Provides classes for the reading and processing of captured Project
CARS telemetry data.
"""
import json
import os.path
from glob import glob
from hashlib import md5
from itertools import tee

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
from replayenhancer.StartingGridEntry import StartingGridEntry


class RaceData:
    """
    Holds data regarding the race.
    """
    def __init__(self, telemetry_directory, *,
                 descriptor_filename='descriptor.json'):
        self._classification = list()
        self._starting_grid = list()
        self._current_drivers = dict()
        self._retired_drivers = dict()

        self._drivers = list()
        self._last_drivers = list()

        self._elapsed_time = 0.0
        self._add_time = 0.0
        self._last_packet = None
        self._next_packet = None

        self._descriptor_filename = descriptor_filename
        self._telemetry_directory = telemetry_directory
        self._telemetry_data = TelemetryData(
            telemetry_directory,
            descriptor_filename=descriptor_filename)

        self.get_data()

    @property
    def best_lap(self):
        try:
            return min([
                driver.best_lap for driver
                in self._current_drivers.values()
                if driver.best_lap is not None])
        except ValueError:
            return None

    @property
    def best_sector_1(self):
        return self._best_sector(1)

    @property
    def best_sector_2(self):
        return self._best_sector(2)

    @property
    def best_sector_3(self):
        return self._best_sector(3)

    @property
    def classification(self):
        """
        Returns classification data at the current time.
        """
        drivers = self.drivers_by_index
        classification = [
            ClassificationEntry(
                participant_info.race_position,
                drivers[index] if len(drivers) > index
                else None,
                self._next_packet.viewed_participant_index == index)
            for index, participant_info
            in enumerate(self._next_packet.participant_info)
            if self._next_packet.participant_info[index].is_active]\
                [:self._next_packet.num_participants]

        return classification

    @property
    def current_drivers(self):
        """
        Returns a dictionary that maps telemetry names (keys) to
        driver objects (values).
        """
        if len(self._current_drivers):
            return self._current_drivers
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
                    if packet.num_participants != len(self._last_drivers):
                        self._last_drivers = self._drivers
                        self._drivers = self._get_drivers(
                            driver_data,
                            packet.num_participants,
                            progress=progress)

                        self._build_driver_name_lookup(
                            self._drivers,
                            self._last_drivers,
                            packet.num_participants)
                    else:
                        packet = next(driver_data)
                        progress.update()

                except AttributeError:
                    packet = next(driver_data)
                    progress.update()

                except StopIteration:
                    progress.close()
                    return self._current_drivers

    @property
    def current_lap(self):
        leader_lap = max(
            [
                participant.current_lap for participant
                in self._next_packet.participant_info])
        return min(leader_lap, self.total_laps)

    @property
    def drivers_by_index(self):
        return sorted(
            self.current_drivers.values(),
            key=lambda x: x.index)

    @property
    def elapsed_time(self):
        """
        Returns the calculated elapsed time.
        """
        return self._elapsed_time

    @property
    def race_state(self):
        """
        Returns the current race state.
        0: RACESTATE_INVALID
        1: RACESTATE_NOT_STARTED
        2: RACESTATE_RACING,
        3: RACESTATE_FINISHED,
        4: RACESTATE_DISQUALIFIED,
        5: RACESTATE_RETIRED,
        6: RACESTATE_DNF,
        7: RACESTATE_MAX
        """
        return self._next_packet.race_state

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
                    drivers[index].name if len(drivers) > index
                    else None)
                for index, participant_info
                in enumerate(packet.participant_info)
                if packet.participant_info[index].is_active]\
                    [:packet.num_participants]

            progress.close()
            return self._starting_grid

    @property
    def telemetry_data(self):
        """
        Returns the telemetry data iterator.
        """
        return self._telemetry_data

    @property
    def total_laps(self):
        return self._next_packet.laps_in_event

    def get_data(self, at_time=None):
        """
        Retrieves the next telemetry packet.
        """
        while True:
            self._last_packet = self._next_packet
            self._next_packet = None

            try:
                while self._next_packet is None \
                        or self._next_packet.packet_type != 0:
                    self._next_packet = next(self.telemetry_data)
            except StopIteration:
                self._next_packet = self._last_packet
                raise

            self._elapsed_time, \
                self._add_time, \
                self._last_packet = \
                self._calc_elapsed_time(
                    self._next_packet,
                    self._add_time,
                    self._last_packet)

            if (self._next_packet is not None
                    and self._last_packet is None) \
                    or self._next_packet.num_participants \
                    != self._last_packet.num_participants:
                data, restore = tee(self.telemetry_data, 2)
                self._last_drivers = self._drivers
                self._drivers = self._get_drivers(
                    data,
                    self._next_packet.num_participants)

                self._build_driver_name_lookup(
                    self._drivers,
                    self._last_drivers,
                    self._next_packet.num_participants
                )

                del data
                self._telemetry_data = restore

            self._add_sector_times(self._next_packet)

            if at_time is None or self._elapsed_time >= at_time:
                return self._next_packet

    def _add_sector_times(self, packet):
        for index, participant_info in enumerate(
                packet.participant_info[:packet.num_participants]):
            if participant_info.sector == 1:
                sector = 3
            elif participant_info.sector == 2:
                sector = 1
            elif participant_info.sector == 3:
                sector = 2
            else:
                error_message = \
                    "Invalid sector number. Value was: {}".format(
                        participant_info.sector)
                raise ValueError(error_message)

            sector_time = SectorTime(
                participant_info.last_sector_time,
                sector,
                participant_info.invalid_lap)
            for name, driver in self._current_drivers.items():
                if driver.index == index:
                    driver.add_sector_time(sector_time)

    def _best_sector(self, sector):
        try:
            if sector == 1:
                return min([
                    driver.best_sector_1
                    for driver in self._current_drivers.values()
                    ])
            elif sector == 2:
                return min([
                    driver.best_sector_2
                    for driver in self._current_drivers.values()])
            elif sector == 3:
                return min([
                    driver.best_sector_3
                    for driver in self._current_drivers.values()])
            else:
                raise ValueError
        except ValueError:
            return None

    def _build_driver_name_lookup(self, drivers, last_drivers, count):
        if len(last_drivers) < count:
            for driver in drivers:
                self._current_drivers = \
                    self._set_driver(
                        self._current_drivers,
                        driver)
        else:
            for index, driver in enumerate(drivers):
                if last_drivers[index].name \
                        != drivers[index].name:
                    self._current_drivers = \
                        self._set_driver(
                            self._current_drivers,
                            drivers[index],
                            last_drivers[-1])
                else:
                    self._current_drivers = \
                        self._set_driver(
                            self._current_drivers,
                            drivers[index])

    @staticmethod
    def _calc_elapsed_time(next_packet, add_time, last_packet):
        if next_packet.current_time == -1.0:
            elapsed_time = 0.0
            add_time = 0.0
            last_packet = None
        else:
            if last_packet is not None and last_packet.current_time \
                    - next_packet.current_time > 0.5:
                add_time += last_packet.current_time

            elapsed_time = add_time + next_packet.current_time

        return elapsed_time, add_time, last_packet

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
            elif packet.packet_type == 1:
                for index, name in enumerate(packet.name):
                    drivers.append(Driver(index, name))
            elif packet.packet_type == 2:
                for index, name in enumerate(
                        packet.name,
                        packet.offset):
                    drivers.append(Driver(index, name))

            packet = next(telemetry_data)
            if progress is not None:
                progress.update()

        return drivers[:count]

    @staticmethod
    def _set_driver(driver_lookup, driver_1, driver_2=None):
        if driver_2 is not None:
            common = os.path.commonprefix([driver_1.name,
                                           driver_2.name])
            driver_1.real_name = common
            driver_lookup[driver_1.name] = driver_1
            driver_lookup[driver_2.name] = driver_1
        elif driver_1.name not in driver_lookup:
            driver_lookup[driver_1.name] = driver_1
        return driver_lookup


class ClassificationEntry:
    """
    Represents an entry on the classification table.
    """
    def __init__(self, race_position, driver, viewed_driver):
        self._race_position = race_position
        self._driver = driver
        self._viewed_driver = viewed_driver

    @property
    def best_lap(self):
        return self._driver.best_lap

    @property
    def best_sector_1(self):
        return self._driver.best_sector_1

    @property
    def best_sector_2(self):
        return self._driver.best_sector_2

    @property
    def best_sector_3(self):
        return self._driver.best_sector_3

    @property
    def driver(self):
        return self._driver

    @property
    def driver_name(self):
        return self._driver.name

    @property
    def viewed_driver(self):
        return self._viewed_driver

    @property
    def laps_complete(self):
        return self._driver.laps_complete

    @property
    def calc_points_data(self):
        return self.driver_name, self.position, self.best_lap

    @property
    def position(self):
        return self._race_position

    @property
    def race_time(self):
        return self._driver.race_time


class Driver:
    """
    Represents a driver in the race.
    """
    _invalidate_next_sector_count = 0

    def __init__(self, index, name):
        self._index = index
        self._name = name
        self._real_name = name

        self._sector_times = list()

    @property
    def best_lap(self):
        valid_laps = list()
        for invalid, time in zip(
                self._lap_invalid(), self._lap_times()):
            if not invalid:
                valid_laps.append(time)

        try:
            return min(valid_laps)
        except ValueError:
            return None

    @property
    def best_sector_1(self):
        return self._best_sector(1)

    @property
    def best_sector_2(self):
        return self._best_sector(2)

    @property
    def best_sector_3(self):
        return self._best_sector(3)

    @property
    def index(self):
        return self._index

    @property
    def laps_complete(self):
        return len(self._sector_times) // 3

    @property
    def lap_times(self):
        return self._lap_times()

    @property
    def last_lap_invalid(self):
        try:
            return self._lap_invalid()[-1]
        except IndexError:
            return None

    @property
    def last_lap_time(self):
        try:
            return self._lap_times()[-1]
        except IndexError:
            return None

    @property
    def name(self):
        return self._name

    @property
    def race_time(self):
        return sum([
            sector_time.time for sector_time in self._sector_times])

    @property
    def real_name(self):
        return self._real_name

    @real_name.setter
    def real_name(self, value):
        self._real_name = value

    @property
    def sector_times(self):
        return self._sector_times

    def add_sector_time(self, sector_time):
        if sector_time.time == -123.0:
            pass
        elif len(self._sector_times) == 0:
            self._sector_times.append(sector_time)
        elif self._sector_times[-1].time != sector_time.time \
                and self._sector_times[-1].sector != sector_time.sector:
            if self._invalidate_next_sector_count > 0:
                self._sector_times.append(SectorTime(
                    sector_time.time,
                    sector_time.sector,
                    True))
                self._invalidate_next_sector_count -= 1
            else:
                self._sector_times.append(SectorTime(
                    sector_time.time,
                    sector_time.sector,
                    False))

        if sector_time.invalid:
            self._invalidate_lap(sector_time)

    def _best_sector(self, sector):
        try:
            return min([
                sector_time.time
                for sector_time in self._sector_times
                if not sector_time.invalid
                and sector_time.sector == sector])
        except ValueError:
            return None

    def _invalidate_lap(self, sector_time):
        if sector_time.sector == 3:
            self._invalidate_next_sector_count = 3
        elif sector_time.sector == 1:
            self._invalidate_next_sector_count = 2
            self._sector_times[-1].invalid = True
        elif sector_time.sector == 2:
            self._invalidate_next_sector_count = 1
            for sector in self._sector_times[-2:]:
                sector.invalid = True
        else:
            raise ValueError("Invalid Sector Number")

    def _lap_times(self):
        """
        Check to see if the first sector in the list is sector 1.
        Trim if not.
        """
        sector_times = self._sector_times
        try:
            while sector_times[0].sector != 1:
                sector_times = sector_times[1:]
        except IndexError:
            pass

        times = [sector.time for sector in sector_times]
        lap_times = list()
        for lap in zip(*[iter(times)]*3):
            try:
                lap_times.append(sum(lap))
            except TypeError:
                lap_times.append(None)
        return lap_times

    def _lap_invalid(self):
        """
        Check to see if the first sector in the list is sector 1.
        Trim if not.
        """
        sector_times = self._sector_times
        try:
            while sector_times[0].sector != 1:
                sector_times = sector_times[1:]
        except IndexError:
            pass

        invalids = [sector.invalid for sector in sector_times]
        lap_validity = list()
        for lap in zip(*[iter(invalids)]*3):
            try:
                lap_validity.append(any(lap))
            except TypeError:
                lap_validity.append(None)
        return lap_validity


class SectorTime:
    """
    Represents a sector time.
    """
    def __init__(self, time, sector, invalid):
        self._time = time
        self._sector = sector
        self._invalid = False if invalid == 0 else True

    @property
    def sector(self):
        """
        Sector number: 1, 2, or 3
        """
        return self._sector

    @property
    def time(self):
        """
        Returns sector time.
        """
        return self._time

    @property
    def invalid(self):
        """
        Returns if sector is valid.
        """
        return self._invalid

    @invalid.setter
    def invalid(self, value):
        self._invalid = value


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

        telemetry_data = self._get_telemetry_data(telemetry_directory)
        progress = tqdm(
            desc='Detecting Race End',
            total=self.packet_count,
            unit='packets')

        packet = None
        old_packet = None
        while True:
            old_packet = packet
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and packet.race_state == 3:
                break

        # Exhaust packets until the race end.
        # TODO: Support for other ways to finish a race?
        while True:
            old_packet = packet
            packet = next(telemetry_data)
            progress.update()
            if packet.packet_type == 0 and packet.race_state != 3:
                break

        progress.close()

        descriptor['race_end'] = old_packet.data_hash

        telemetry_data = self._get_telemetry_data(
            telemetry_directory,
            reverse=True)
        progress = tqdm(
            desc='Analyzing Telemetry Data',
            total=self.packet_count,
            unit='packets')

        # Exhaust packets until the race end.
        while True:
            packet = next(telemetry_data)
            progress.update()
            if packet.data_hash == descriptor['race_end']:
                break

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

        old_packet = packet
        # Exhaust packets after the race start, except one.
        try:
            while True:
                if packet.packet_type == 0:
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

            if descriptor is not None and md5(packet_data).hexdigest() == descriptor['race_end']:
                raise StopIteration

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
