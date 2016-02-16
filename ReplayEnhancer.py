from collections import deque
from itertools import groupby
from os.path import commonprefix
import csv
import argparse
from glob import glob
from hashlib import sha256
from natsort import natsorted
from struct import unpack
import json
import os.path
import sys

import moviepy.editor as mpy
from moviepy.editor import vfx
from moviepy.video.io.bindings import PIL_to_npimage
from numpy import diff, nonzero, where, cumsum
from PIL import Image, ImageFont
from tqdm import tqdm

from Champion import Champion
from Configuration import Configuration
from Results import Results
from SeriesStandings import SeriesStandings
from Standings import Standings
from Timer import Timer
from Title import Title
from Track import Track
from UpdatedVideoClip import UpdatedVideoClip

class ReplayEnhancer():
    def __init__(self, configuration=None):
        with open(os.path.realpath(configuration), 'r') as f:
            try:
                json_data = json.load(f)
            except ValueError as e:
                raise e

        self.font = ImageFont.truetype(json_data['font'], json_data['font_size'])
        self.heading_font = ImageFont.truetype(json_data['heading_font'], json_data['heading_font_size'])
        self.heading_color = tuple(json_data['heading_color'])

        self.backdrop = json_data['backdrop']
        self.logo = json_data['logo']
        self.logo_height = json_data['logo_height']
        self.logo_width = json_data['logo_width']
        self.series_logo = json_data['series_logo']

        self.show_champion = json_data['show_champion']

        self.heading_text = json_data['heading_text']
        self.subheading_text = json_data['subheading_text']

        self.margin = json_data['margin']
        self.column_margin = json_data['column_margin']

        self.source_video = json_data['source_video'] if len(json_data['source_video']) else None
        self.source_telemetry = json_data['source_telemetry']
        self.telemetry_file = 'tele.csv'
        self.output_video = json_data['output_video']

        self.name_display = {k:v['display'] for k, v in json_data['participant_config'].items()}
        self.short_name_display = {k:v['short_display'] for k, v in json_data['participant_config'].items()}
        self.car_data = {k:v['car'] for k, v in json_data['participant_config'].items()}
        self.team_data = {k:v['team'] for k, v in json_data['participant_config'].items()}
        self.points = {k:v['points'] for k, v in json_data['participant_config'].items()}

        #self.car_data = {v['participant']:v['car'] for v in json_data['participant_config']}
        #self.team_data = {v['participant']:v['team'] if len(v['team']) else None for v in json_data['participant_config']}
        #self.points = {v['participant']:v['points'] for v in json_data['participant_config']}

        self.point_structure = json_data['point_structure']

        self.video_threshold = json_data['video_threshold']
        self.video_gaptime = json_data['video_gaptime']
        self.video_skipstart = json_data['video_skipstart']
        self.video_skipend = json_data['video_skipend']
        self.video_cache = json_data['video_cache']

        self.sync_racestart = json_data['sync_racestart']

        self.participant_data = list()
        self.participant_configurations = list()
        self.participant_lookup = list()
        self.telemetry_data = list()
        self.config_version = 4

        '''
        self.sector_bests = [-1, -1, -1]
        self.personal_bests = [[-1, -1, -1] for x in range(64)]
        self.best_lap = -1
        self.personal_best_laps = [-1 for x in range(64)]
        self.elapsed_times = [-1 for x in range(64)]
        '''

        self.race_start = -1
        self.race_finish = -1
        self.race_p1_finish = -1
        self.race_end = -1

        self.get_telemetry()

        self.track = Track(self.telemetry_data[0][0][0][-7])

    def get_telemetry(self):
        try:
            f = open(self.source_telemetry+self.telemetry_file, 'r')
        except FileNotFoundError:
            self.process_telemetry()
            f = open(self.source_telemetry+self.telemetry_file, 'r')
        finally:
            index = 0
            with open(self.source_telemetry+self.telemetry_file) as csv_file:
                for index, _ in enumerate(csv_file):
                    pass
            number_lines = index+1
            csvdata = csv.reader(f)

        try:
            i = 0;
            with tqdm(desc="Loading telemetry", total=number_lines) \
                        as progress_bar:
                for row in csvdata:
                    self.telemetry_data.append(row+[i])
                    i += 1
                    progress_bar.update()

                    '''
                    if int(row[1]) & 3 == 0:
                        self.telemetry_data.append(row)
                    elif int(row[1]) & 3 == 1:
                        for p in enumerate(row[6:-1]):
                            if len(p[1]):
                                self.participant_data.append(p)
                    elif int(row[1]) & 3 == 2:
                        for p in enumerate(row[3:-1], int(row[2])):
                            if len(p[1]):
                                self.participant_data.append(p)
                    else:
                        raise ValueError("ValueError: Unrecognized packet type ("+str(int(row[1]) & 3)+")")

                self.participant_data = [(i, n, t, c) for (i, n), t, c in zip(list(sorted({x for x in self.participant_data})), self.team_data, self.car_data)]
                '''

            #Extract, process, and de-garbage the participant data.
            #Also add cumulative time index to end of data structure.

            last_time = 0
            add_time = 0
            time_adjust = 0
            participants = 0
            new_data = list()

            with tqdm(desc="Processing telemetry", total=number_lines) \
                        as progress_bar:
                for i, data in enumerate(self.telemetry_data):
                    if len(data) == 688 and int(data[4]) != -1:
                        participants = int(data[4])

                        if float(data[13]) == -1:
                            self.telemetry_data[i] = data+[-1]
                        else:
                            if last_time == 0:
                                time_adjust = float(data[13])
                            elif float(data[13]) < last_time:
                                add_time = last_time + add_time
                            self.telemetry_data[i] = data+[float(data[13])+add_time-time_adjust]
                            last_time = float(data[13])
                    elif len(data) == 688 and int(data[4]) == -1:
                        pass
                    elif len(data) == 24:
                        for p in enumerate(data[6:6+min(16, participants)]):
                            if len(p[1]):
                                new_data.append(p)
                    elif len(data) == 21:
                        for p in enumerate(data[3:3+min(16, participants)], int(data[2])):
                            if len(p[1]):
                                new_data.append(p)
                    else:
                        raise ValueError("ValueError: Unrecognized or malformed packet.")

                    if len(new_data) >= participants and participants > 0:
                        try:
                            if new_data != self.participant_configurations[-1][:-1]:
                                self.participant_configurations.append(new_data+[participants])
                        except IndexError:
                            self.participant_configurations.append(new_data+[participants])
                        finally:
                            new_data = list()

                    progress_bar.update()

            self.participant_lookup = {x: [x] for i, x in self.participant_configurations[0][:-1]}

            for participant_row in self.participant_configurations[1:]:
                for i, participant_name in participant_row[:-1]:
                    matches = [(k, participant_name, commonprefix(" ".join((" ".join(self.participant_lookup[k]), participant_name)).split())) for k in self.participant_lookup.keys() if len(commonprefix(" ".join((" ".join(self.participant_lookup[k]), participant_name)).split()))]
                    if len(matches):
                        max_length = max([len(p) for *rest, p in matches])
                        match_row = [(k, n, p) for k, n, p in matches if len(p) == max_length]

                        for k, n, p in match_row:
                            if n not in self.participant_lookup[k]:
                                self.participant_lookup[k].append(n)
                                if len(p) < len(k):
                                    self.participant_lookup[p] = self.participant_lookup.pop(k)
                    else:
                        self.participant_lookup[participant_name] = [participant_name]

            #This is hacky but works. Change maybe?
            #Reverse keys and values.
            self.participant_lookup = {v:k for k, l in self.participant_lookup.items() for v in l}

            self.telemetry_data = [x for x in self.telemetry_data if len(x) == 689]

            try:
                self.race_end = [i for i, data in reversed(list(enumerate(self.telemetry_data))) if int(data[9]) & int('111', 2) == 3][0] + 1
            except IndexError:
                self.race_end = len(self.telemetry_data)

            try:
                self.race_finish = [i for i, data in reversed(list(enumerate(self.telemetry_data[:self.race_end]))) if int(data[9]) & int('111', 2) == 2][0] + 1
            except IndexError:
                self.race_finish = len(self.telemetry_data)

            try:
                self.race_p1_finish = [ix for ix, data in reversed(list(enumerate(self.telemetry_data[:self.race_finish]))) for i in range(int(data[4])) if int(data[182+i*9]) & int('01111111', 2) == 1 and int(data[184+i*9]) <= int(data[10])][0] + 1
            except IndexError:
                self.race_p1_finish = len(self.telemetry_data)

            try:
                self.race_start = [i for i, data in reversed(list(enumerate(self.telemetry_data[:self.race_p1_finish]))) if(int(data[2]) & int('11110000', 2)) >> 4 != 5 or int(data[2]) & int('00001111', 2) != 2][0] + 1
                #self.race_start = [i for i, data in reversed(list(enumerate(self.telemetry_data[:self.race_finish]))) if int(data[9]) & int('111', 2) == 0 or (int(data[2]) & int('11110000', 2)) >> 4 != 5][0] + 1
            except IndexError:
                self.race_start = 0

            #For some reason (probably loading lag?) the telemetry
            #doesn't immediately load standings or reset lap distance
            #to zero right away. Step through until we're in that
            #state.
            old_race_start = self.race_start
            number_participants = max([x[-1] for x in self.participant_configurations])
            try:
                while sum([int(self.telemetry_data[self.race_start][182+i*9]) & int('01111111', 2) for i in range(number_participants)]) == 0 or sum([int(self.telemetry_data[self.race_start][181+i*9]) for i in range(number_participants)]) != 0:
                    self.race_start += 1
            except IndexError:
                self.race_start = old_race_start

            participant_queue = deque(self.participant_configurations)
            participant_groups = [self.update_participants(participant_queue) for x in range(len(self.participant_configurations))]

            #Trim and partition the telemetry data, and attach participants.
            self.telemetry_data = [(list(g), x) for x, g in groupby(self.telemetry_data[self.race_start:self.race_end], key=lambda k: int(k[4]))]
            self.telemetry_data = [(g, x, y, p) for (g, x), y, p in zip(self.telemetry_data, [0]+list(cumsum([len(g) for g, x in self.telemetry_data])), participant_groups)]
            self.race_end = self.race_end-self.race_start
            self.race_finish = self.race_finish-self.race_start
            self.race_p1_finish = self.race_p1_finish-self.race_start
            self.race_start = self.race_start-self.race_start

            #Change the elapsed time values.
            time_adjust = min([x[-1] for y in self.telemetry_data for x in y[0] if x[-1] != -1])
            for tg_i, tele_group in enumerate(self.telemetry_data):
                for tele_i, tele_data in enumerate(tele_group[0]):
                    if self.telemetry_data[tg_i][0][tele_i][-1] != -1:
                        self.telemetry_data[tg_i][0][tele_i][-1] -= time_adjust

            '''
            data = self.telemetry_data[0][0]
            self.starting_grid = sorted(((str(int(data[182+i*9]) & int('01111111', 2)), n, t if t is not None else "", c) for i, n, t, c in self.participant_data), key=lambda x: int(x[0]))

            data = self.telemetry_data[self.race_finish]
            finishers = list()
            for i, n in self.participant_configurations[-1][:-1]:
                name = self.participant_lookup[n]
                finishers.append((i, name, self.team_data[name], self.car_data[name]))

            lead_lap_indexes = [i for i, *rest in finishers if int(data[184+i*9]) >= int(data[10])]
            lapped_indexes = [i for i, *rest in finishers if int(data[184+i*9]) < int(data[10])]

            data = self.telemetry_data[-1]
            self.classification = sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[10])) for i, n, t, c in finishers if i in lead_lap_indexes)
            self.classification += sorted((int(data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(data[183+i*9])) for i, n, t, c in finishers if i in lapped_indexes)
            self.classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(self.classification, 1)]
            import pdb; pdb.set_trace()
            '''

        except ValueError as e:
            print("{}".format(e), file=sys.stderr)
        finally:
            f.close()

    def update_participants(self, participant_queue):
        participant_data = list()
        for i, n in participant_queue.popleft()[:-1]:
            #Find the name in the lookup, to use the de-junked version of the name.
            name = self.participant_lookup[n]
            participant_data.append((i, name, self.team_data[name], self.car_data[name]))
            '''
            for clean__name, raw_names in self.participant_lookup.items():
                for raw_name in raw_names:
                    if name[1] == raw_name:
                        participant_data.append(name)
            '''
        #participant_data = [(i, n, t, c) for (i, n), t, c in zip(list(sorted({x for x in participant_data})), self.team_data, self.car_data)]
        return participant_data

    def process_telemetry(self):
        source_telemetry = self.source_telemetry
        telemetry_file = "tele.csv"
        with open(source_telemetry+telemetry_file, 'w') as csvfile:
            for a in natsorted(glob(source_telemetry+'pdata*')):
                with open(a, 'rb') as packFile:
                    packData = packFile.read()
                    if len(packData) == 1367:
                        packString  = "HB"
                        packString += "B"
                        packString += "bb"
                        packString += "BBbBB"
                        packString += "B"
                        packString += "21f"
                        packString += "H"
                        packString += "B"
                        packString += "B"
                        packString += "hHhHHBBBBBbffHHBBbB"
                        packString += "22f"
                        packString += "8B12f8B8f12B4h20H16f4H"
                        packString += "2f"
                        packString += "2B"
                        packString += "bbBbbb"

                        for participant in range(56):
                            packString += "hhhHBBBBf"
                        
                        packString += "fBBB"

                    elif len(packData) == 1028:
                        packString  = "HBB"

                        for participant in range(16):
                            packString += "64s"

                    elif len(packData) == 1347:
                        packString  = "HB64s64s64s64s"

                        for participant in range(16):
                            packString += "64s"

                        packString += "64x"

                    csvfile.write(",".join(str(x, encoding='utf-8', errors='ignore').replace('\x00', '') if isinstance(x, bytes) else str(x).replace('\x00', '') for x in unpack(packString, packData)+(a,))+"\n")
        
    def black_test(self):
        #Test file hash, because blackframe detection is slow, so we cache it.
        #Get stored file.
        try:
            with open(self.video_cache, 'r') as h:
                cache = csv.reader(h)

                for row in cache:
                    try:
                        if row[0] == os.path.realpath(self.source_video) and row[1] == self.__hashfile(open(self.source_video, 'rb'), sha256()):
                            videostart, videoend = float(row[2]), float(row[3])
                            return mpy.VideoFileClip(self.source_video).subclip(videostart, videoend)
                    except IndexError:
                        pass
                raise FileNotFoundError

        except FileNotFoundError:
            #Nothing found in the cache, so detect and add to cache.
            video = mpy.VideoFileClip(self.source_video)
            
            blackframes = [0] + [t for (t, f) in video.iter_frames(with_times=True, progress_bar=1) if f.mean() < self.video_threshold] + [video.duration]

            try:
                videostart = blackframes[where(diff(blackframes)>self.video_gaptime)[0][0+self.video_skipstart]]
            except IndexError:
                #Some replays don't use blackframes to separate frames. In this case
                #the only blackframes are the start and stop of the replay.
                videostart = blackframes[where(diff(blackframes)>self.video_gaptime)[0][0]]
                luminosity_difference = abs(diff([f.sum() for f in video.subclip(videostart,videostart+60).iter_frames(dtype=float, progress_bar=1)]))
                luminosity_average = luminosity_difference.mean()
                luminosity_jumps = 1+nonzero(luminosity_difference>10*luminosity_average)[0]
                tt = [videostart] + list((1.0/video.fps)*luminosity_jumps+videostart) + [videostart+60]
                try:
                    videostart = [tt[x] for x in nonzero(diff(tt)>1)[0]][0+self.video_skipstart]
                except IndexError:
                    videostart = 0

            try:
                videoend = blackframes[::-1][where(diff(blackframes[::-1])<-self.video_gaptime)[0][0+self.video_skipend]]
            except IndexError:
                #Some replays don't use blackframes to separate frames. In this case
                #the only blackframes are the start and stop of the replay.
                videoend = blackframes[::-1][where(diff(blackframes[::-1])<-self.video_gaptime)[0][0]]
                luminosity_difference = abs(diff([f.sum() for f in video.subclip(videoend-60,videoend).iter_frames(dtype=float, progress_bar=1)]))
                luminosity_average = luminosity_difference.mean()
                luminosity_jumps = 1+nonzero(luminosity_difference>10*luminosity_average)[0]
                tt = [videoend-60] + list((1.0/video.fps)*luminosity_jumps+videoend-60) + [videoend]
                try:
                    videoend = [tt[x] for x in nonzero(diff(tt)>1)[0]][0-self.video_skipend]
                except IndexError:
                    videoend = video.duration

            finally:
                with open(self.video_cache, 'a') as h:
                    cache = csv.writer(h)
                    cache.writerow([os.path.realpath(self.source_video), self.__hashfile(open(self.source_video, 'rb'), sha256()), videostart, videoend])
                return mpy.VideoFileClip(self.source_video).subclip(videostart, videoend)

    def __hashfile(self, afile, hasher, blocksize=65536):
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher.hexdigest()

    def __lsf(s1, s2):
        m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
        longest, x_longest = 0, 0
        for x in range(1, 1+len(s1)):
            for y in range(1, 1 + len(s2)):
                if s1[x-1] == s2[y-1]:
                    m[x][y] = m[x-1][y-1]+1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return s1[x_longest-longest:x_longest]

    @classmethod
    def new_configuration(cls):
        try:
            print("No configuration file provided.")
            print("Creating new configuration file.")

            config = Configuration()
            config.new_configuration()

            print("Creating low-quality video as {}".format(config.output_video))
            print("If video trimming needs to be adjusted, run the Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print("To synchronize telemetry with video, run the Project CARS Replay Enhancer with the `-r` option.")
            print("Set the synchronization offset to the value shown on the Timer when the viewed car crosses the start finish linee to begin lap 2.")
            print("Please wait. Telemetry being processed and rendered. If this is the first time this data has been used, it make take longer.")

            try:
                replay = cls(config.config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                start_video = replay.__build_default_video(False)
                end_video = replay.__build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips([start_video, end_video])
                output.write_videofile(replay.output_video, fps=10, preset='superfast')
        except KeyboardInterrupt:
            print("Aborting...")

    @classmethod
    def edit_configuration(cls, previous_file):
        try:
            print("Editing configuration file {}".format(previous_file))

            config = Configuration(previous_file)
            config.new_configuration()

            print("Creating low-quality video as {}".format(config.output_video))
            print("If video trimming needs to be adjusted, run the Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print("To synchronize telemetry with video, run the Project CARS Replay Enhancer with the `-r` option.")
            print("Set the synchronization offset to the value shown on the Timer when the viewed car crosses the start finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                start_video = replay.__build_default_video(False)
                end_video = replay.__build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips([start_video, end_video])
                output.write_videofile(replay.output_video, fps=10, preset='superfast')

        except KeyboardInterrupt:
            print("Aborting...")

    @classmethod
    def edit_trim(cls, previous_file):
        try:
            print("Editing configuration file {}".format(previous_file))

            config = Configuration(previous_file)
            config.modify_trim()

            print("Creating low-quality video as {}".format(config.output_video))
            print("If video trimming needs to be adjusted, run the Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print("To synchronize telemetry with video, run the Project CARS Replay Enhancer with the `-r` option.")
            print("Set the synchronization offset to the value shown on the Timer when the viewed car crosses the start finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                start_video = replay.__build_default_video(False)
                end_video = replay.__build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)

                output = mpy.concatenate_videoclips([start_video, end_video])
                output.write_videofile(replay.output_video, fps=10, preset='superfast')

        except KeyboardInterrupt:
            print("Aborting...")
            
    @classmethod
    def edit_racestart(cls, previous_file):
        try:
            print("Editing configuration file {}".format(previous_file))

            config = Configuration(previous_file)
            config.modify_racestart()

            print("Creating low-quality video as {}".format(config.output_video))
            print("If video trimming needs to be adjusted, run the Project CARS Replay Enhancer with the `-t` option.")
            print("\n")
            print("To synchronize telemetry with video, run the Project CARS Replay Enhancer with the `-r` option.")
            print("Set the synchronization offset to the value shown on the Timer when the viewed car crosses the start finish line to begin lap 2.")

            try:
                replay = cls(config.config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                start_video = replay.__build_default_video(False)
                end_video = replay.__build_default_video(False)

                start_video = start_video.set_duration(
                    start_video.duration).subclip(0, 185)
                if replay.show_champion:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-120)
                else:
                    end_video = end_video.set_duration(
                        end_video.duration).subclip(
                            end_video.duration-100)
                output = mpy.concatenate_videoclips([start_video, end_video])
                output.write_videofile(replay.output_video, fps=10, preset='superfast')

        except KeyboardInterrupt:
            print("Aborting...")

    @classmethod
    def create_custom(cls, config_file):
        try:
            print("Creating video with custom settings.")

            try:
                replay = cls(config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                output = replay.__build_default_video(False)
                #output.save_frame("outputs/frame1.png", output.duration-50)
                #output.save_frame("outputs/frame2.png", output.duration-30)
                #output.save_frame("outputs/frame3.png", output.duration-10)
                output.set_duration(output.duration).subclip(5, 15).write_videofile(replay.output_video, fps=10, preset='superfast')
        except KeyboardInterrupt:
            print("Aborting...")

    @classmethod
    def create_video(cls, config_file):
        try:
            print("Creating video.")

            try:
                replay = cls(config_file)
            except ValueError as e:
                print("Invalid JSON in configuration file: {}".format(e))
            else:
                output = replay.__build_default_video(True)
                output.write_videofile(replay.output_video, fps=30)
        except KeyboardInterrupt:
            print("Aborting...")

    def __build_default_video(self, process_data):
        if self.source_video is None:
            video = mpy.ColorClip((1280, 720), duration=self.telemetry_data[-1][0][-1][-1])
        elif isinstance(self.video_skipstart, float) or isinstance(self.video_skipend, float):
            video = mpy.VideoFileClip(self.source_video).subclip(self.video_skipstart, self.video_skipend)
        else:
            video = self.black_test()
        video_width, video_height = video.size

        if self.backdrop != "":
            backdrop = Image.open(self.backdrop).resize((video_width, video_height))
            if self.logo != "":
                logo = Image.open(self.logo).resize((self.logo_width, self.logo_height))
                backdrop.paste(logo, (backdrop.width-logo.width, backdrop.height-logo.height), logo)
        else:
            backdrop = Image.new('RGBA', (video_width, video_height), (0, 0, 0))
            if self.logo != "":
                logo = Image.open(self.logo).resize((self.logo_width, self.logo_height))
                backdrop.paste(logo, (backdrop.width-logo.width, backdrop.height-logo.height), logo)

        backdrop = mpy.ImageClip(PIL_to_npimage(backdrop))
        title = mpy.ImageClip(Title(self).to_frame()).set_duration(5).set_position(('center', 'center'))

        standing = UpdatedVideoClip(Standings(self, process_data=process_data))
        standing = standing.set_position((self.margin, self.margin)).set_duration(video.duration)
        standing_mask = mpy.ImageClip(Standings(self, process_data=process_data).make_mask(), ismask=True, duration=video.duration)
        standing = standing.set_mask(standing_mask)

        timer = UpdatedVideoClip(Timer(self, process_data=process_data))
        timer_width, timer_height = timer.size
        timer = timer.set_position((video_width-timer_width-self.margin, self.margin)).set_duration(video.duration)
        timer_mask = mpy.ImageClip(Timer(self, process_data=process_data).make_mask(), ismask=True, duration=video.duration)
        timer = timer.set_mask(timer_mask)

        result = mpy.ImageClip(Results(self).to_frame()).set_duration(20).set_position(('center', 'center')).add_mask()
        result.mask = result.mask.fx(vfx.fadeout, 1)

        series_standings = mpy.ImageClip(SeriesStandings(self).to_frame()).set_start(20).set_duration(20).set_position(('center', 'center')).add_mask()

        if self.show_champion:
            series_standings.mask = series_standings.mask.fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
            champion = mpy.ImageClip(Champion(self).to_frame()).set_start(40).set_duration(20).set_position(('center', 'center')).add_mask()
            champion.mask = champion.mask.fx(vfx.fadein, 1)
        else:
            series_standings.mask = series_standings.mask.fx(vfx.fadein, 1)

        intro = mpy.CompositeVideoClip([backdrop, title]).set_duration(5).fx(vfx.fadeout, 1)
        mainevent = mpy.CompositeVideoClip([video, standing, timer]).set_duration(video.duration)

        if self.show_champion:
            outro = mpy.CompositeVideoClip([backdrop, result, series_standings, champion]).set_duration(sum([x.duration for x in [result, series_standings, champion]])).fx(vfx.fadein, 1)
        else:
            outro = mpy.CompositeVideoClip([backdrop, result, series_standings]).set_duration(sum([x.duration for x in [result, series_standings]])).fx(vfx.fadein, 1)

        output = mpy.concatenate_videoclips([intro, mainevent, outro])
        return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Project CARS Replay Enhancer")
    parser.add_argument('-v', '--version', action='version', 
        version='Version 0.3')
    parser.add_argument('configuration', nargs='?')
    parser.add_argument('-c', '--configure', action='store_true',
        help='create or edit configuration file')
    parser.add_argument('-u', '--custom', action='store_true',
        help=argparse.SUPPRESS)
    parser.add_argument('-r', '--racestart', action='store_true',
        help='modify race start for telemetry sync')
    parser.add_argument('-t', '--trim', action='store_true',
        help='modify video trim parameters')
        
    arguments = parser.parse_args()

    error_message = ""
    if arguments.racestart is True and arguments.configuration is None:
        error_message += "\n-r, --racestart requires a provided confguration file."
    if arguments.trim is True and arguments.configuration is None:
        error_message += "\n-t, --trim requires a provided configuration file."

    if len(error_message):
        parser.error(error_message)

    if arguments.custom is True:
        try:
            ReplayEnhancer.create_custom(arguments.configuration)
        except FileNotFoundError:
            parser.error("\n{} not found. Aborting.".format(arguments.configuration))
    elif arguments.configure is True:
        if arguments.configuration is None:
            ReplayEnhancer.new_configuration()
        else:
            try:
                ReplayEnhancer.edit_configuration(arguments.configuration)
            except FileNotFoundError:
                parser.error("\n{} not found. Aborting.".format(arguments.configuration))
    elif arguments.trim is True:
        try:
            ReplayEnhancer.edit_trim(arguments.configuration)
        except FileNotFoundError:
            parser.error("\n{} not found. Aborting.".format(arguments.configuration))
    elif arguments.racestart is True:
        try:
            ReplayEnhancer.edit_racestart(arguments.configuration)
        except FileNotFoundError:
            parser.error("\n{} not found. Aborting.".format(arguments.configuration))
    else:
        if arguments.configuration is None:
            ReplayEnhancer.new_configuration()
        else:
            try:
                ReplayEnhancer.create_video(arguments.configuration)
            except FileNotFoundError:
                parser.error("\n{} not found. Aborting.".format(arguments.configuration))

    '''
    if len(sys.argv) == 1:
        print("No configuration file provided.")
        print("Do you want to create a new configuration file?")

        while True:
            create_config = input("[Y/n]-->> ")
            if len(create_config) == 0 or \
                    str.lower(create_config) == "y":
                config = Configuration()
                break;
            elif str.lower(create_config) == "n":
                print ("Usage: python ReplayEnhancer.py",
                    "<configuration_file")
                break



    try:
        replay = ReplayEnhancer(sys.argv[1])
    except ValueError as e:
        print("Invalid JSON in configuration file: {}".format(e))
    else:
        if replay.source_video is None:
            video = mpy.ColorClip((1280, 720), duration=replay.telemetry_data[-1][0][-1][-1])
        else:
            video = replay.black_test()
        video_width, video_height = video.size

        if replay.backdrop != "":
            backdrop = Image.open(replay.backdrop).resize((video_width, video_height))
            if replay.logo != "":
                logo = Image.open(replay.logo).resize((replay.logo_width, replay.logo_height))
                backdrop.paste(logo, (backdrop.width-logo.width, backdrop.height-logo.height), logo)
        else:
            backdrop = Image.new('RGBA', (video_width, video_height), (0, 0, 0))
            if replay.logo != "":
                logo = Image.open(replay.logo).resize((replay.logo_width, replay.logo_height))
                backdrop.paste(logo, (backdrop.width-logo.width, backdrop.height-logo.height), logo)

        backdrop = mpy.ImageClip(PIL_to_npimage(backdrop))
        title = mpy.ImageClip(Title(replay).to_frame()).set_duration(6).set_position(('center', 'center'))

        standing = UpdatedVideoClip(Standings(replay, process_data=True))
        standing = standing.set_position((replay.margin, replay.margin)).set_duration(video.duration)
        standing_mask = mpy.ImageClip(Standings(replay).make_mask(), ismask=True, duration=video.duration)
        standing = standing.set_mask(standing_mask)

        timer = UpdatedVideoClip(Timer(replay, process_data=True))
        timer_width, timer_height = timer.size
        timer = timer.set_position((video_width-timer_width-replay.margin, replay.margin)).set_duration(video.duration)
        timer_mask = mpy.ImageClip(Timer(replay).make_mask(), ismask=True, duration=video.duration)
        timer = timer.set_mask(timer_mask)

        result = mpy.ImageClip(Results(replay).to_frame()).set_duration(20).set_position(('center', 'center')).add_mask()
        result.mask = result.mask.fx(vfx.fadeout, 1)

        series_standings = mpy.ImageClip(SeriesStandings(replay).to_frame()).set_start(20).set_duration(20).set_position(('center', 'center')).add_mask()

        if replay.show_champion:
            series_standings.mask = series_standings.mask.fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
            champion = mpy.ImageClip(Champion(replay).to_frame()).set_start(40).set_duration(20).set_position(('center', 'center')).add_mask()
            champion.mask = champion.mask.fx(vfx.fadein, 1)
        else:
            series_standings.mask = series_standings.mask.fx(vfx.fadein, 1)

        intro = mpy.CompositeVideoClip([backdrop, title]).set_duration(6).fx(vfx.fadeout, 1)
        mainevent = mpy.CompositeVideoClip([video, standing, timer]).set_duration(video.duration)

        if replay.show_champion:
            outro = mpy.CompositeVideoClip([backdrop, result, series_standings, champion]).set_duration(sum([x.duration for x in [result, series_standings, champion]])).fx(vfx.fadein, 1)
        else:
            outro = mpy.CompositeVideoClip([backdrop, result, series_standings]).set_duration(sum([x.duration for x in [result, series_standings]])).fx(vfx.fadein, 1)

        output = mpy.concatenate_videoclips([intro, mainevent, outro])

        #title.save_frame("outputs/title.jpg", 0)
        #series_standings.save_frame("outputs/series_standings.jpg", 0)

        #Full video.
        #output.write_videofile(replay.output_video, fps=30)
        
        #Full video, low framerate
        #output.write_videofile(replay.output_video, fps=10)

        #Subclip video.
        #output.subclip(1*60+50, 2*60).write_videofile(replay.output_video, fps=10, preset='superfast')
        output.subclip(0, 8).write_videofile(replay.output_video, fps=10, preset='superfast')
        #output.subclip(1020, 1260).write_videofile(replay.output_video, fps=10, preset='superfast')
        #output.subclip(output.duration-80, output.duration).write_videofile(replay.output_video, fps=10)

        #Single frame.
        #output.save_frame(replay.output_video+".jpg", 400)

        #Multiple frames.
        #for frame in range(int(output.duration-45), int(output.duration-25)):
            #output.save_frame(replay.output_video+"."+str(frame)+".jpg", frame)
    '''
