"""
Provides base class for static objects. Static objects are those
objects that do not update continuously based on the telemetry
feed.
"""

from PIL import ImageFont, Image, ImageDraw
from moviepy.video.io.bindings import PIL_to_npimage


class StaticBase:
    """
    Defines base class for static objects, including default object
    return methods.

    To get the representation of the static object, `to_frame` is
    called. Execution chain is `to_frame` -> `_make_material` ->
    `_write_data`.

    To get the mask of the static object, `make_mask` is called.
    Execution chain is `make_mask` -> `_make_material`.
    """
    _row_colors = [
        (255, 255, 255, 255),
        (192, 192, 192, 255)]

    def __init__(self, data, **kwargs):
        self._data = data
        self._options = kwargs

    @property
    def row_colors(self):
        return self._row_colors

    @row_colors.setter
    def row_colors(self, value):
        self._row_colors = value

    @staticmethod
    def format_time(seconds):
        """
        Converts seconds into seconds, minutes:seconds, or
        hours:minutes.seconds as appropriate.
        """
        minutes, seconds = divmod(float(seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return_value = (int(hours), int(minutes), float(seconds))

        if hours:
            return "{0:d}:{1:0>2d}:{2:0>6.3f}".format(*return_value)
        elif minutes:
            return "{1:d}:{2:0>6.3f}".format(*return_value)
        else:
            return "{2:.3f}".format(*return_value)

    def to_frame(self):
        return PIL_to_npimage(
            self._make_material().convert('RGBA'))

    def _make_material(self):
        DisplayLine.reset()

        #  If data exists, create a heading.
        try:
            heading_color = tuple(self._options['heading_color'])
            heading_font_color = tuple(
                self._options['heading_font_color'])
            try:
                heading_font = ImageFont.truetype(
                    self._options['heading_font'],
                    self._options['heading_font_size'])
            except OSError:
                heading_font = ImageFont.load_default()

            try:
                series_logo = Image.open(self._options['series_logo'])
            except (KeyError, OSError):
                series_logo = None

            heading_text = self._options['heading_text']
            subheading_text = self._options['subheading_text']
        except KeyError:
            heading_color = None
            heading_font_color = None
            heading_font = None
            heading_text = None
            subheading_text = None
            heading = False
            series_logo = None
        else:
            heading = True

        #  If provided, use a font.
        try:
            try:
                font = ImageFont.truetype(
                    self._options['font'],
                    self._options['font_size'])
            except OSError:
                font = ImageFont.load_default()
            font_color = tuple(self._options['font_color'])
        except KeyError:
            font = ImageFont.load_default()
            font_color = (0, 0, 0)

        #  If set, use external and internal margins.
        try:
            margin = self._options['margin']
        except KeyError:
            margin = 6*font.getsize("A")[1]

        try:
            column_margin = self._options['column_margin']
        except KeyError:
            column_margin = 3*font.getsize("A")[1]

        #  If set, use limit on number of lines to show.
        try:
            starting_grid = \
                self._data[:self._options['result_lines']]
        except KeyError:
            starting_grid = self._data

        #  If set, use a backdrop.
        try:
            backdrop = Image.open(self._options['backdrop'])
            backdrop_size = backdrop.size
        except (KeyError, IOError):
            backdrop = None
            backdrop_size = None

        #  If set, use a logo on the backdrop.
        try:
            logo = Image.open(self._options['logo'])
            logo_size = (
                self._options['logo_width'],
                self._options['logo_height'])
        except (KeyError, IOError):
            logo = None
            logo_size = None

        #  If set, get name mapping.
        try:
            participant_config = self._options['participant_config']
            name_lookup = {
                k: v['display']
                for k, v in participant_config.items()}

            car_lookup = {
                k: v['car']
                for k, v in participant_config.items()}
            team_lookup = {
                k: v['team']
                for k, v in participant_config.items()}
            points_lookup = {
                k: v['points']
                for k, v in participant_config.items()}
        except KeyError:
            DisplayLine.append_lookup(None, None)
        else:
            DisplayLine.append_lookup(name_lookup, None)
            DisplayLine.append_lookup(car_lookup, "")
            DisplayLine.append_lookup(team_lookup, "")
            DisplayLine.append_lookup(points_lookup, 0)

        #  TODO: Multi-class race support.

        #  Build main data material.
        column_widths = list()
        display_lines = list()
        for grid in starting_grid:
            line = DisplayLine(grid.position, grid.driver_name)
            column_widths = line.column_widths(font, column_widths)
            display_lines.append(line)

        row_height = font.getsize("A")[1]+margin
        material_width = sum(column_widths)\
            + (len(column_widths)-1)*column_margin
        material_width += 2*margin

        #  Build heading, if applicable.
        heading_height = 0
        heading_material = None
        if heading:
            heading_height = sum([
                heading_font.getsize(str(heading_text))[1],
                font.getsize(str(subheading_text))[1]])
            heading_height += 2*margin

            series_logo_width = 0
            series_logo_height = 0
            if series_logo is not None:
                series_logo.thumbnail((material_width, heading_height))
                series_logo_width, series_logo_height = series_logo.size

            material_width = max([
                (
                    2*margin
                    + heading_font.getsize(str(heading_text))[0]
                    + series_logo_width),
                (
                    2*margin
                    + font.getsize(str(subheading_text))[0]
                    + series_logo_height),
                material_width])

            heading_material = Image.new(
                'RGBA',
                (material_width, heading_height),
                heading_color)
            if series_logo is not None:
                text_x_position = material_width-series_logo_width
                y_position = 0
                heading_material.paste(
                    series_logo,
                    (text_x_position, y_position))

            draw = ImageDraw.Draw(heading_material)

            draw.text(
                (margin, margin),
                heading_text,
                fill=heading_font_color,
                font=heading_font)
            y_position = margin+heading_font.getsize(
                str(heading_text))[1]
            draw.text(
                (margin, y_position),
                subheading_text,
                fill=heading_font_color,
                font=font)

        material_height = sum([
            heading_height,
            row_height*len(starting_grid)])
        material = Image.new(
            'RGBA',
            (material_width, material_height))

        #  Write heading, if applicable.
        if heading:
            material.paste(heading_material, (0, 0), heading_material)

        y_position = heading_height
        for index, line in enumerate(display_lines):
            row_material = Image.new(
                'RGBA',
                (material_width, row_height),
                self._row_color(index))
            draw = ImageDraw.Draw(row_material)

            text_x_position = margin
            text_y_position = int((row_height-font.getsize("A")[1])/2)

            for display_text, column_width in line:
                draw.text(
                    (text_x_position, text_y_position),
                    display_text,
                    fill=font_color,
                    font=font)
                text_x_position += column_width + column_margin
            material.paste(row_material, (0, y_position), row_material)
            y_position += row_height

        if backdrop is not None:
            backdrop_width, backdrop_height = backdrop_size

            #  Add logo if needed.
            if logo is not None:
                logo = logo.resize(logo_size)
                logo_width, logo_height = logo_size
                text_x_position = backdrop_width-logo_width
                y_position = backdrop_height-logo_height
                backdrop.paste(
                    logo,
                    (text_x_position, y_position),
                    logo)

            if material_width > backdrop_width \
                    or material_height > backdrop_height:
                material.thumbnail(backdrop_size)
                material_width, material_height = material.size

            text_x_position = int((backdrop_width-material_width)/2)
            y_position = int((backdrop_height-material_height)/2)
            backdrop.paste(
                material,
                (text_x_position, y_position),
                material)
            material = backdrop

        return material

    def _row_color(self, index):
        return self._row_colors[index % len(self._row_colors)]

    @staticmethod
    def _row_width(widths, margin, internal_margin):
        return sum(widths) \
               + 2 * margin \
               + (len(widths) - 1) * internal_margin


class DisplayLine:
    """
    Defines a single line in the display.
    """
    _lookups = list()
    _defaults = list()
    _column_widths = list()

    def __init__(self, driver_position, driver_name):
        self._line_data = [str(driver_position)]
        for index in range(len(self._lookups)):
            try:
                text_value = str(self._lookups[index][driver_name])
            except (KeyError, TypeError):
                if self._defaults[index] is None:
                    text_value = str(driver_name)
                else:
                    text_value = str(self._defaults[index])

            self._line_data.append(text_value)

    def __iter__(self):
        line_data = iter(self._line_data)
        column_widths = iter(self._column_widths)
        while True:
            yield (next(line_data), next(column_widths))

    @property
    def defaults(self):
        return self._defaults

    @property
    def lookups(self):
        return self._lookups

    @classmethod
    def append_lookup(cls, lookup, default):
        cls._lookups.append(lookup)
        cls._defaults.append(default)

    def column_widths(self, font, column_widths):
        for index, data in enumerate(self._line_data):
            try:
                self._column_widths[index] = max(
                    [column_widths[index], font.getsize(data)[0]])
            except IndexError:
                self._column_widths.append(font.getsize(data)[0])
        return self._column_widths

    @classmethod
    def reset(cls):
        cls._lookups = list()
        cls._defaults = list()
        cls._column_widths = list()
