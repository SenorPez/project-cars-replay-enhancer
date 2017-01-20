from replayenhancer.RaceData import TelemetryData
import sys

data = TelemetryData(sys.argv[1])

packet = next(data)
while packet.packet_type != 0:
    packet = next(data)

print("Track Length: {}".format(packet.track_length))

while packet.packet_type != 1:
    packet = next(data)

print("Track: {} / {}".format(packet.track_location, packet.track_variation))
