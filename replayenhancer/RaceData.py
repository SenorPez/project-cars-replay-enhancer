"""
Provides classes for the reading and processing of captured Project
CARS telemetry data.
"""
import json
import os.path
from glob import glob
from hashlib import md5
from itertools import tee
from math import ceil

from natsort import natsorted
from tqdm import tqdm

from replayenhancer.AdditionalParticipantPacket \
    import AdditionalParticipantPacket
from replayenhancer.ParticipantPacket import ParticipantPacket
from replayenhancer.TelemetryDataPacket import TelemetryDataPacket
from replayenhancer.Track import Track


class RaceData:
    """
    Holds data regarding the race.
    """
    def __init__(self, telemetry_directory, *,
                 descriptor_filename='descriptor.json'):
        self._starting_grid = list()
        self.drivers = dict()
        self._dropped_drivers = dict()

        self._stopped_drivers = set()

        self.elapsed_time = 0.0
        self._last_packet = None
        self._next_packet = None

        self.track = None

        self._descriptor_filename = descriptor_filename
        self._telemetry_directory = telemetry_directory
        self.telemetry_data = TelemetryData(
            telemetry_directory,
            descriptor_filename=descriptor_filename)

        self.get_data()

        if self.laps_in_event == 0:
            time_data = TelemetryData(
                telemetry_directory,
                descriptor_filename=descriptor_filename)
            packet = next(time_data)
            while (packet.packet_type == 0 and packet.race_state == 1) \
                    or packet.packet_type != 0:
                packet = next(time_data)

            self.total_time = ceil(packet.event_time_remaining)
        else:
            self.total_time = None

    @property
    def all_driver_classification(self):
        classification = self.classification
        for driver in self._dropped_drivers.values():
            classification.append(ClassificationEntry(None, driver, False))

        position = 0
        for entry in sorted(
                classification,
                key=lambda x: (-x.driver.laps_complete, x.driver.race_time)):
            position += 1
            entry.position = position

        return classification

    @property
    def best_lap(self):
        try:
            return min([
                driver.best_lap for driver
                in self.drivers.values()
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
        classification = list()
        drivers_by_index = sorted(
            [driver for driver in self.drivers.values()],
            key=lambda x: x.index)
        for index in range(self._next_packet.num_participants):
            classification.append(ClassificationEntry(
                self._next_packet.participant_info[index].race_position,
                drivers_by_index[index],
                self._next_packet.viewed_participant_index == index))

        return classification

    @property
    def current_lap(self):
        leader_lap = max(
            [
                participant.current_lap for participant
                in self._next_packet.participant_info])
        return leader_lap if self.laps_in_event == 0 \
            else min(leader_lap, self.laps_in_event)

    @property
    def current_time(self):
        return self._next_packet.current_time

    @property
    def event_time_remaining(self):
        return self._next_packet.event_time_remaining

    @property
    def laps_in_event(self):
        return self._next_packet.laps_in_event

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
            packet = None

            while packet is None or packet.packet_type != 0:
                packet = next(grid_data)

            drivers = sorted(
                self._get_drivers(
                    grid_data,
                    packet.num_participants).values(),
                key=lambda x: x.index)

            self._starting_grid = [
                StartingGridEntry(
                    participant_info.race_position,
                    index,
                    drivers[index].name)
                if index < len(drivers) else None
                for index, participant_info
                in enumerate(packet.participant_info)]

            self._starting_grid = [
                entry for entry in self._starting_grid
                if entry is not None]

            return self._starting_grid

    def driver_world_position(self, index):
        return self._next_packet.participant_info[index].world_position

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

            if (self._next_packet is not None
                    and self._last_packet is None) \
                    or (
                        self._next_packet.num_participants
                        != self._last_packet.num_participants
                        and self._next_packet.num_participants != -1):
                data, restore = tee(self.telemetry_data, 2)

                current_drivers = self._get_drivers(
                    data,
                    self._next_packet.num_participants)
                del data
                self.telemetry_data = restore

                # Add any new drivers.
                for key in current_drivers.keys() - self.drivers.keys():
                    self.drivers[key] = current_drivers[key]

                # Delete any dropped drivers.
                for key in self.drivers.keys() - current_drivers.keys():
                    self._dropped_drivers[key] = self.drivers[key]
                    del self.drivers[key]

                # Reset indices for drivers that remain.
                for key in current_drivers.keys():
                    self.drivers[key].index = current_drivers[key].index

            self.track = Track(self._next_packet.track_length)
            self._add_sector_times(self._next_packet)
            self._calc_elapsed_time()

            if at_time is None or self.elapsed_time >= at_time:
                return self._next_packet

    def _add_sector_times(self, packet):
        for index, participant_info in enumerate(
                packet.participant_info[:packet.num_participants]):
            driver_name = None
            for driver in self.drivers.values():
                if driver.index == index:
                    driver_name = driver.name

            if participant_info.sector == 1:
                sector = 3
            elif participant_info.sector == 2:
                if driver_name in self._stopped_drivers:
                    self._stopped_drivers.remove(driver_name)
                sector = 1
            elif participant_info.sector == 3:
                sector = 2
            else:
                """
                TODO: Investigate instance of a driver existing but having an
                invalid sector number (0). I suspect it's due to a network
                timeout.
                """
                return

            if self.track.at_pit_entry(participant_info.world_position) \
                    and driver_name not in self._stopped_drivers \
                    and self.race_state == 2:
                self._stopped_drivers.add(driver_name)

            if self.track.at_pit_exit(participant_info.world_position) \
                    and driver_name in self._stopped_drivers:
                self.drivers[driver_name].stops += 1
                self._stopped_drivers.remove(driver_name)

            sector_time = SectorTime(
                participant_info.last_sector_time,
                sector,
                participant_info.invalid_lap)

            self.drivers[driver_name].add_sector_time(sector_time)

    def _best_sector(self, sector):
        try:
            if sector == 1:
                return min(
                    [driver.best_sector_1 for driver in self.drivers.values()])
            elif sector == 2:
                return min(
                    [driver.best_sector_2 for driver in self.drivers.values()])
            elif sector == 3:
                return min(
                    [driver.best_sector_3 for driver in self.drivers.values()])
            else:
                raise ValueError
        except ValueError:
            return None

    def _calc_elapsed_time(self):
        if self._next_packet.current_time == -1.0:
            self.elapsed_time = 0.0
            self._last_packet = None
        else:
            driver = next(
                driver for driver in self.drivers.values()
                if driver.index == self._next_packet.viewed_participant_index)
            self.elapsed_time = \
                sum(driver.lap_times) + self._next_packet.current_time

    @staticmethod
    def _get_drivers(telemetry_data, count):
        drivers = list()
        packet = next(telemetry_data)

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

        return {driver.name: driver for driver in sorted(
            drivers,
            key=lambda x: x.index)[:count]}


class ClassificationEntry:
    """
    Represents an entry on the classification table.
    """
    def __init__(self, position, driver, viewed_driver):
        self.position = position
        self.driver = driver
        self.viewed_driver = viewed_driver

    @property
    def best_lap(self):
        return self.driver.best_lap

    @property
    def best_sector_1(self):
        return self.driver.best_sector_1

    @property
    def best_sector_2(self):
        return self.driver.best_sector_2

    @property
    def best_sector_3(self):
        return self.driver.best_sector_3

    @property
    def driver_name(self):
        return self.driver.name

    @property
    def laps_complete(self):
        return self.driver.laps_complete

    @property
    def calc_points_data(self):
        return self.driver_name, self.position, self.best_lap

    @property
    def race_time(self):
        return self.driver.race_time

    @property
    def stops(self):
        return self.driver.stops


class Driver:
    """
    Represents a driver in the race.
    """
    _invalidate_next_sector_count = 0

    def __init__(self, index, name):
        self.index = index
        self.name = name

        self.sector_times = list()
        self.stops = 0

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
    def laps_complete(self):
        return len(self.sector_times) // 3

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
    def race_time(self):
        return sum([sector_time.time for sector_time in self.sector_times])

    def add_sector_time(self, sector_time):
        if sector_time.time == -123.0:
            pass
        elif len(self.sector_times) == 0:
            self.sector_times.append(sector_time)
        elif self.sector_times[-1].time != sector_time.time \
                or self.sector_times[-1].invalid != sector_time.invalid \
                or self.sector_times[-1].sector != sector_time.sector:
            if self.sector_times[-1].invalid != sector_time.invalid \
                    and self.sector_times[-1].time == sector_time.time \
                    and self.sector_times[-1].sector == sector_time.sector:
                self.sector_times[-1] = sector_time
            else:
                if self._invalidate_next_sector_count > 0:
                    self.sector_times.append(SectorTime(
                        sector_time.time,
                        sector_time.sector,
                        True))
                    self._invalidate_next_sector_count -= 1
                else:
                    self.sector_times.append(SectorTime(
                        sector_time.time,
                        sector_time.sector,
                        False))

            if sector_time.invalid:
                self._invalidate_lap(sector_time)

    def _best_sector(self, sector):
        try:
            return min([
                sector_time.time
                for sector_time in self.sector_times
                if not sector_time.invalid
                and sector_time.sector == sector])
        except ValueError:
            return None

    def _invalidate_lap(self, sector_time):
        if sector_time.sector == 3:
            self._invalidate_next_sector_count = 3
        elif sector_time.sector == 1:
            self._invalidate_next_sector_count = 2
            for sector in self.sector_times[-1:]:
                sector.invalid = True
        elif sector_time.sector == 2:
            self._invalidate_next_sector_count = 1
            for sector in self.sector_times[-2:]:
                sector.invalid = True
        else:
            raise ValueError("Invalid Sector Number")

    def _lap_times(self):
        """
        Check to see if the first sector in the list is sector 1.
        Trim if not.
        """
        sector_times = self.sector_times
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
        sector_times = self.sector_times
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
        self.time = time
        self.sector = sector
        self.invalid = False if invalid == 0 else True


class StartingGridEntry:
    """
    Represents an entry on the starting grid.
    """
    def __init__(self, position, driver_index, driver_name):
        self.position = position
        self.driver_index = driver_index
        self.driver_name = driver_name


class TelemetryData:
    """
    Reads a directory of telemetry data and returns it as requested.
    """
    def __init__(self, telemetry_directory, *,
                 reverse=False,
                 descriptor_filename='descriptor.json'):
        if not os.path.isdir(telemetry_directory):
            raise NotADirectoryError

        self.packet_count = len(
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

    def _build_descriptor(self, telemetry_directory, descriptor_filename):
        descriptor = {
            'race_end': None,
            'race_finish': None,
            'race_start': None}

        telemetry_data = self._get_telemetry_data(telemetry_directory)
        progress = tqdm(
            desc='Detecting Race End',
            total=self.packet_count,
            unit='packets')

        old_packet = None
        try:
            while True:
                while True:
                    packet = next(telemetry_data)
                    progress.update()
                    if packet.packet_type == 0 and packet.race_state == 3:
                        break

                # Exhaust packets until the race end.
                # TODO: Support for other ways to finish a race?
                while True:
                    try:
                        old_packet = packet
                        packet = next(telemetry_data)
                        progress.update()
                        if packet.packet_type == 0 and packet.race_state != 3:
                            break
                    except StopIteration:
                        old_packet = packet
                        break

        except StopIteration:
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

            if descriptor is not None \
                    and md5(packet_data).hexdigest() == descriptor['race_end']:
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
                """
                TODO: Make sure this is actually correct. I think it's due
                to network lag during race loading.
                """
                positions = [
                    participant.race_position for participant
                    in packet.participant_info][:packet.num_participants]
                sectors = [
                    participant.sector for participant
                    in packet.participant_info][:packet.num_participants]

                if not all(positions) or not all(sectors):
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
