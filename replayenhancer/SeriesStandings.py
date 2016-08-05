"""
Provides the default Series Standings screen for the Project CARS
Replay Enhancer
"""
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class SeriesStandings(StaticBase):
    """
    Defines a static Series Standings card, consisting of the following
    columns:

    - Series Position (Ties share a number)
    - Driver Name
    - Team (if provided)
    - Car
    - Series Points
    """
    _classification = None

    def __init__(self, replay, lines=None, car_class=None):
        self.replay = replay
        self.race_data = self.replay.race_data

        self.car_class = car_class

        self.material = None
        self.widths = None
        self.row_height = None

        self.lines = lines

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)
        classification = self.classification_with_headings

        y_pos = self.replay.margin

        draw.text(
            (20, y_pos),
            self.replay.heading_text,
            fill=self.replay.heading_font_color,
            font=self.replay.heading_font)
        y_pos += self.replay.heading_font.getsize(
            self.replay.heading_text)[1]

        draw.text(
            (20, y_pos),
            self.replay.subheading_text,
            fill=self.replay.heading_font_color,
            font=self.replay.font)
        y_pos += self.replay.font.getsize(
            self.replay.subheading_text)[1]+int(self.replay.margin*1.5)

        column_positions = [self.replay.margin if i == 0 \
            else self.replay.margin+self.replay.column_margin*i+sum(
                self.widths[0:i]) if self.widths[i-1] != 0 \
                    else self.replay.margin+\
                        self.replay.column_margin*(i-1)+\
                        sum(self.widths[0:(i-1)])
                            for i, w in enumerate(self.widths)]

        for rank, name, team, car, car_class, points \
                in [list(zip(x, column_positions)) \
                for x in classification]:
            draw.text(
                (rank[1], y_pos),
                self.format_string(rank[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (name[1], y_pos),
                self.format_string(name[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (team[1], y_pos),
                self.format_string(team[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (car[1], y_pos),
                self.format_string(car[0]),
                fill=self.replay.font_color,
                font=self.replay.font)

            try:
                color = [data['color'] \
                    for _, data in self.replay.car_classes.items() \
                    if car[0] in data['cars']][0]
                x_divisions = int(self.row_height/3)
                draw.polygon(
                    [
                        (car_class[1], y_pos+self.row_height),
                        (car_class[1]+x_divisions, y_pos),
                        (car_class[1]+x_divisions*3, y_pos),
                        (
                            car_class[1]+x_divisions*2,
                            y_pos+self.row_height
                        )
                    ],
                    outline=(0, 0, 0),
                    fill=tuple(color))
                x_adj = 0
            except IndexError:
                if car_class[0] is None:
                    x_adj = 0
                else:
                    x_adj = -self.row_height

            draw.text(
                (car_class[1]+x_adj+self.row_height, y_pos),
                self.format_string(car_class[0]),
                fill=self.replay.font_color,
                font=self.replay.font)

            if car_class[0] is None:
                x_adj = 0
            else:
                x_adj = self.row_height

            draw.text(
                (points[1]+x_adj+(self.widths[5]-\
                    self.replay.font.getsize(
                        self.format_string(points[0]))[0])/2, y_pos),
                self.format_string(points[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            y_pos += self.row_height+self.replay.margin
        return self.material

    def _make_material(self, bgOnly):
        classification = self.classification_with_headings

        self.widths = [max([self.replay.font.getsize(
            self.format_string(x[i]))[0] \
            for x \
                in [data if data is not None else "" \
                    for data in classification]]) \
            for i in range(len(classification[0]))]
        self.widths.append(sum(self.widths))

        heights = [max([self.replay.font.getsize(
            self.format_string(x[i]))[1] \
            for x \
                in [data if data is not None else "" \
                    for data in classification]]) \
            for i in range(len(classification[0]))]
        self.row_height = max(heights)
        heights = [self.row_height for x in classification]
        heights.append(self.replay.heading_font.getsize(
            self.replay.heading_text)[1])
        heights.append(self.replay.font.getsize(
            self.replay.subheading_text)[1])

        heading_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]+\
            self.replay.font.getsize(
                self.replay.subheading_text)[1]+self.replay.margin*2

        text_width = max(
            self.widths[-1]+self.replay.column_margin*(len(
                [x for x in self.widths[:-1] if x != 0])-1),
            self.replay.heading_font.getsize(
                self.replay.heading_text)[0]+\
                self.replay.column_margin+heading_height,
            self.replay.font.getsize(
                self.replay.subheading_text)[0]+\
                self.replay.column_margin+heading_height)
        if len(self.replay.car_classes):
            text_width += self.row_height
        text_height = sum(heights)+self.replay.margin*len(heights)-1

        heading_material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, heading_height),
            self.replay.heading_color)

        if self.replay.series_logo is not None:
            series_logo = Image.open(
                self.replay.series_logo).resize(
                    (heading_material.height, heading_material.height))
            heading_material.paste(
                series_logo,
                (heading_material.width-series_logo.width,
                 0))

        self.material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, text_height))
        self.material.paste(
            heading_material,
            (0, 0))

        y_pos = heading_height
        for i, _ in enumerate(classification):
            if i % 2:
                material_color = (255, 255, 255, 255)
            else:
                material_color = (192, 192, 192, 255)

            row_material = Image.new(
                'RGBA',
                (
                    text_width+self.replay.margin*2,
                    self.row_height+self.replay.margin),
                material_color)
            self.material.paste(row_material, (0, y_pos))
            y_pos += self.row_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

    @property
    def classification(self):
        """
        Returns the classficiation, trimmed to the number of lines
        specified.
        """
        if self._classification is None and self.car_class is None:
            self._classification = self.race_data.classification
        elif self._classification is None:
            self._classification = \
                self.race_data.class_classification(self.car_class)

        if self.lines is None:
            positions = len(
                [data for data in self._classification \
                    if data[-1] > 0])
        else:
            positions = self.lines
        positions = min(positions, 16)

        classification = sorted(
            [(line[1], line[2], line[3], line[4], line[12]) \
                for line in self._classification \
                if line[4] == self.car_class],
            key=lambda x: -x[-1])[:positions]

        # Check to see if there are ties that got cropped.
        extras = [data for data in \
            [(line[1], line[2], line[3], line[4], line[12]) \
                for line in self._classification \
                if line[12] == classification[-1][-1]]
            if data not in classification]

        # Trim to a max of 16.
        classification = classification + extras
        while len(classification) > 16:
            classification = [data for data in classification \
                if data[-1] != classification[-1][-1]]

        # Resort
        classification = sorted(
            classification,
            key=lambda x: (-x[-1], x[0]))

        for rank, data in enumerate(classification):
            if rank == 0:
                classification[rank] = (rank+1,)+data
            elif classification[rank-1][-1] == data[-1]:
                classification[rank] = (classification[rank-1][0],)+\
                    data
            else:
                classification[rank] = (rank+1,)+data

        return classification

    @property
    def classification_with_headings(self):
        """
        Returns classification with headings added as first
        list element.
        """
        classification = self.classification
        classification.insert(0, tuple(self.column_headings))

        return classification

    @property
    def column_headings(self):
        """
        Returns column headings. Empty columns are headed with "None"
        """
        column_headings = [
            "Rank",
            "Driver",
            "Team",
            "Car",
            "Car Class",
            "Series Points"]

        column_headings = [heading \
            if len(
                [data[i] for data in self.classification \
                    if data[i] is not None]) \
            else None \
            for i, heading in enumerate(column_headings)]

        return column_headings

    def to_frame(self):
        return super(SeriesStandings, self).to_frame()

    def make_mask(self):
        return super(SeriesStandings, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(SeriesStandings, StaticBase))
    print('Instance:', isinstance(SeriesStandings(0), StaticBase))
