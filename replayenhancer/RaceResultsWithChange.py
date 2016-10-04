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
            starting_position = starting_grid[entry.driver.index].position
            finish_position = entry.position

            position_lookup[finish_position] = starting_position

        try:
            try:
                font = ImageFont.truetype(
                    kwargs['font'],
                    kwargs['font_size'])
            except OSError:
                font = ImageFont.load_default()
            font_color = tuple(kwargs['font_color'])
        except KeyError:
            font = ImageFont.load_default()
            font_color = (0, 0, 0)

        self.add_column(
            'position',
            '',
            formatter=self._make_charm,
            formatter_args={
                'position_lookup': position_lookup,
                'text_height': font.getsize("A")[1]})
        self._columns.insert(1, self._columns.pop())

        # self.add_column(
        #     'position',
        #     '',
        #     formatter=self._position_change,
        #     formatter_args={'position_lookup': position_lookup})
        # self._columns.insert(2, self._columns.pop())

    def _position_change(self, value, **kwargs):
        return "{:+d}".format(kwargs['position_lookup'][value] - value)

    def _make_charm(self, value, **kwargs):
        text_height = kwargs['text_height']
        try:
            change = kwargs['position_lookup'][value] - value
        except KeyError:
            change = 0

        charm = Image.new('RGBA', (text_height, text_height), (0, 0, 0, 0))

        draw = ImageDraw.Draw(charm)
        if change > 0:
            draw.polygon(
                [
                    (0, text_height),
                    (text_height, text_height),
                    (int(text_height/2), 0)],
                fill=(0, 255, 0, 255),
                outline=(0, 255, 0, 255))
        elif change < 0:
            draw.polygon(
                [
                    (0, 0),
                    (text_height, 0),
                    (int(text_height/2), text_height)],
                fill=(255, 0, 0, 255),
                outline=(255, 0, 0, 255))
        else:
            draw.rectangle(
                [
                    (0, int(text_height*.35)),
                    (text_height, int(text_height*.65))],
                fill=(255, 255, 0, 255),
                outline=(255, 255, 0, 255))

        return charm
