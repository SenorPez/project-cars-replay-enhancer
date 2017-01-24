import json
import sys

import moviepy.editor as mpy
from numpy import cumsum

from replayenhancer.RaceData import RaceData

config = json.load(open(sys.argv[1]))
data = RaceData(config['source_telemetry'])
clip = mpy.VideoFileClip(config['source_video']).subclip(
    config['video_skipstart'], config['video_skipend'])

try:
    while True:
        data.get_data()
except StopIteration:
    pass

times = [time + config['sync_racestart'] for time in list(cumsum(data.drivers['Kobernulf Monnur'].lap_times))]

for lap, time in enumerate(times, 1):
    clip.save_frame("outputs/lap{}.jpg".format(lap), time)

for ix in range(10, -11, -1):
    offset = config['sync_racestart'] + ix / 100
    times = [time + offset for time in list(cumsum(data.drivers['Kobernulf Monnur'].lap_times))]
    clip.save_frame("outputs/sync{}.jpg".format(int(offset * 100)), times[0])
