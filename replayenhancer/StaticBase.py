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
    """
    _row_colors = [
        (192, 192, 192, 255),
        (255, 255, 255, 255),
    ]

    def __init__(self, data, size=None, **kwargs):
        self._data = data
        self._options = kwargs
        self._columns = list()
        self._size = size

    @property
    def row_colors(self):
        return self._row_colors

    @row_colors.setter
    def row_colors(self, value):
        self._row_colors = value

    def add_column(self, attribute, heading=None, *,
                   align='left', formatter=None, formatter_args=None,
                   colspan=1):
        self._columns.append(DisplayColumn(
            attribute,
            heading,
            align=align,
            formatter=formatter,
            formatter_args=formatter_args,
            colspan=colspan))

    def add_lookup(self, attribute, lookup, default, heading=None, *,
                   align='left', formatter=None, formatter_args=None):
        self._columns.append(DisplayColumn(
            attribute,
            heading,
            lookup,
            default,
            align=align,
            formatter=formatter,
            formatter_args=formatter_args))

    @staticmethod
    def car_class_formatter(value, **kwargs):
        text_height = kwargs['text_height']
        font = kwargs['font']
        charm_width = text_height + font.getsize(value[1])[0] + 2
        charm_height = text_height + 1

        charm = Image.new('RGBA', (charm_width, charm_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(charm)
        draw.polygon(
            [
                (0, text_height),
                (text_height // 3, 0),
                (text_height, 0),
                (text_height - text_height // 3, text_height)],
            fill=tuple(value[0]),
            outline=(0, 0, 0, 255))
        draw.text(
            (text_height + 2, 0),
            str(value[1]),
            fill=kwargs['font_color'],
            font=kwargs['font'])
        return charm

    def sort_data(self, call):
        self._data = sorted(self._data, key=call)

    def to_frame(self):
        return PIL_to_npimage(self._make_material().convert('RGBA'))

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
            except (AttributeError, OSError):
                heading_font = ImageFont.load_default()

            try:
                series_logo = Image.open(self._options['series_logo'])
            except (AttributeError, KeyError, OSError):
                series_logo = None

            heading_text = self._options['heading_text'] \
                if self._options['heading_text'] is not None else ""
            subheading_text = self._options['subheading_text'] \
                if self._options['subheading_text'] is not None else ""
        except KeyError:
            heading_color = None
            heading_font_color = None
            heading_font = None
            heading_text = ""
            subheading_text = ""
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
            except (AttributeError, OSError):
                font = ImageFont.load_default()
            font_color = tuple(self._options['font_color'])
        except KeyError:
            font = ImageFont.load_default()
            font_color = (0, 0, 0)

        #  If set, use external and internal margins.
        try:
            margin = self._options['margin']
        except KeyError:
            margin = 2*font.getsize("A")[1]

        try:
            column_margin = self._options['column_margin']
        except KeyError:
            column_margin = 1*font.getsize("A")[1]

        #  If set, use limit on number of lines to show.
        try:
            starting_grid = \
                self._data[:self._options['result_lines']]
        except KeyError:
            starting_grid = self._data

        #  If set, use a backdrop.
        try:
            backdrop = Image.open(self._options['backdrop'])

            if self._size is not None:
                backdrop = backdrop.resize(self._size)
                backdrop_size = self._size
            else:
                backdrop_size = backdrop.size
        except (AttributeError, KeyError, IOError):
            backdrop = None
            backdrop_size = None

        #  If set, use a logo on the backdrop.
        try:
            logo = Image.open(self._options['logo'])
            logo_size = (
                self._options['logo_width'],
                self._options['logo_height'])
        except (AttributeError, KeyError, IOError):
            logo = None
            logo_size = None

        #  Build main data material.
        column_widths = list()
        display_lines = list()

        if any([column.heading for column in self._columns]):
            line = DisplayLine(self._columns, None, True)
            column_widths = line.column_widths(font, column_widths)
            display_lines.append(line)

        for grid in starting_grid:
            line = DisplayLine(self._columns, grid)
            column_widths = line.column_widths(font, column_widths)
            display_lines.append(line)

        row_height = int(font.getsize("A")[1]*2.5)
        material_width = sum(column_widths)\
            + (len(column_widths)-1)*column_margin
        material_width += 2*margin

        #  Build heading, if applicable.
        heading_height = 0
        heading_material = None
        if heading:
            heading_block_height = sum([
                heading_font.getsize("A")[1],
                font.getsize("A")[1]])
            heading_height = int(heading_block_height*2.5)

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

            x_position = margin
            y_position = int((heading_height-heading_block_height)/2)

            draw.text(
                (x_position, y_position),
                heading_text,
                fill=heading_font_color,
                font=heading_font)
            y_position += heading_font.getsize("A")[1]
            draw.text(
                (margin, y_position),
                subheading_text,
                fill=heading_font_color,
                font=font)

        material_height = sum([
            heading_height,
            row_height*len(starting_grid)])
        if any([column.heading for column in self._columns]):
            material_height += row_height

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

            iline = iter(line)
            for display_text, column_width, align, col_span in iline:
                if isinstance(display_text, str):
                    if align == 'center' \
                            and line.heading_line \
                            and col_span > 1:
                        span = col_span
                        while span > 1:
                            _, next_column_width, _, _ = next(iline)
                            column_width += \
                                next_column_width \
                                + column_margin
                            span -= 1

                    if align == 'center':
                        text_width = font.getsize(display_text)[0]
                        draw_x_position = text_x_position + int(
                            (column_width-text_width)/2)
                    else:
                        draw_x_position = text_x_position
                    draw.text(
                        (draw_x_position, text_y_position),
                        display_text,
                        fill=font_color,
                        font=font)
                else:
                    row_material.paste(
                        display_text,
                        (text_x_position, text_y_position),
                        display_text)

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


class DisplayColumn:
    """
    Defines a single column in the display.
    """
    _point_structure = list()

    def __init__(self, attribute, heading=None, lookup=None,
                 default=None, *, align='left', formatter=None,
                 formatter_args=None, colspan=1):
        self._heading = heading
        self._attribute = attribute
        self._lookup = lookup
        self._default = default
        self._align = align
        self._formatter = formatter
        self._formatter_args = formatter_args
        self._colspan = colspan

    @property
    def align(self):
        return self._align

    @property
    def attribute(self):
        return self._attribute

    @property
    def colspan(self):
        return self._colspan

    @property
    def default(self):
        return self._default

    @property
    def formatter(self):
        return self._formatter

    @property
    def formatter_args(self):
        return self._formatter_args

    @property
    def heading(self):
        return self._heading

    @property
    def lookup(self):
        return self._lookup

    @property
    def point_structure(self):
        return self._point_structure

    @point_structure.setter
    def point_structure(self, value):
        self._point_structure = value


class DisplayLine:
    """
    Defines a single line in the display.
    """
    _column_widths = list()

    def __init__(self, columns, data, make_headings=False):
        self._line_data = list()
        self._col_spans = list()
        self._align = list()
        self._heading_line = make_headings

        for column in columns:
            self._align.append(column.align)
            self._col_spans.append(column.colspan)
            try:
                if make_headings:
                    text_value = str(column.heading)
                else:
                    text_value = column.lookup[
                        getattr(data, column.attribute)]
            except (KeyError, TypeError):
                if column.default is None:
                    text_value = getattr(data, column.attribute)
                else:
                    text_value = column.default

            if column.formatter is None or make_headings:
                self._line_data.append(str(text_value))
            elif column.formatter_args is None:
                self._line_data.append(column.formatter(text_value))
            else:
                self._line_data.append(column.formatter(
                    text_value,
                    **column.formatter_args))

    def __iter__(self):
        line_data = iter(self._line_data)
        column_widths = iter(self._column_widths)
        col_spans = iter(self._col_spans)
        align = iter(self._align)
        while True:
            yield (
                next(line_data),
                next(column_widths),
                next(align),
                next(col_spans))

    @property
    def heading_line(self):
        return self._heading_line

    def column_widths(self, font, column_widths):
        for index, data in enumerate(self._line_data):
            if self._heading_line and self._col_spans[index] > 1:
                self._column_widths.append(0)
            elif isinstance(data, str):
                try:
                    self._column_widths[index] = max(
                        [column_widths[index], font.getsize(data)[0]])
                except IndexError:
                    self._column_widths.append(font.getsize(data)[0])
            else:
                try:
                    self._column_widths[index] = max(
                        [column_widths[index], data.size[0]])
                except IndexError:
                    self._column_widths.append(data.size[0])

        return self._column_widths

    @classmethod
    def reset(cls):
        cls._lookups = list()
        cls._defaults = list()
        cls._column_widths = list()
