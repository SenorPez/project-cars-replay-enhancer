"""
Provides classes for default static cards.
"""
from PIL import Image, ImageDraw, ImageFont

from replayenhancer.StaticBase import StaticBase


class RaceResults(StaticBase):
    """
    Defines a class for a default Race Results title card.

    This card, by default, has the following columns:
        - Pos.: Finish position.
        - Driver: Driver name.
        - Team: Driver team (if applicable, blank else).
        - Car: Driver car.
        - Laps: Driver laps completed.
        - Time: Driver total race time.
        - Best Lap: Driver best lap.
        - Best S1: Driver best sector 1.
        - Best S2: Driver best sector 2.
        - Best S3: Driver best sector 3.
        - Points: Driver points earned.
    """
    def __init__(self, data, size=None, **kwargs):
        super().__init__(data, size=size, **kwargs)

        try:
            name_lookup = {
                k: v['display']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            name_lookup = None

        try:
            car_lookup = {
                k: v['car']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            car_lookup = None

        try:
            team_lookup = {
                k: v['team']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            team_lookup = None

        try:
            point_structure = {
                k: v
                for k, v in enumerate(kwargs['point_structure'])}
        except KeyError:
            point_structure = None

        self.add_column('position', 'Pos.')

        if name_lookup is None:
            self.add_column('driver_name', 'Driver')
        else:
            self.add_lookup(
                'driver_name',
                name_lookup,
                'ERROR',
                'Driver')

        if team_lookup is not None:
            self.add_lookup('driver_name', team_lookup, '', 'Team')

        if car_lookup is not None:
            self.add_lookup('driver_name', car_lookup, '', 'Car')

        self.add_column('laps_complete', 'Laps', align='center')
        self.add_column(
            'race_time',
            'Time',
            formatter=self.format_time,
            align='center')
        self.add_column(
            'best_lap',
            'Best Lap',
            formatter=self.format_time,
            align='center')
        self.add_column(
            'best_sector_1',
            'Best S1',
            formatter=self.format_time,
            align='center')
        self.add_column(
            'best_sector_2',
            'Best S2',
            formatter=self.format_time,
            align='center')
        self.add_column(
            'best_sector_3',
            'Best S3',
            formatter=self.format_time,
            align='center')

        if point_structure is not None:
            formatter_args = {'point_structure': point_structure}
            self.add_column(
                'calc_points_data',
                'Points',
                formatter=self.calc_points,
                formatter_args=formatter_args,
                align='center')

    def calc_points(self, value, **kwargs):
        driver_name, position, best_lap = value
        points = 0
        try:
            if best_lap == min(
                    [entry.best_lap for entry in self._data]):
                points += kwargs['point_structure'][0]
            points += kwargs['point_structure'][position]
        except (KeyError, TypeError):
            points += 0
        return str(points)

    @staticmethod
    def format_time(seconds):
        """
        Converts seconds into seconds, minutes:seconds, or
        hours:minutes.seconds as appropriate.
        """
        try:
            minutes, seconds = divmod(float(seconds), 60)
            hours, minutes = divmod(minutes, 60)

            return_value = (int(hours), int(minutes), float(seconds))

            if hours:
                return "{0:d}:{1:0>2d}:{2:0>6.3f}".format(*return_value)
            elif minutes:
                return "{1:d}:{2:0>6.3f}".format(*return_value)
            else:
                return "{2:.3f}".format(*return_value)
        except TypeError:
            return ""


class StartingGrid(StaticBase):
    """
    Defines a class for a default Starting Grid title card.

    This card, by default, has the following columns:
        - Pos.: Starting position.
        - Driver: Driver name.
        - Team: Driver team (if applicable, blank else).
        - Car: Driver car.
        - Points: Driver series points (if applicable, blank else).
    """
    def __init__(self, data, size=None, **kwargs):
        super().__init__(data, size=size, **kwargs)

        try:
            name_lookup = {
                k: v['display']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            name_lookup = None

        try:
            car_lookup = {
                k: v['car']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            car_lookup = None

        try:
            team_lookup = {
                k: v['team']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            team_lookup = None

        try:
            points_lookup = {
                k: v['points']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            points_lookup = None

        self.add_column('position', 'Pos.')

        if name_lookup is None:
            self.add_column('driver_name', 'Driver')
        else:
            self.add_lookup(
                'driver_name',
                name_lookup,
                'ERROR',
                'Driver')

        if team_lookup is not None:
            self.add_lookup('driver_name', team_lookup, '', 'Team')

        if car_lookup is not None:
            self.add_lookup('driver_name', car_lookup, '', 'Car')

        if points_lookup is not None or 'point_structure' in kwargs:
            self.add_lookup(
                'driver_name',
                points_lookup,
                0,
                'Points',
                align='center')


class SeriesStandings(RaceResults):
    """
    Defines a class for a default Series Standings title card.

    This card, by default, has the following columns:
        - Rank: Series rank.
        - Driver: Driver name.
        - Team: Driver team (if applicable, blank else).
        - Car: Driver car.
        - Points: Driver series points.
    """

    def __init__(self, data, size=None, **kwargs):
        super(RaceResults, self).__init__(data, size=size, **kwargs)

        try:
            name_lookup = {
                k: v['display']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            name_lookup = None

        try:
            car_lookup = {
                k: v['car']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            car_lookup = None

        try:
            team_lookup = {
                k: v['team']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            team_lookup = None

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
        self.sort_data(
            lambda x: (
                -int(self.calc_series_points(
                    x.calc_points_data, **formatter_args)),
                x.driver_name))
        self.add_column(
            'calc_points_data',
            'Rank',
            formatter=self.calc_series_rank,
            formatter_args=formatter_args)

        if name_lookup is None:
            self.add_column('driver_name', 'Driver')
        else:
            self.add_lookup(
                'driver_name',
                name_lookup,
                'ERROR',
                'Driver')

        if team_lookup is not None:
            self.add_lookup('driver_name', team_lookup, '', 'Team')

        if car_lookup is not None:
            self.add_lookup('driver_name', car_lookup, '', 'Car')

        self.add_column(
            'calc_points_data',
            'Points',
            formatter=self.calc_series_points,
            formatter_args=formatter_args,
            align='center')

    def calc_series_points(self, value, **kwargs):
        driver_name, position, best_lap = value
        try:
            points = kwargs['points_lookup'][driver_name]
        except (KeyError, TypeError):
            points = 0

        points += int(self.calc_points(value, **kwargs))

        return str(points)

    def calc_series_rank(self, value, **kwargs):
        driver_name, position, best_lap = value
        ranks = dict()
        last_points = None
        last_rank = 0
        for entry in self._data:
            if last_points != int(
                    self.calc_series_points(
                        entry.calc_points_data,
                        **kwargs)):
                last_points = int(
                    self.calc_series_points(
                        entry.calc_points_data,
                        **kwargs))
                last_rank = len(ranks) + 1
            ranks[entry.driver_name] = last_rank

        return str(ranks[driver_name])


class SeriesChampion(SeriesStandings):
    """
    Defines a class for a default Series Champion title card.
    """
    def __init__(self, data, size=None, **kwargs):
        super(RaceResults, self).__init__(data, size=size, **kwargs)

        try:
            self._name_lookup = {
                k: v['display']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            self._name_lookup = {
                entry.driver_name: entry.driver_name
                for entry in self._data}

        try:
            self._car_lookup = {
                k: v['car']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            self._car_lookup = None

        try:
            self._team_lookup = {
                k: v['team']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            self._team_lookup = None

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
        self._formatter_args = formatter_args

        self.sort_data(
            lambda x: (
                -int(self.calc_series_points(
                    x.calc_points_data, **formatter_args)),
                x.driver_name))

    def _make_material(self):
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
        except KeyError:
            heading_color = None
            heading_font_color = (0, 0, 0)
            heading_font = ImageFont.load_default()
            heading_text = None
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

        champion_data = [
            entry for entry in self._data
            if int(self.calc_series_rank(
                entry.calc_points_data,
                **self._formatter_args)) <= 3]

        #  Build main data material
        text_width = 2 * margin
        text_height = 2 * margin
        for rank, entry in enumerate(champion_data, 1):
            if rank == 1:
                width, height = heading_font.getsize("Champion")
                text_width = max([text_width, width + 2 * margin])
                text_height += height

                width, height = heading_font.getsize(
                    self._name_lookup[entry.driver_name])
                text_width = max([text_width, width + 2 * margin])
                text_height += height
            else:
                width, height = font.getsize("Runner Up")
                text_width = max([text_width, width + 2 * margin])
                text_height += height

                width, height = font.getsize(
                    self._name_lookup[entry.driver_name])
                text_width = max([text_width, width + 2 * margin])
                text_height += height

            if self._team_lookup is not None:
                width, height = font.getsize(
                    self._team_lookup[entry.driver_name])
                text_width = max([
                    text_width,
                    width + column_margin + 2 * margin])
                text_height += height

            if self._car_lookup is not None:
                width, height = font.getsize(
                    self._car_lookup[entry.driver_name])
                text_width = max([
                    text_width,
                    width + column_margin + 2 * margin])
                text_height += height

            text_height += margin

        #  TODO: Parametrize the "big logo" width.
        material_width = 300+text_width

        #  Build heading, if applicable.
        heading_height = 0
        heading_material = None
        if heading:
            heading_height = heading_font.getsize(str(heading_text))[1]
            heading_height += 2*margin

            material_width = max([
                (
                    2*margin
                    + heading_font.getsize(str(heading_text))[0]),
                material_width])

            heading_material = Image.new(
                'RGBA',
                (material_width, heading_height),
                heading_color)

            draw = ImageDraw.Draw(heading_material)

            draw.text(
                (margin, margin),
                heading_text,
                fill=heading_font_color,
                font=heading_font)

        material_height = sum([
            heading_height,
            max([300, text_height])
        ])

        #  TODO: Parametrize background color.
        material = Image.new(
            'RGBA',
            (material_width, material_height),
            (255, 255, 255, 255))

        #  Write heading, if applicable.
        if heading:
            material.paste(heading_material, (0, 0), heading_material)

        if series_logo is not None:
            series_logo.thumbnail((300, 300))
            material.paste(series_logo, (0, heading_height))

        y_position = heading_height+int((material_height-text_height)/2)
        x_position = 300+margin

        draw = ImageDraw.Draw(material)

        for rank, entry in enumerate(champion_data, 1):
            if rank == 1:
                draw.text(
                    (x_position, y_position),
                    "Champion",
                    fill=font_color,
                    font=heading_font)
                y_position += heading_font.getsize("A")[1]

                draw.text(
                    (x_position, y_position),
                    self._name_lookup[entry.driver_name],
                    fill=font_color,
                    font=heading_font)
                y_position += heading_font.getsize("A")[1]
                x_position += column_margin
            else:
                draw.text(
                    (x_position, y_position),
                    "Runner Up",
                    fill=font_color,
                    font=font)
                y_position += font.getsize("A")[1]

                draw.text(
                    (x_position, y_position),
                    self._name_lookup[entry.driver_name],
                    fill=font_color,
                    font=font)
                y_position += font.getsize("A")[1]
                x_position += column_margin

            if self._team_lookup is not None:
                draw.text(
                    (x_position, y_position),
                    self._team_lookup[entry.driver_name],
                    fill=font_color,
                    font=font)
                y_position += font.getsize("A")[1]

            if self._car_lookup is not None:
                draw.text(
                    (x_position, y_position),
                    self._car_lookup[entry.driver_name],
                    fill=font_color,
                    font=font)
                y_position += font.getsize("A")[1]

            y_position += margin
            x_position -= column_margin

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
