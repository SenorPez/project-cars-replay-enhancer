"""
Provides classes for the creation of a GT Sport style
Standings overlay.
"""

from PIL import Image, ImageDraw, ImageFont

from DynamicBase import DynamicBase
from RaceStandings import Driver, ParticipantData

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

        self.material = None

    def _write_data(self):
        return self.material

    def _make_material(self, bgOnly):
        self.standings = self.update(force_process=True)

        height = self.replay.font.getsize(
            "ABCD")[1]
        self.material = Image.new(
            'RGBA',
            (
                200,
                height*2*10+1*9)
            )
        
        y_position = 0
        for driver in self.standings[:10]:
            position_material = Image.new(
                'RGBA',
                (
                    height*2,
                    height*2),
                (0, 0, 0, 255))
            name_material = Image.new(
                'RGBA',
                (
                    200-height*2,
                    height*2),
                (51, 51, 51, 255))
            self.material.paste(
                position_material,
                (0, y_position))
            self.material.paste(
                name_material,
                (height*2, y_position))
            y_position += height*2+1

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

