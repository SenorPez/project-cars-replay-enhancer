"""
Provides a Starting Grid card for the Project CARS Replay Enhancer
"""
from PIL import Image, ImageFont
from PIL import ImageDraw

from replayenhancer.StaticBase import StaticBase


class StartingGrid(StaticBase):
    """
    Defines a static Starting Grid card
    """
    _row_colors = [
        (255, 255, 255, 255),
        (192, 192, 192, 255)]

    def __init__(self, starting_grid, **kwargs):
        self.starting_grid = sorted(starting_grid,
                                    key=lambda x: x.position)
        self.options = kwargs

    @property
    def row_colors(self):
        return self._row_colors

    @row_colors.setter
    def row_colors(self, value):
        self._row_colors = value

    def make_mask(self):
        return super(StartingGrid, self).make_mask()

    def to_frame(self):
        return super(StartingGrid, self).to_frame()

    def _make_material(self, material_only):
        #  If data exists, create a heading.
        try:
            heading_color = tuple(self.options['heading_color'])
            heading_font_color = tuple(
                self.options['heading_font_color'])
            try:
                heading_font = ImageFont.truetype(
                    self.options['heading_font'],
                    self.options['heading_font_size'],
                )
            except OSError:
                heading_font = ImageFont.load_default()
            heading_text = self.options['heading_text']
            subheading_text = self.options['subheading_text']
        except KeyError:
            heading_color = None
            heading_font_color = None
            heading_font = ImageFont.load_default()
            heading_text = None
            subheading_text = None
            heading = False
        else:
            heading = True

        #  If provided, use a font.
        try:
            try:
                font = ImageFont.truetype(
                    self.options['font'],
                    self.options['font_size']
                )
            except OSError:
                font = ImageFont.load_default()
            font_color = tuple(self.options['font_color'])
        except KeyError:
            font = ImageFont.load_default()
            font_color = (0, 0, 0)

        #  If set, use external and internal margins.
        try:
            margin = self.options['margin']
        except KeyError:
            margin = 6*font.getsize("A")[1]

        try:
            column_margin = self.options['column_margin']
        except KeyError:
            column_margin = 3*font.getsize("A")[1]

        #  If set, use limit on number of lines to show.
        try:
            starting_grid = \
                self.starting_grid[:self.options['result_lines']]
        except KeyError:
            starting_grid = self.starting_grid

        #  TODO: Backdrop.
        #  TODO: Name mapping.
        #  TODO: Car data.
        #  TODO: Car class data.
        #  TODO: Team data.
        #  TODO: Points data.

        #  Build main data material.
        column_widths = list()
        for grid in starting_grid:
            try:
                column_widths[0] = max([
                    column_widths[0],
                    font.getsize(str(grid.position))[0]
                ])
            except IndexError:
                column_widths.append(
                    font.getsize(str(grid.position))[0])

            try:
                column_widths[1] = max([
                    column_widths[1],
                    font.getsize(str(grid.driver_name))[0]
                ])
            except IndexError:
                column_widths.append(
                    font.getsize(str(grid.driver_name))[0])

        row_height = font.getsize("A")[1]+margin
        material_width = sum(column_widths)\
            + (len(column_widths)-1)*column_margin
        material_width += 2*margin

        #  Build heading, if applicable.
        heading_height = 0
        heading_material = None
        if heading:
            material_width = max([
                2*margin + heading_font.getsize(str(heading_text))[0],
                2*margin + font.getsize(str(subheading_text))[0],
                material_width
            ])

            heading_height = sum([
                heading_font.getsize(str(heading_text))[1],
                font.getsize(str(subheading_text))[1]
            ])
            heading_height += 2*margin

            heading_material = Image.new('RGBA',
                                         (
                                             material_width,
                                             heading_height),
                                         heading_color)
            draw = ImageDraw.Draw(heading_material)

            draw.text(
                (margin, margin),
                heading_text,
                fill=heading_font_color,
                font=heading_font)
            y_pos = margin+heading_font.getsize(str(heading_text))[1]
            draw.text(
                (margin, y_pos),
                subheading_text,
                fill=heading_font_color,
                font=font)

        material = Image.new(
            'RGBA',
            (
                (material_width,
                 sum([heading_height, row_height*len(starting_grid)]))
            )
        )

        #  Write heading, if applicable.
        if heading:
            material.paste(heading_material, (0, 0))

        y_pos = heading_height
        for i, grid in enumerate(starting_grid):
            row_material = Image.new(
                'RGBA',
                (material_width, row_height),
                self._row_color(i)
            )
            draw = ImageDraw.Draw(row_material)
            #  TODO: Reduce amount of hardcoding.
            x_position = margin
            y_position = (row_height-font.getsize("A")[1])/2
            draw.text(
                (x_position, y_position),
                str(grid.position),
                fill=font_color,
                font=font)
            x_position += column_widths[0]+column_margin
            draw.text(
                (x_position, y_position),
                str(grid.driver_name),
                fill=font_color,
                font=font)
            material.paste(row_material, (0, y_pos))
            y_pos += row_height

        return material

    def _row_color(self, index):
        return self.row_colors[index % len(self.row_colors)]

    @staticmethod
    def _row_width(widths, margin, internal_margin):
        return sum(widths)+2*margin+(len(widths)-1)*internal_margin

    def _write_data(self):
        return Image.new('RGBA', (100, 100))
