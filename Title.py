"""
Provides the default Title for the Project CARS Replay Enhancer.
"""
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Title(StaticBase):
    """
    Defines a static Title card, consisting of the following columns:

    - Starting Position
    - Driver Name
    - Team (if provided)
    - Car
    """
    def __init__(self, replay):
        self.replay = replay

        self.starting_grid = sorted(
            self.replay.race_data.starting_grid,
            key=lambda x: int(x[0]))[:16]
        self.starting_grid = [
            tuple(
                ["" if y is None else str(y) for y in x]
            )
            for x in self.starting_grid]

        self.widths = list()
        self.data_height = int(0)
        self.material = Image.new(
            'RGBA',
            (100, 100))

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)

        y_pos = self.replay.margin

        draw.text((20, y_pos),
                  self.replay.heading_text,
                  fill=self.replay.heading_font_color,
                  font=self.replay.heading_font)
        y_pos += self.replay.heading_font.getsize(
            self.replay.heading_text
            )[1]

        draw.text((20, y_pos),
                  self.replay.subheading_text,
                  fill=self.replay.heading_font_color,
                  font=self.replay.font)
        y_pos += self.replay.font.getsize(
            self.replay.subheading_text
            )[1]+self.replay.margin
        y_pos += self.replay.margin/2

        column_positions = [self.replay.margin if i == 0 \
            else self.replay.margin+self.replay.column_margin*i+sum(
                self.widths[0:i]
                ) if self.widths[i-1] != 0 \
            else self.replay.margin+self.replay.column_margin*(i-1)+sum(
                self.widths[0:(i-1)]
                ) \
            for i, w in enumerate(self.widths)]

        for position, name, team, car, car_class in \
                [list(zip(x, column_positions)) \
                    for x in self.starting_grid]:
            draw.text((position[1], y_pos),
                      str(position[0]),
                      fill=self.replay.font_color,
                      font=self.replay.font)
            draw.text((name[1], y_pos),
                      str(name[0]),
                      fill=self.replay.font_color,
                      font=self.replay.font)
            draw.text((team[1], y_pos),
                      str(team[0]),
                      fill=self.replay.font_color,
                      font=self.replay.font)
            draw.text((car[1], y_pos),
                      str(car[0]),
                      fill=self.replay.font_color,
                      font=self.replay.font)
            if len(car_class[0]):
                color = [data['color'] \
                    for _, data in self.replay.car_classes.items() \
                    if car[0] in data['cars']][0]
                x_divisions = int(self.data_height/3)
                draw.polygon(
                    [
                        (car_class[1], y_pos+self.data_height),
                        (car_class[1]+x_divisions, y_pos),
                        (car_class[1]+x_divisions*3, y_pos),
                        (
                            car_class[1]+x_divisions*2,
                            y_pos+self.data_height)],
                    fill=tuple(color))
                draw.text((car_class[1]+self.data_height, y_pos),
                          str(car_class[0]),
                          fill=self.replay.font_color,
                          font=self.replay.font)
            y_pos += self.data_height+self.replay.margin

        return self.material

    def _make_material(self, bgOnly):
        self.widths = [max([self.replay.font.getsize(str(x[i]))[0] \
            for x in self.starting_grid]) \
            for i in range(len(self.starting_grid[0]))]
        self.widths.append(sum(self.widths))

        heights = [max([self.replay.font.getsize(str(x[i]))[1] \
            for x in self.starting_grid]) \
            for i in range(len(self.starting_grid[0]))]
        self.data_height = max(heights)
        heights = [self.data_height for x in self.starting_grid]
        heights.append(
            self.replay.heading_font.getsize(
                self.replay.heading_text)[1])
        heights.append(
            self.replay.font.getsize(
                self.replay.subheading_text)[1])

        header_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]
        header_height += self.replay.font.getsize(
            self.replay.subheading_text)[1]
        header_height += self.replay.margin*2

        text_width = max(
            self.widths[-1]+self.replay.column_margin*(len(
                [x for x in self.widths[:-1] if x != 0])-1),
            self.replay.heading_font.getsize(
                self.replay.heading_text)[0]+ \
                self.replay.column_margin+ \
                header_height,
            self.replay.font.getsize(
                self.replay.subheading_text)[0]+ \
                self.replay.column_margin+ \
                header_height)
        if any([car_class \
                for _, _, _, _, car_class in self.starting_grid]):
            text_width += self.data_height
        text_height = sum(heights)+self.replay.margin*len(heights)-1

        heading_material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, header_height),
            self.replay.heading_color)

        if self.replay.series_logo is not None:
            series_logo = Image.open(
                self.replay.series_logo
                ).resize(
                    (heading_material.height, heading_material.height))
            heading_material.paste(
                series_logo,
                (heading_material.width-series_logo.width, 0))

        self.material = self.material.resize(
            (text_width+self.replay.margin*2, text_height))
        self.material.paste(heading_material, (0, 0))

        y_pos = header_height
        for i, _ in enumerate(self.starting_grid):
            if i % 2:
                material_color = (255, 255, 255, 255)
            else:
                material_color = (192, 192, 192, 255)

            row_material = Image.new(
                'RGBA',
                (
                    text_width+self.replay.margin*2,
                    self.data_height+self.replay.margin),
                material_color)
            self.material.paste(row_material, (0, y_pos))
            y_pos += self.data_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

    def to_frame(self):
        return super(Title, self).to_frame()

    def make_mask(self):
        return super(Title, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Title, StaticBase))
    print('Instance:', isinstance(Title(0), StaticBase))
