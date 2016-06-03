"""
Provides classes for the creation of a GT Sport style
Standings overlay.
"""

from PIL import Image, ImageDraw

from DynamicBase import DynamicBase
from RaceStandings import ParticipantData

class GTStandings(DynamicBase):
    """
    Creates a standings overlay that constaly updates with the
    following columns of information:
    Position | Driver | Lap / Sector Times | Lap Difference

    Up to 10 drivers are displayed.
    Positions 1-5 are always displayed.
    Postions n-2 through n+2, where n is the viewed car are
        displayed if there is no overlap with P1-5.
    Additional positions are added to display 10.
    """

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

        self.participant_data = ParticipantData()
        self.standings = None

        self.material = None

    def __filter_drivers(self):
        subject_position = self.participant_data.drivers_by_index[0].\
            race_position
        last_place = self.participant_data.last_place

        if subject_position <= 8:
            return self.participant_data.drivers_by_position[:10]
        elif subject_position == last_place \
                or subject_position+1 == last_place:
            return self.participant_data.drivers_by_position[:5] + \
                self.participant_data.drivers_by_position[-5:]
        else:
            #Remember that python is 0-indexed.
            slice_start = subject_position-3
            slice_end = subject_position+2
            return self.participant_data.drivers_by_position[:5] + \
                self.participant_data.drivers_by_position[\
                    slice_start:slice_end]

    def _write_data(self):
        _, text_height = \
            self.participant_data.max_name_dimensions(
                self.replay.font)

        #Determine the height without taking descenders into account.
        block_height = self.replay.font.getsize("A")[1]

        y_position = int(
            (text_height*2-block_height)/2)+self.replay.margin

        draw = ImageDraw.Draw(self.material)

        for driver in self.__filter_drivers():
            position_width = self.replay.font.getsize(
                str(driver.race_position))[0]
            x_position = int(
                (text_height*2-position_width)/2)+self.replay.margin

            text_color = (0, 0, 0) \
                if driver.viewed \
                else (255, 255, 255)

            draw.text(
                (x_position, y_position),
                str(driver.race_position),
                fill=text_color,
                font=self.replay.font)

            x_position = text_height*2+10+self.replay.margin

            draw.text(
                (x_position, y_position),
                str(driver.name),
                fill=text_color,
                font=self.replay.font)

            y_position += text_height*2+1

        return self.material

    def _make_material(self, bgOnly):
        self.standings = self.update(force_process=True)

        text_width, text_height = \
            self.participant_data.max_name_dimensions(
                self.replay.font)
        material_width = self.replay.margin+\
            text_height*2+text_width+10*2
        self.material = Image.new(
            'RGBA',
            (
                material_width,
                self.replay.margin+text_height*2*10+1*11)
            )

        y_position = self.replay.margin
        last_race_position = None
        for driver in self.__filter_drivers():
            position_material_color = (255, 215, 0, 210) \
                if driver.viewed \
                else (0, 0, 0, 210)
            name_material_color = (255, 215, 0, 210) \
                if driver.viewed \
                else (51, 51, 51, 210)

            position_material = Image.new(
                'RGBA',
                (
                    text_height*2,
                    text_height*2),
                position_material_color)
            name_material = Image.new(
                'RGBA',
                (
                    text_width+10*2,
                    text_height*2),
                name_material_color)
            self.material.paste(
                position_material,
                (self.replay.margin, y_position))
            self.material.paste(
                name_material,
                (self.replay.margin+text_height*2, y_position))

            if last_race_position is None:
                draw = ImageDraw.Draw(self.material)
                draw.line(
                    [
                        (
                            0,
                            self.replay.margin),
                        (
                            material_width,
                            self.replay.margin)],
                    fill='white',
                    width=1)
            elif last_race_position+1 != driver.race_position:
                draw = ImageDraw.Draw(self.material)
                draw.line(
                    [
                        (
                            0,
                            y_position),
                        (
                            material_width,
                            y_position)],
                    fill='white',
                    width=1)

            last_race_position = driver.race_position
            y_position += text_height*2+1

        draw = ImageDraw.Draw(self.material)
        draw.line(
            [
                (
                    0,
                    y_position),
                (
                    material_width,
                    y_position)],
            fill='white',
            width=1)

        return self.material if bgOnly else self._write_data()

    def update(self, force_process=False):
        if self.process_data or force_process:
            if self.clip_t > self.replay.sync_racestart:
                try:
                    telemetry_data, participant_data = \
                        [(x[0], x[-1]) \
                            for x in self.replay.telemetry_data \
                            if x[0][-1][-1] > \
                            self.clip_t-self.replay.sync_racestart][0]
                    telemetry_data = \
                        [x for x in telemetry_data \
                        if x[-1] > \
                            self.clip_t-self.replay.sync_racestart][0]
                except IndexError:
                    telemetry_data, participant_data, index_offset = \
                        [(x[0], x[-1], x[2]) \
                            for x in self.replay.telemetry_data \
                            if x[2] < self.replay.race_finish][-1]
                    telemetry_data = \
                        telemetry_data[self.replay.race_finish-\
                            index_offset]
            else:
                telemetry_data = self.replay.telemetry_data[0][0][0]
                participant_data = self.replay.telemetry_data[0][-1]

            self.participant_data.update_drivers(
                telemetry_data,
                participant_data)

        self.clip_t += float(1/self.ups)

        return self.participant_data.drivers_by_position

    def to_frame(self):
        return super(GTStandings, self).to_frame()

    def make_mask(self):
        return super(GTStandings, self).make_mask()

