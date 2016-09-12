"""
Provides classes for default static cards.
"""

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
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

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
        self.add_lookup('driver_name', name_lookup, 'ERROR', 'Driver')
        self.add_lookup('driver_name', team_lookup, '', 'Team')
        self.add_lookup('driver_name', car_lookup, '', 'Car')
        self.add_column('laps_complete', 'Laps')
        self.add_column(
            'race_time',
            'Time',
            formatter=self.format_time)
        self.add_column(
            'best_lap',
            'Best Lap',
            formatter=self.format_time)
        self.add_column(
            'best_sector_1',
            'Best S1',
            formatter=self.format_time)
        self.add_column(
            'best_sector_2',
            'Best S2',
            formatter=self.format_time)
        self.add_column(
            'best_sector_3',
            'Best S3',
            formatter=self.format_time)
        formatter_args = {'point_structure': point_structure}
        self.add_column(
            'calc_points_data',
            'Points',
            formatter=self.calc_points,
            formatter_args=formatter_args)

    def calc_points(self, value, **kwargs):
        driver_name, position, best_lap = value
        points = 0
        try:
            if best_lap == min(
                    [entry.best_lap for entry in self._data]):
                points += kwargs['point_structure'][0]
            points += kwargs['point_structure'][position]
        except KeyError:
            points += 0
        return str(points)

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
    def __init__(self, data, **kwargs):
        super(RaceResults, self).__init__(data, **kwargs)
        
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
        self.add_lookup(
            'driver_name',
            name_lookup,
            'ERROR',
            'Driver')
        self.add_lookup(
            'driver_name',
            team_lookup,
            '',
            'Team')
        self.add_lookup('driver_name', car_lookup, '', 'Car')
        self.add_column(
            'calc_points_data',
            'Points',
            formatter=self.calc_series_points,
            formatter_args=formatter_args)

    def calc_series_points(self, value, **kwargs):
        driver_name, position, best_lap = value
        try:
            points = kwargs['points_lookup'][driver_name]
        except KeyError:
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
                last_rank += 1
            ranks[entry.driver_name] = last_rank

        return str(ranks[driver_name])
        

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
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

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
        self.add_lookup(
            'driver_name',
            name_lookup,
            'ERROR',
            'Driver')
        self.add_lookup('driver_name', team_lookup, '', 'Team')
        self.add_lookup('driver_name', car_lookup, '', 'Car')
        self.add_lookup(
            'driver_name',
            points_lookup,
            0,
            'Points')
