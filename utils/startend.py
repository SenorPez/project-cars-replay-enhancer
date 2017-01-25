import os.path
import sys

import moviepy.editor as mpy
from numpy import diff, nonzero
from tqdm import tqdm

from replayenhancer.RaceData import RaceData

source_video = mpy.VideoFileClip(os.path.abspath(sys.argv[1]))
threshold = 1
gap_time = 1

blackframes = [
    t for (t, f)
    in source_video.iter_frames(with_times=True, progress_bar=1)
    if f.mean() < threshold]

print([blackframes[x] for x in nonzero(diff(blackframes)>gap_time)[0]])
print([blackframes[::-1][x] for x in nonzero(diff(blackframes[::-1])<-gap_time)[0]])

race_data = RaceData(os.path.abspath(sys.argv[2]))

with tqdm(desc="Processing telemetry") as progress:
    while True:
        try:
            _ = race_data.get_data()
            progress.update()
        except StopIteration:
            break

print(sum(race_data.drivers['Kobernulf Monnur'].lap_times))
