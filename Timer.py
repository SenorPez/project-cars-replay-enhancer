from PIL import Image, ImageDraw
from numpy import diff, nonzero

from DynamicBase import DynamicBase

class Timer(DynamicBase):
    _clip_t = 0
    _ups = 30

    @property
    def clip_t(self):
        return self._clip_t

    @clip_t.setter
    def clip_t(self, value):
        self._clip_t = value

    @property
    def ups(self):
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

    def __init__(self, replay, clip_t=0, ups=30, process_data=True):
        self.replay = replay
        self.clip_t = clip_t
        self.ups = ups
        self.process_data = process_data

        self.time = -1
        self.lap = -1
        self.data_height = -1

        #Whats the slowest lap time in the entire race.
        #Used for sizing.
        telemetry_data = [x for x in zip(*self.replay.telemetry_data)][0]
        telemetry_data = [item for chunk in telemetry_data for item in chunk]
        split_data = [[float(telemetry_data[y+1][186+i*9]) for y in nonzero(diff([float(x[186+i*9]) for x in telemetry_data]))[0].tolist()] for i in range(56)]
        self.max_lap_time = self.format_time(max([sum(x[i:i+3]) for x in split_data for i in range(0, len(x), 3)]))
        self.max_laps = "{}/{}".format(telemetry_data[0][10], telemetry_data[0][10])

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)
        draw.text((self.replay.margin, int(self.replay.margin/2)), self.format_time(self.time), fill='black', font=self.replay.font)
        draw.text((self.replay.margin, self.data_height+int(self.replay.margin*1.5)), self.lap, fill='black', font=self.replay.font)

        return self.material

    def _make_material(self, bgOnly):
        self.time, self.lap = self.update(force_process=True)

        self.data_height = max((self.replay.font.getsize(self.time)[1], self.replay.font.getsize(self.lap)[1]))
        text_height = sum((self.replay.font.getsize(self.time)[1], self.replay.font.getsize(self.lap)[1], self.replay.margin))

        text_width = max((self.replay.font.getsize(str(self.max_lap_time))[0], self.replay.font.getsize(self.max_laps)[0]))
        
        self.material = Image.new('RGBA', (text_width+self.replay.margin*2, text_height+self.replay.margin*2))

        topMaterial = Image.new('RGBA', (text_width+self.replay.margin*2, self.data_height+self.replay.margin), (255, 255, 255, 128))
        self.material.paste(topMaterial, (0, 0))

        bottomMaterial = Image.new('RGBA', (text_width+self.replay.margin*2, self.data_height+self.replay.margin), (192, 192, 192, 128))
        self.material.paste(bottomMaterial, (0, self.data_height+self.replay.margin))

        return self.material if bgOnly else self._write_data()

    def update(self, force_process=False):
        if self.process_data or force_process:
            if self.clip_t > self.replay.sync_racestart:
                try:
                    telemetry_data, participant_data = [(x[0], x[-1]) for x in self.replay.telemetry_data if x[0][-1][-1] > self.clip_t-self.replay.sync_racestart][0]
                    telemetry_data = [x for x in telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0]
                    currentLap = min((int(telemetry_data[10]), int(telemetry_data[184+int(telemetry_data[3])*9])))
                    self.lap = "{}/{}".format(currentLap, telemetry_data[10])
                    #self.time = "{:.2f}".format(float([x for x in self.replay.telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0][13]))
                    #data = [x for x in self.replay.telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0]
                except IndexError:
                    telemetry_data, participant_data, index_offset = [(x[0], x[-1], x[2]) for x in self.replay.telemetry_data if x[2] < self.replay.race_finish][-1]
                    telemetry_data = telemetry_data[self.replay.race_finish-index_offset]

                    #Instead of the current lap, since we're freezing, we grab the completed laps.
                    currentLap = min((int(telemetry_data[10]), int(telemetry_data[183+int(telemetry_data[3])*9])))
                    self.lap = "{}/{}".format(currentLap, telemetry_data[10])
                    #raceFinish = [i for i, data in reversed(list(enumerate(self.replay.telemetry_data))) if int(data[9]) & int('111', 2)  == 2][0] + 1
                    #self.time = "{:.2f}".format(float(self.replay.telemetry_data[raceFinish][13]))
                    #data = self.replay.telemetry_data[raceFinish]

                #self.time = "{:.2f}".format(float([x for x in telemetry_data if x[-1] > self.clip_t-self.replay.sync_racestart][0][13]))
                self.time = "{:.2f}".format(float(telemetry_data[13]))
            else:
                telemetry_data = self.replay.telemetry_data[0][0][0]
                self.time = "0.00"
                self.lap = "{}/{}".format(1, telemetry_data[10])

            #self.time = "{:.2f}".format(self.clip_t)
        self.clip_t += float(1/self.ups)

        return self.time, self.lap

    def to_frame(self):
        return super(Timer, self).to_frame()

    def make_mask(self):
        return super(Timer, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Timer, DynamicBase))
    print('Instance:', isinstance(Timer(30), DynamicBase))
