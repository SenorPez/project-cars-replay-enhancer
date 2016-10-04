"""
Provides a class for a Series Standings card with position change.
"""
from PIL import Image, ImageDraw, ImageFont

from replayenhancer.DefaultCards import SeriesStandings


class SeriesStandingsWithChange(SeriesStandings):
    """
    Defines a class for a Series Standings card with position change.
    """
    def __init__(self, data, size=None, **kwargs):
        super().__init__(data, size=size, **kwargs)

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

        try:
            point_structure = {
                k: v
                for k, v in enumerate(kwargs['point_structure'])}
        except KeyError:
            point_structure = None

        try:
            points_lookup = {
                k: v['points']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            points_lookup = None

        formatter_args = {'point_structure': point_structure,
                          'points_lookup': points_lookup}

        self._columns.pop()
        self.add_column(
            'calc_points_data',
            'Points',
            formatter=self.calc_series_points,
            formatter_args=formatter_args,
            align='center',
            colspan=2)

        self.add_column(
            'calc_points_data',
            '',
            formatter=self._make_charm,
            formatter_args={
                'font': font,
                'font_color': font_color,
                'text_height': font.getsize("A")[1],
                'point_structure': point_structure,
                'point_lookup': points_lookup})

    def _make_charm(self, value, **kwargs):
        text_height = kwargs['text_height']
        old_rank = self.calc_rank(value, **kwargs)
        new_rank = self.calc_series_rank(value, **kwargs)
        change = int(old_rank) - int(new_rank)

        font = kwargs['font']
        charm_width = text_height \
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
                fill=(0, 0, 0, 255),
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
                fill=(0, 0, 0, 255),
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
                fill=(0, 0, 0, 255),
                font=kwargs['font'])

        return charm

    def calc_rank(self, value, **kwargs):
        driver_name, _, _ = value
        ranks = dict()
        last_points = None
        last_rank = 0
        for entry in self._data:
            if last_points != kwargs['point_lookup'][entry.driver_name]:
                last_points = kwargs['point_lookup'][entry.driver_name]
                last_rank += 1
            ranks[entry.driver_name] = last_rank

        return str(ranks[driver_name])
