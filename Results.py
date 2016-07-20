"""
Provides the default Results screen for the Project CARS Replay
Enhancer
"""
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Results(StaticBase):
    """
    Defines a static Results card, consisting of the following columns:

    - Classification (Finish position or DNF)
    - Driver Name
    - Team (if provided)
    - Car
    - Laps Completed
    - Race Time
    - Personal Best Lap Time
    - Personal Best Sector 1 Time
    - Personal Best Sector 2 Time
    - Personal Best Sector 3 Time
    - Points Earned
    """
    _classification = None

    def __init__(self, replay, lines=None):
        self.replay = replay
        self.race_data = self.replay.race_data

        participants = {x for x \
            in self.replay.participant_lookup.values()}
        self.lap_finish = {n:None for n in participants}

        self.material = None
        self.widths = None
        self.data_height = None

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
            self.replay.subheading_text)[1]+self.replay.margin
        y_pos += self.replay.margin/2

        column_positions = [self.replay.margin if i == 0 \
            else self.replay.margin+self.replay.column_margin*i+sum(
                self.widths[0:i]) if self.widths[i-1] != 0 \
                    else self.replay.margin+ \
                        self.replay.column_margin*(i-1)+\
                        sum(self.widths[0:(i-1)])
                            for i, w in enumerate(self.widths)]

        for position, name, team, car, car_class, laps, elapsed_time, \
                best_lap, best_sector_1, best_sector_2, best_sector_3, \
                points \
                in [list(zip(x, column_positions)) \
                for x in classification]:
            draw.text(
                (position[1], y_pos),
                self.format_string(position[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (name[1], y_pos),
                name[0],
                fill=self.replay.font_color,
                font=self.replay.font)
            if team is not None:
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
            if car_class is not None:
                draw.text(
                    (car_class[1], y_pos),
                    self.format_string(car_class[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)
            draw.text(
                (laps[1]+(self.widths[5]-self.replay.font.getsize(
                    self.format_string(laps[0]))[0])/2, y_pos),
                self.format_string(laps[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (elapsed_time[1]+(
                    self.widths[6]-self.replay.font.getsize(
                        self.format_string(
                            elapsed_time[0]))[0])/2, y_pos),
                self.format_string(elapsed_time[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_lap[1]+(self.widths[7]-self.replay.font.getsize(
                    self.format_string(best_lap[0]))[0])/2, y_pos),
                self.format_string(best_lap[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_1[1]+(
                    self.widths[8]-self.replay.font.getsize(
                        self.format_string(
                            best_sector_1[0]))[0])/2, y_pos),
                self.format_string(best_sector_1[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_2[1]+(
                    self.widths[9]-self.replay.font.getsize(
                        self.format_string(
                            best_sector_2[0]))[0])/2, y_pos),
                self.format_string(best_sector_2[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_3[1]+(
                    self.widths[10]-self.replay.font.getsize(
                        self.format_string(
                            best_sector_3[0]))[0])/2, y_pos),
                self.format_string(best_sector_3[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            if points != "":
                draw.text(
                    (points[1]+(
                        self.widths[11]-self.replay.font.getsize(
                            self.format_string(
                                points[0]))[0])/2, y_pos),
                    self.format_string(points[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)
            y_pos += self.data_height+self.replay.margin

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
        self.data_height = max(heights)
        heights = [self.data_height for x in classification]
        heights.append(self.replay.heading_font.getsize(
            self.replay.heading_text)[1])
        heights.append(self.replay.font.getsize(
            self.replay.subheading_text)[1])

        header_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]+\
            self.replay.font.getsize(
                self.replay.subheading_text)[1]+\
                self.replay.margin*2

        text_width = max(
            self.widths[-1]+self.replay.column_margin*(len(
                [x for x in self.widths[:-1] if x != 0])-1),
            self.replay.heading_font.getsize(
                self.replay.heading_text)[0]+\
                self.replay.column_margin+header_height,
            self.replay.font.getsize(
                self.replay.subheading_text)[0]+\
                self.replay.column_margin+header_height)
        text_height = sum(heights)+self.replay.margin*len(heights)-1

        heading_material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, header_height),
            self.replay.heading_color)

        if self.replay.series_logo is not None:
            series_logo = Image.open(
                self.replay.series_logo).resize(
                    (heading_material.height, heading_material.height))
            heading_material.paste(
                series_logo,
                (heading_material.width-series_logo.width, 0))

        self.material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, text_height))
        self.material.paste(heading_material, (0, 0))

        y_pos = header_height
        for i, _ in enumerate(classification):
            if i % 2:
                material_color = (255, 255, 255)
            else:
                material_color = (192, 192, 192)

            row_material = Image.new(
                'RGBA',
                (
                    text_width+self.replay.margin*2,
                    self.data_height+self.replay.margin),
                material_color)
            self.material.paste(row_material, (0, y_pos))
            y_pos += self.data_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

    @property
    def classification(self):
        """
        Returns the classification, trimmed to the number of lines
        specified.
        """
        if self._classification is None:
            self._classification = self.race_data.classification

        if self.lines is None:
            positions = len(self.replay.point_structure)-1
        else:
            positions = self.lines
        positions = min(positions, 16)

        classification = sorted(
            [line[:-1] for line in self._classification \
                if line[0] is not None],
            key=lambda x: x[0])[:positions]

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
            "Pos.",
            "Driver",
            "Team",
            "Car",
            "Car Class",
            "Laps",
            "Time",
            "Best Lap",
            "Best S1",
            "Best S2",
            "Best S3",
            "Points"]

        column_headings = [heading \
            if len(
                [data[i] for data in self.classification \
                    if data[i] is not None]) \
            else None \
            for i, heading in enumerate(column_headings)]

        return column_headings

    def to_frame(self):
        return super(Results, self).to_frame()

    def make_mask(self):
        return super(Results, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Results, StaticBase))
    print('Instance:', isinstance(Results(0), StaticBase))
