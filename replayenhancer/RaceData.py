"""
Provides classes for the reading and processing of captured Project
CARS telemetry data.
"""
from glob import glob
from hashlib import md5
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


class TelemetryData:
    """
    Reads a directory of telemetry data and returns it as requested.
    """
    def __init__(self, telemetry_directory, *,
                 reverse=False,
                 descriptor_filename='descriptor.json'):
        if not os.path.isdir(telemetry_directory):
            raise NotADirectoryError

        self._telemetry_directory = telemetry_directory
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

    @property
    def packet_count(self):
        """
        Returns the number of packets in the directory.
        """
        return len(glob(self._telemetry_directory + os.sep + 'pdata*'))

    @property
    def telemetry_data(self):
        """
        Returns an iterator containing the telemetry data.
        """
        return self._telemetry_data

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