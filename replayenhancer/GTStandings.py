"""
Provides classes for the creation of a standings tree.
"""

from moviepy.video.io.bindings import PIL_to_npimage
from PIL import Image, ImageDraw, ImageFont


class GTStandings:
    """
    Creates a standings overlay that updates with the following
    columns of information:
        - Position
        - Driver

    Up to 10 drivers are displayed.
        - Positions 1-5 are always displayed.
        - Positions n-2 through n+2, where n is the viewed car are
            displayed if there is no overlap with P1-5.
        - Additional positions are added to display 10 in total.
    """
    _ups = 30

    def __init__(self, data, *, ups, **kwargs):
        self._data = data
        self._options = kwargs

        #  If provided, use a font.
        try:
            try:
                font = ImageFont.truetype(
                    self._options['font'],
                    self._options['font_size'])
            except OSError:
                font = ImageFont.load_default()
        except KeyError:
            font = ImageFont.load_default()

        #  If set, use external and internal margins.
        try:
            self._margin = self._options['margin']
        except KeyError:
            self._margin = 2*font.getsize("A")[1]

        block_height = font.getsize("A")[1]
        self._row_height = 2 * block_height
        name_width = max(
            [font.getsize(driver.driver_name)[0] for driver in data])
        entries = len(data)

        self._row_width = \
            name_width \
            + self._row_height \
            + int(self._row_height - block_height)
        material_height = \
            self._row_height * entries \
            + (entries-1) * 1 \
            + self._margin

        #  TODO: Remove red fill once we're sure everything's okay.
        self._material = Image.new(
            'RGBA',
            (self._row_width + self._margin, material_height),
            color=(255, 0, 0, 255))

        self._standings_lines = list()
        for entry in data:
            self._standings_lines.append(StandingLine(
                entry,
                (self._row_width, self._row_height),
                font,
                ups=ups))

    def to_frame(self):
        return PIL_to_npimage(self._make_material().convert('RGBA'))

    def _make_material(self):
        y_position = self._margin
        for line in self._standings_lines:
            line_output = line.to_frame()
            self._material.paste(
                line_output,
                (self._margin, y_position),
                line_output)
            y_position += self._row_height + 1
        return self._material


class StandingLine:
    """
    Represents a single line entry in the Standings.
    """
    _position_color = (0, 0, 0, 200)
    _name_color = (51, 51, 51, 200)
    _viewed_position_color = (255, 215, 0, 200)
    _viewed_name_color = (255, 215, 0, 200)

    _position_text_color = (255, 255, 255, 255)
    _name_text_color = (255, 255, 255, 255)
    _viewed_position_text_color = (0, 0, 0, 255)
    _viewed_name_text_color = (0, 0, 0, 255)

    _ups = 30

    def __init__(self, entry, size, font, *, ups=30):
        self._ups = ups
        self._driver_name = entry.driver_name
        self._position = entry.position
        self._viewed_driver = entry.viewed_driver
        self._size = size
        self._font = font

    @property
    def name_color(self):
        if self._viewed_driver:
            return self._viewed_name_color
        else:
            return self._name_color

    @property
    def name_text_color(self):
        if self._viewed_driver:
            return self._viewed_name_text_color
        else:
            return self._name_text_color

    @property
    def position_color(self):
        if self._viewed_driver:
            return self._viewed_position_color
        else:
            return self._position_color

    @property
    def position_text_color(self):
        if self._viewed_driver:
            return self._viewed_position_text_color
        else:
            return self._position_text_color

    @property
    def ups(self):
        return self._ups

    def to_frame(self):
        row_width, row_height = self._size
        material = Image.new('RGBA', self._size, (255, 255, 255, 0))

        position_material = Image.new(
            'RGBA',
            (row_height, row_height),
            self.position_color)

        position_width = self._font.getsize(str(self._position))[0]
        block_height = self._font.getsize("A")[1]
        x_position = int((row_height - position_width) / 2)
        y_position = int((row_height - block_height) / 2)

        draw = ImageDraw.Draw(position_material)
        draw.text(
            (x_position, y_position),
            str(self._position),
            fill=self.position_text_color,
            font=self._font)

        material.paste(position_material, (0, 0), position_material)

        name_material = Image.new(
            'RGBA',
            (row_width - row_height, row_height),
            self.name_color)

        x_position = int((row_height - block_height) / 2)
        y_position = int((row_height - block_height) / 2)

        draw = ImageDraw.Draw(name_material)
        draw.text(
            (x_position, y_position),
            str(self._driver_name),
            fill=self.name_text_color,
            font=self._font)

        material.paste(name_material, (row_height, 0), name_material)

        return material
