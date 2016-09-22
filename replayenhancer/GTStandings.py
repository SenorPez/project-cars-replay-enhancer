"""
Provides classes for the creation of a standings tree.
"""

import abc
from copy import copy

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

    def __init__(self, race_data, *, ups, **kwargs):
        self._race_data = race_data
        self._options = kwargs
        self._flyout = None

        self._last_frame = None

        #  If set, get the telemetry synchronization value.
        try:
            self._sync_racestart = self._options['sync_racestart']
        except KeyError:
            self._sync_racestart = 0.0

        #  If provided, use a font.
        try:
            try:
                self._font = ImageFont.truetype(
                    self._options['font'],
                    self._options['font_size'])
            except OSError:
                self._font = ImageFont.load_default()
        except KeyError:
            self._font = ImageFont.load_default()

        #  If set, use external margins.
        try:
            self._margin = self._options['margin']
        except KeyError:
            self._margin = 2*self._font.getsize("A")[1]

        #  If provided, create short name lookup.
        try:
            self._short_name_lookup = {
                k: v['short_display']
                for k, v in kwargs['participant_config'].items()}
        except KeyError:
            self._short_name_lookup = None

        block_height = self._font.getsize("A")[1]
        self._row_height = int(block_height * 2.5)
        name_width = max(
            [self._font.getsize(driver.name)[0] for driver in self._race_data.current_drivers.values()])
        entries = len(self._race_data.current_drivers)

        self._flyout_width =\
            self._font.getsize("00:00.000")[0] \
            + (self._row_height - block_height)

        self._row_width = \
            name_width \
            + self._row_height \
            + int(self._row_height - block_height)

        material_height = \
            self._row_height * (entries + 1) \
            + (entries + 1) * 1 \
            + self._margin

        material_width = self._margin + self._row_width + self._flyout_width

        self._size = (
            material_width,
            material_height
        )
        self._base_material = Image.new(
            'RGBA',
            self._size,
            (0, 0, 0, 0))

        draw = ImageDraw.Draw(self._base_material)
        draw.line([(0, self._margin + self._row_height), (self._margin + self._row_width - 1, self._margin + self._row_height)], fill='white', width=1)
        draw.line([(0, material_height - 1), (self._margin + self._row_width - 1, material_height - 1)], fill='white', width=1)

        self._timer = Header(self._race_data, self._sync_racestart, (self._row_width, self._row_height), self._font, ups=ups)

        self._standings_lines = list()
        self._classification = sorted(self._race_data.classification, key=lambda x: x.position)
        for entry in self._classification:
            try:
                display_name = self._short_name_lookup[entry.driver_name]
            except KeyError:
                display_name = None
            finally:
                self._standings_lines.append(StandingLine(
                    entry,
                    (self._row_width, self._row_height),
                    self._font,
                    flyout_width=self._flyout_width,
                    display_name=display_name,
                    ups=ups))

    def make_frame(self, time):
        while self._race_data.elapsed_time < time - self._sync_racestart:
            try:
                self._race_data.get_data()
            except StopIteration:
                break

        self._last_frame = self.to_frame()
        return self._last_frame[:, :, :3]

    def make_mask_frame(self, time):
        if self._last_frame is None:
            while self._race_data.elapsed_time < time - self._sync_racestart:
                try:
                    self._race_data.get_data()
                except StopIteration:
                    break
            self._last_frame = self.to_frame()

        return self._last_frame[:, :, -1]/255

    def to_frame(self):
        return PIL_to_npimage(self._make_material().convert('RGBA'))

    def _make_material(self):
        material = self._base_material.copy()

        x_position = self._margin
        y_position = self._margin

        material.paste(self._timer.to_frame(), (x_position, y_position))

        _, material_height = self._size
        y_position = material_height-self._row_height-1

        classification = sorted(self._race_data.classification, key=lambda x: x.position, reverse=True)
        standings_lines = list()

        for entry in classification:
            x_offset = 0
            y_offset = 0
            line = next(line for line in self._standings_lines
                        if line.driver.name == entry.driver_name)

            position_diff = line.position - entry.position
            animation_offset = self._row_height * position_diff \
                               + 1 * position_diff
            if animation_offset != 0:
                line.animations.append(Animation(self._ups, (0, animation_offset)))
                line.position = entry.position

            if entry.laps_complete != line.laps_complete and line.flyout is None:
                block_height = self._font.getsize("A")[1]
                flyout_margin = int((self._row_height - block_height) / 2)
                if entry.position == 1:
                    line.flyout = LapTimeFlyout(
                        self._race_data,
                        entry.driver,
                        self._font,
                        (self._flyout_width, self._row_height),
                        margin=flyout_margin)
                else:
                    line.flyout = GapTimeFlyout(
                        self._race_data,
                        entry.driver,
                        self._font,
                        (self._flyout_width, self._row_height),
                        margin=flyout_margin)

            line.driver = copy(entry.driver)

            for animation in line.animations:
                x_adj, y_adj = animation.offset
                x_offset += x_adj
                y_offset += y_adj

            line_output = line.to_frame()
            material.paste(
                line_output,
                (x_position+x_offset, y_position+y_offset),
                line_output)

            standings_lines.append(line)
            y_position -= self._row_height + 1

        self._standings_lines = standings_lines
        return material


class Header:
    """
    Represents a timer line in the standings display.
    """
    _background_color = (51, 51, 51, 200)
    _background_text_color = (255, 255, 255, 255)

    _ups = 30

    def __init__(self, race_data, time_offset, size, font, *, ups=30):
        self._font = font
        self._race_data = race_data
        self._size = size
        self._time_offset = time_offset

        self._ups = ups

    @property
    def background_color(self):
        return self._background_color

    @property
    def background_text_color(self):
        return self._background_text_color

    @property
    def ups(self):
        return self._ups

    def to_frame(self):
        row_width, row_height = self._size
        block_height = self._font.getsize("A")[1]
        material = Image.new('RGBA', self._size, self.background_color)
        draw = ImageDraw.Draw(material)

        x_position = int((row_height - block_height) / 2)
        y_position = int((row_height - block_height) / 2)

        draw.text(
            (x_position, y_position),
            "Lap {current}/{total}".format(
                current=self._race_data.current_lap,
                total=self._race_data.total_laps),
            fill=self.background_text_color,
            font=self._font)

        return material


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

    def __init__(self, entry, size, font, *, flyout_width=0, display_name=None, ups=30):
        self._ups = ups
        self._display_name = display_name
        self._driver = copy(entry.driver)
        self._laps_complete = entry.driver.laps_complete
        self._position = entry.position
        self._viewed_driver = entry.viewed_driver
        self._size = size
        self._flyout_width = flyout_width
        self._font = font

        self._flyout = None

        self._animations = list()

    @property
    def animations(self):
        self._animations = [animation for animation in self._animations if not animation.complete]
        return self._animations

    @property
    def display_name(self):
        return self._driver.name if self._display_name is None \
            else self._display_name

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value
        self._laps_complete = value.laps_complete

    @property
    def flyout(self):
        return self._flyout

    @flyout.setter
    def flyout(self, value):
        self._flyout = value

    @property
    def laps_complete(self):
        return self._laps_complete

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
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

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

    @property
    def viewed_driver(self):
        return self._viewed_driver

    def to_frame(self):
        row_width, row_height = self._size
        material = Image.new(
            'RGBA',
            (self._size[0]+self._flyout_width, self._size[1]),
            (0, 0, 0, 0))

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

        material.paste(position_material, (0, 0))

        name_material = Image.new(
            'RGBA',
            (row_width - row_height, row_height),
            self.name_color)

        x_position = int((row_height - block_height) / 2)
        y_position = int((row_height - block_height) / 2)

        draw = ImageDraw.Draw(name_material)
        draw.text(
            (x_position, y_position),
            str(self.display_name),
            fill=self.name_text_color,
            font=self._font)

        material.paste(name_material, (row_height, 0))

        if self.flyout is not None:
            x_offset = 0
            y_offset = 0

            for animation in self.flyout.animations:
                x_adj, y_adj = animation.offset
                x_offset += x_adj
                y_offset += y_adj

            flyout = self.flyout.to_frame()
            flyout = flyout.crop((
                0-x_offset,
                0-y_offset,
                flyout.size[0],
                flyout.size[1]))

            material.paste(
                flyout,
                (row_width, 0))

            if all([animation.complete for animation in self.flyout.animations]):
                self._flyout = None

        return material


class Animation:
    """
    Class representing animations for objects.
    """
    def __init__(self, duration, position_from, position_to=(0, 0), delay=0):
        """
        Defines an animation action.

        Parameters
        ----------
        duration = Duration, in frames, of the animation.
        position_from = (x, y) defining the starting position for the
            object.
        position_to = (x, y) defining the ending position for the
            object.
        delay = Duration, in frames, to delay starting the animation.

        Note that the coordinate system in non-standard, to match the
        system used by MoviePy and Pillow. (0, 0) is located at the
        TOP-LEFT of the image.
        """
        self._position_from = position_from
        self._position_to = position_to
        self._ticks_remaining = duration
        self._offset_adjustment = tuple(
            (p_from-p_to)/dur
            for p_from, p_to, dur in zip(
                self._position_from,
                self._position_to,
                (duration, duration)))
        self._delay = delay

    @property
    def complete(self):
        """
        Returns
        -------
        complete = Boolean. True if animation is complete.
        """
        return False if self._ticks_remaining else True

    @property
    def offset(self):
        """
        Returns
        -------
        offset = (x, y) defining the offset, and then updates the offset
            and ticks reminaing.
        Use offset_static to not update.
        """
        if self._delay > 0:
            self._delay -= 1
            return (0, 0)
        else:
            self._ticks_remaining = max(self._ticks_remaining-1, 0)

            if self._ticks_remaining <= 0:
                self._position_from = self._position_to
                self._offset_adjustment = (0, 0)
            else:
                self._position_from = tuple(
                    x-y for x, y in zip(
                        self._position_from,
                        self._offset_adjustment))
                self._position_from = tuple([
                    (y if abs(x-y) <= z else x)
                    for x, y, z in zip(
                        self._position_from,
                        self._position_to,
                        self._offset_adjustment)])
        return_value = tuple([int(x) for x in self._position_from])
        return return_value

    @property
    def offset_static(self):
        """
        Returns
        -------
        offset_static = (x, y) defining the offset. Offset and ticks
            remaining are not updated after this call.
        """
        return tuple([int(x) for x in self._position_from])


class Flyout:
    """
    Abstract class defining flyouts.
    """
    _size = None
    _ups = 30

    def __init__(self, size=None, margin=20, ups=30):
        self._animations = list()
        self._margin = margin
        self._size = size
        self._ups = ups

    @property
    def animations(self):
        return self._animations

    @property
    def ups(self):
        return self._ups

    @abc.abstractmethod
    def _make_material(self):
        """
        Create flyout.
        """


class TimeFlyout(Flyout):
    """
    Abstract class representing a flyout that displays time values.
    """
    _color = (0, 0, 0, 200)

    _session_best_text_color = (255, 0, 255, 255)
    _personal_best_text_color = (0, 255, 0, 255)
    _text_color = (255, 255, 255, 255)
    _invalid_text_color = (255, 0, 0, 255)

    def __init__(self, race_data, driver, size=None, margin=20, ups=30):
        super().__init__(size=size, margin=margin, ups=ups)
        self._driver = driver
        self._race_data = race_data

        self._animations.append(
            Animation(
                duration=int(self.ups/2),
                position_from=(-self._size[0], 0)))
        self._animations.append(
            Animation(
                duration=int(self.ups/2),
                position_from=(0, 0),
                position_to=(-self._size[0], 0),
                delay=self.ups*5))

    @property
    def color(self):
        return self._color

    @property
    def text_color(self):
        #  TODO: Support for invalid lap

        if self._driver.last_lap_time <= self._race_data.best_lap:
            return self._session_best_text_color
        elif self._driver.last_lap_time <= self._driver.best_lap:
            return self._personal_best_text_color
        else:
            return self._text_color

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


class LapTimeFlyout(TimeFlyout):
    """
    Class representing a flyout for the last lap's time.
    """

    def __init__(self, race_data, driver, font, size, *, margin=20, ups=30):
        super().__init__(race_data, driver, size=size, margin=margin, ups=ups)

        self._font = font

    def to_frame(self):
        return self._make_material()

    def _make_material(self):
        material = Image.new('RGBA', self._size, self.color)

        block_height = self._font.getsize("A")[1]
        block_width = self._font.getsize(self.format_time(self._driver.last_lap_time))[0]

        draw = ImageDraw.Draw(material)

        x_position = self._size[0]-self._margin-block_width
        y_position = int((self._size[1]-block_height)/2)

        draw.text(
            (x_position, y_position),
            self.format_time(self._driver.last_lap_time),
            fill=self.text_color,
            font=self._font)

        return material


class GapTimeFlyout(TimeFlyout):
    """
    Class representing a flyout for the gap time to the leader.
    """
    def __init__(self, race_data, driver, font, size, *, margin=20, ups=30):
        super().__init__(race_data, driver, size=size, margin=margin, ups=ups)

        self._font = font

        lap_difference = self._race_data.classification[0].driver.laps_complete \
            - self._driver.laps_complete

        if lap_difference == 0:
            leader_time = sum(self._race_data.classification[0].driver.lap_times)
            driver_time = sum(self._driver.lap_times)
            self._gap = "+{}".format(self.format_time(driver_time-leader_time))
        else:
            self._gap = "+{} lap".format(lap_difference)

    def to_frame(self):
        return self._make_material()

    def _make_material(self):
        material = Image.new('RGBA', self._size, self.color)

        block_height = self._font.getsize("A")[1]
        block_width = self._font.getsize(self._gap)[0]

        draw = ImageDraw.Draw(material)

        x_position = self._size[0]-self._margin-block_width
        y_position = int((self._size[1]-block_height)/2)

        draw.text(
            (x_position, y_position),
            self._gap,
            fill=self.text_color,
            font=self._font)

        return material
