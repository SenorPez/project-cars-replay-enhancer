"""
Provides the default Series Champion screen for the Project CARS
Replay Enhancer
"""
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Champion(StaticBase):
    """
    Defines a static Champion card, consisting of the top three
    finishers in points, as Champions and Runners Up.
    """
    _classification = None

    def __init__(self, replay):
        self.replay = replay
        self.race_data = self.replay.race_data

        participants = {
            x for x in self.replay.participant_lookup.values()}
        self.lap_finish = {n:None for n in participants}

        self.material = None
        self.heading_height = None

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)
        classification = self.classification

        draw.text(
            (self.replay.margin, self.replay.margin),
            self.replay.heading_text,
            fill=self.replay.heading_font_color,
            font=self.replay.heading_font)

        x_pos = 300+self.replay.margin
        y_pos = self.heading_height+self.replay.margin

        for rank, name, team, car, _ in classification:
            if rank == 1:
                draw.text(
                    (x_pos, y_pos),
                    "Champion",
                    fill=self.replay.font_color,
                    font=self.replay.heading_font)
                y_pos += self.replay.heading_font.getsize("Champion")[1]
                draw.text(
                    (x_pos, y_pos),
                    self.format_string(name),
                    fill=self.replay.font_color,
                    font=self.replay.heading_font)
                y_pos += self.replay.heading_font.getsize(name)[1]
            else:
                draw.text(
                    (x_pos, y_pos),
                    "Runner Up",
                    fill=self.replay.font_color,
                    font=self.replay.font)
                y_pos += self.replay.font.getsize("Runner Up")[1]
                draw.text(
                    (x_pos, y_pos),
                    self.format_string(name),
                    fill=self.replay.font_color,
                    font=self.replay.font)
                y_pos += self.replay.font.getsize(name)[1]
            draw.text(
                (x_pos+self.replay.column_margin, y_pos),
                self.format_string(team),
                fill=self.replay.font_color,
                font=self.replay.font)
            y_pos += self.replay.font.getsize(team)[1]
            draw.text(
                (x_pos+self.replay.column_margin, y_pos),
                self.format_string(car),
                fill=self.replay.font_color,
                font=self.replay.font)
            y_pos += self.replay.font.getsize(car)[1]+self.replay.margin

        return self.material

    def _make_material(self, bgOnly):
        classification = self.classification

        heading_width = self.replay.heading_font.getsize(
            self.replay.heading_text)[0]+self.replay.margin*2
        text_width = max(
            [max(
                [self.replay.heading_font.getsize(n)[0] \
                     if r == 1 \
                     else self.replay.font.getsize(n)[0],
                 self.replay.font.getsize(t)[0]+\
                    self.replay.column_margin,
                 self.replay.font.getsize(c)[0]+\
                    self.replay.column_margin]) \
            for r, n, t, c, _ \
            in classification]+\
                [self.replay.heading_font.getsize("Champion")[0]]+\
                [self.replay.font.getsize("Runner Up")[0]])+\
                self.replay.margin*2

        self.heading_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]+self.replay.margin*2
        text_height = max(
            [300, sum(
                [self.replay.heading_font.getsize(n)[1]+\
                    self.replay.font.getsize(t)[1]+\
                    self.replay.font.getsize(c)[1] \
                    if r == 1 \
                    else self.replay.font.getsize(n)[1]+\
                    self.replay.font.getsize(t)[1]+\
                    self.replay.font.getsize(c)[1] \
                    for r, n, t, c, _ \
                    in classification]+\
                    [self.replay.heading_font.getsize("Champion")[1]]+\
                    [self.replay.font.getsize("Runner Up")[1]*2])+\
                    self.replay.margin*4])

        width = max((heading_width, 300+text_width))
        height = self.heading_height+text_height

        heading_material = Image.new(
            'RGBA',
            (width, self.heading_height),
            self.replay.heading_color)

        self.material = Image.new(
            'RGBA',
            (width, height),
            (255, 255, 255))
        self.material.paste(heading_material, (0, 0))

        if self.replay.series_logo is not None:
            series_logo = Image.open(
                self.replay.series_logo).resize((300, 300))
            self.material.paste(
                series_logo,
                (0, self.heading_height))

        return self.material if bgOnly else self._write_data()

    @property
    def classification(self):
        """
        Returns the top three in series points.
        """
        if self._classification is None:
            self._classification = self.race_data.classification

        classification = sorted(
            [(line[1], line[2], line[3], line[12]) \
                for line \
                in self._classification],
            key=lambda x: -x[-1])[:3]

        for rank, data in enumerate(classification):
            if rank == 0:
                classification[rank] = (rank+1,)+data
            elif classification[rank-1][-1] == data[-1]:
                classification[rank] = (classification[rank-1][0],)+\
                    data
            else:
                classification[rank] = (rank+1,)+data

        return classification

    def to_frame(self):
        return super(Champion, self).to_frame()

    def make_mask(self):
        return super(Champion, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Champion, StaticBase))
    print('Instance:', isinstance(Champion(0), StaticBase))
