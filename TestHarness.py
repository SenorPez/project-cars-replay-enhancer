from AdditionalParticipantPacket import AdditionalParticipantPacket
from ParticipantPacket import ParticipantPacket
from RaceData import RaceData
from TelemetryDataPacket import TelemetryDataPacket

from tqdm import tqdm
import os
from natsort import natsorted
from glob import glob

class TestHarness():
    def __init__(self):
        self.race_data = RaceData()
        self.__process_telemetry_directory('assets/race1/')

    def __process_telemetry_directory(self, telemetry_directory):
        with tqdm(desc="Processing telemetry",
                total=len([x for x in os.listdir(
                    telemetry_directory)])) as progress_bar:
            for packet in natsorted(glob(telemetry_directory+'/pdata*')):
                with open(packet, 'rb') as packet_file:
                    packet_data = packet_file.read()

                self.__process_telemetry_packet(packet_data)
                progress_bar.update()

    def __process_telemetry_packet(self, packet):
        if len(packet) == 1347:
            self.__dispatch(ParticipantPacket(packet))
        elif len(packet) == 1028:
            self.__dispatch(AdditionalParticipantPacket(
                packet))
        elif len(packet) == 1367:
            self.__dispatch(TelemetryDataPacket(packet))

    def __dispatch(self, packet):
        self.race_data.add(packet)

output = TestHarness()
print(output.race_data)
