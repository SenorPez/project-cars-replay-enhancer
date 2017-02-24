from replayenhancer.TelemetryDataPacket import TelemetryDataPacket
from glob import glob
from natsort import natsorted

with open('outputs/times.txt', 'w+') as f:
    for packet in natsorted(
                    glob('assets/race1-descriptor/pdata*')):
        with open(packet, 'rb') as packet_file:
            packet_data = packet_file.read()

        if len(packet_data) == 1367:
            RETDP = TelemetryDataPacket(packet_data)
            time = str(RETDP.current_time) + " | " + str(RETDP.data_hash) + "\n"
            f.write(str(time))
