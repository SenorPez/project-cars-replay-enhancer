"""
Provides a class for a Race Results card with position change.
"""
from PIL import Image, ImageDraw, ImageFont

from replayenhancer.DefaultCards import RaceResults


class RaceResultsWithChange(RaceResults):
    """
    Defines a class for a Race Results card with position change.
    """
    def __init__(self, data, starting_grid, size=None, **kwargs):
        super().__init__(data, size=size, **kwargs)

        position_lookup = dict()
        for entry in data:
            starting_position = next(
                grid.position for grid in starting_grid
                if grid.driver_name == entry.driver_name)
            finish_position = entry.position

            position_lookup[finish_position] = starting_position

        try:
            try:
                font = ImageFont.truetype(
                    kwargs['font'],
                    kwargs['font_size'])
            except (AttributeError, OSError):
                font = ImageFont.load_default()
            font_color = tuple(kwargs['font_color'])
        except KeyError:
            font = ImageFont.load_default()
            font_color = (0, 0, 0)

        self.add_column('position', 'Pos.', colspan=2)
        self._columns.pop(0)
        self._columns.insert(0, self._columns.pop())

        self.add_column(
            'position',
            '',
            formatter=self._make_charm,
            formatter_args={
                'position_lookup': position_lookup,
                'text_height': font.getsize("A")[1],
                'font': font,
                'font_color': font_color})
        self._columns.insert(1, self._columns.pop())

    @staticmethod
    def _make_charm(value, **kwargs):
        text_height = kwargs['text_height']
        change = kwargs['position_lookup'][value] - value

        font = kwargs['font']
        charm_width = \
            text_height \
            + font.getsize(str(abs(change)))[0] \
            + 2
        charm_height = text_height + 1

        charm = Image.new(
            'RGBA',
            (charm_width, charm_height),
            (0, 0, 0, 0))

        draw = ImageDraw.Draw(charm)
        if change > 0:
            draw.polygon(
                [
                    (0, text_height),
                    (text_height, text_height),
                    (int(text_height/2), 0)],
                fill=(0, 255, 0, 255),
                outline=(0, 0, 0, 255))
            draw.text(
                (text_height + 2, 0),
                str(abs(change)),
                fill=kwargs['font_color'],
                font=kwargs['font'])
        elif change < 0:
            draw.polygon(
                [
                    (0, 0),
                    (text_height, 0),
                    (int(text_height/2), text_height)],
                fill=(255, 0, 0, 255),
                outline=(0, 0, 0, 255))
            draw.text(
                (text_height + 2, 0),
                str(abs(change)),
                fill=kwargs['font_color'],
                font=kwargs['font'])
        else:
            draw.rectangle(
                [
                    (0, int(text_height*.45)),
                    (text_height, int(text_height*.75))],
                fill=(255, 255, 0, 255),
                outline=(0, 0, 0, 255))
            draw.text(
                (text_height + 2, 0),
                str(abs(change)),
                fill=kwargs['font_color'],
                font=kwargs['font'])

        return charm
