"""
Provides classes for the creation of a standings tree.
"""

import abc
import math
from copy import copy

from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.bindings import PIL_to_npimage


class GTStandings:
    """
    Creates a standings overlay that updates with the following
    columns of information:
        - Position
        - Driver

    There are two 'areas' of information:
        The leader window shows the top x positions (default 16).
        The field windows shows y positions, centered on the subject car
            (default 0).
        If the subject car is in the leader window, the top x + y positions
            are shown.
    """
    _ups = 30

    def __init__(self, race_data, *, ups, **kwargs):
        self._race_data = race_data
        self._options = kwargs
        self._flyout = None

        self._dropping_lines = set()

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
            except (AttributeError, OSError):
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
            name_width = max(
                [
                    self._font.getsize(driver)[0]
                    for driver in self._short_name_lookup.values()])

        except KeyError:
            self._short_name_lookup = None
            name_width = max(
                [
                    self._font.getsize(driver)[0]
                    for driver in race_data.drivers.keys()])

        # If set, use leader window size.
        try:
            self._leader_window_size = kwargs['leader_window_size'] \
                if kwargs['leader_window_size'] >= 0 else 16
        except KeyError:
            self._leader_window_size = 16

        # Plus one to account for timer.
        # TODO: Add setting to make timer optional.
        self._leader_window_size += 1

        # If set, use field window size.
        try:
            self._field_window_size = kwargs['field_window_size'] \
                if kwargs['field_window_size'] >= 0 else 0
        except KeyError:
            self._field_window_size = 0

        block_height = self._font.getsize("A")[1]
        self._row_height = int(block_height * 2.5)
        entries = len(self._race_data.drivers)

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

        material_width = \
            self._margin \
            + self._row_width \
            + self._flyout_width

        self._size = (
            material_width,
            material_height
        )
        self._base_material = Image.new(
            'RGBA',
            self._size,
            (0, 0, 0, 0))

        draw = ImageDraw.Draw(self._base_material)
        draw.line(
            [
                (0, self._margin + self._row_height),
                (
                    self._margin + self._row_width - 1,
                    self._margin + self._row_height)],
            fill='white', width=1)

        self._timer = Header(
            self._race_data,
            self._sync_racestart,
            (self._row_width, self._row_height),
            self._font,
            ups=ups)

        self._standings_lines = list()
        for entry in sorted(self._race_data.classification, key=lambda x: x.position):
            try:
                display_name = \
                    self._short_name_lookup[entry.driver_name]
            except (KeyError, TypeError):
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
        while self._race_data.elapsed_time < time \
                - self._sync_racestart:
            try:
                self._race_data.get_data()
            except StopIteration:
                break

        self._last_frame = self.to_frame()
        return self._last_frame[:, :, :3]

    def make_mask_frame(self, time):
        if self._last_frame is None:
            while self._race_data.elapsed_time < time \
                    - self._sync_racestart:
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
        material.paste(
            self._timer.to_frame(),
            (self._margin, self._margin))

        standings_lines = list()
        classification = self._race_data.classification

        max_y_position = 0

        viewed_y_position = None

        for line in sorted(
                self._standings_lines,
                key=lambda x: (x.position, x in self._dropping_lines),
                reverse=True):
            x_position = self._margin
            y_position = \
                self._margin \
                + self._row_height * line.position \
                + line.position

            x_offset = 0
            y_offset = 0

            try:
                entry = next(
                    entry for entry in classification
                    if entry.driver_name == line.driver.name)
            except StopIteration:
                if line in self._dropping_lines and all([
                        animation.complete
                        for animation in line.animations]):
                    self._dropping_lines.remove(line)
                else:
                    if line not in self._dropping_lines:
                        line.flyout = None
                        line.animations.append(
                            Animation(
                                self._ups,
                                (0, 0),
                                (-line.size[0], 0)))
                        self._dropping_lines.add(line)
                    for animation in line.animations:
                        x_adj, y_adj = animation.offset
                        x_offset += x_adj
                        y_offset += y_adj

                    line_output = line.to_frame()
                    line_output = line_output.crop(
                        (0, 0, line.size[0], line.size[1]))

                    material.paste(
                        line_output,
                        (x_position + x_offset, y_position + y_offset))

                    standings_lines.insert(0, line)
            else:
                position_diff = line.position - entry.position
                animation_offset = \
                    self._row_height * position_diff \
                    + position_diff
                if animation_offset != 0:
                    line.animations.append(
                        Animation(self._ups, (0, animation_offset)))
                    line.position = entry.position
                    y_offset -= animation_offset

                block_height = self._font.getsize("A")[1]
                flyout_margin = int(
                    (self._row_height - block_height) / 2)

                if isinstance(line.flyout, PitStopFlyout):
                    line.flyout.update(
                        self._race_data.driver_world_position(
                            entry.driver.index),
                        self._race_data._next_packet.current_time)
                    if self._race_data.track.at_pit_exit(
                            self._race_data.driver_world_position(
                                entry.driver.index)) \
                            and not line.flyout.is_closing:
                        line.flyout.close_flyout()

                if self._race_data.track.at_pit_entry(
                        self._race_data.driver_world_position(
                            entry.driver.index)) \
                        and not isinstance(line.flyout, PitStopFlyout):
                    line.flyout = PitStopFlyout(
                        self._race_data,
                        entry.driver,
                        self._font,
                        (self._flyout_width, self._row_height),
                        self._race_data.driver_world_position(
                            entry.driver.index),
                        margin=flyout_margin)

                if entry.laps_complete != line.laps_complete \
                        and self._race_data.race_state == 2 \
                        and line.flyout is None:
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
                    (x_position + x_offset, y_position + y_offset))

                standings_lines.insert(0, line)

                max_y_position = max(
                    max_y_position,
                    y_position + y_offset)

            if line.viewed_driver:
                viewed_y_position = y_position + y_offset

        material_width, material_height = material.size
        draw_middle_line = False
        draw_bottom_line = False

        leader_window = None
        field_window = None

        if self._leader_window_size > 0:
            leader_window_bottom = \
                self._row_height * self._leader_window_size \
                + 1 * self._leader_window_size + self._margin
            leader_window = material.crop(
                (0, 0, material_width, leader_window_bottom))
        else:
            leader_window_bottom = 0

        if self._field_window_size > 0:
            lines_below = self._field_window_size // 2
            if self._field_window_size % 2:
                lines_above = self._field_window_size // 2
            else:
                lines_above = (self._field_window_size - 1) // 2

            # Are we at the bottom?
            if material_height \
                    - (self._row_height * (lines_below + 1)
                           + 1 * (lines_below + 1)) < viewed_y_position:
                field_window_top = \
                    material_height \
                    - (
                        self._row_height * self._field_window_size
                        + 1 * self._field_window_size)
                field_window_bottom = material_height
                draw_middle_line = True

            # Are we at the top?
            elif self._row_height * (self._leader_window_size + lines_above) \
                    + 1 * (self._leader_window_size + lines_above) \
                    + self._margin > viewed_y_position:
                field_window_top = leader_window_bottom
                field_window_bottom = \
                    self._row_height * (
                        self._leader_window_size + self._field_window_size) \
                    + 1 * (self._leader_window_size + self._field_window_size) \
                    + self._margin
                draw_middle_line = False

            # Nope, Chuck Testa.
            else:
                field_window_top = \
                    viewed_y_position \
                    - self._row_height * lines_above \
                    - 1 * lines_above
                field_window_bottom = \
                    viewed_y_position \
                    + self._row_height * (lines_below + 1) \
                    + 1 * (lines_below + 1)
                draw_middle_line = True

            field_window = material.crop(
                (0, field_window_top, material_width, field_window_bottom))

        if leader_window is not None and field_window is not None:
            combined_material = Image.new(
                'RGBA',
                (material_width, leader_window.size[1] + field_window.size[1]),
                (0, 0, 0, 0))
            combined_material.paste(leader_window, (0, 0))
            combined_material.paste(
                field_window,
                (0, leader_window.size[1]))
            draw_bottom_line = True
        elif leader_window is not None and field_window is None:
            combined_material = leader_window
            draw_bottom_line = True
        elif leader_window is None and field_window is not None:
            combined_material = field_window
            draw_bottom_line = True
        else:
            combined_material = material

        draw = ImageDraw.Draw(combined_material)

        if draw_middle_line:
            draw.line(
                [
                    (0, leader_window.size[1] - 1),
                    (
                        self._margin + self._row_width - 1,
                        leader_window.size[1] - 1
                    )],
                fill='white',
                width=1)

        if draw_bottom_line:
            draw.line(
                [
                    (0, combined_material.size[1] - 1),
                    (
                        self._margin + self._row_width - 1,
                        combined_material.size[1] - 1
                    )],
                fill='white',
                width=1)

        self._standings_lines = standings_lines
        return combined_material


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

    def __init__(self, entry, size, font, *,
                 flyout_width=0, display_name=None, ups=30):
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
        self._animations = [
            animation for animation in self._animations
            if not animation.complete]
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
    def size(self):
        return self._size

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
            material = material.crop((
                0,
                0,
                self._size[0] + flyout.size[0],
                max(self._size[1], flyout.size[1])))

            if all(
                    [
                        animation.complete for animation
                        in self.flyout.animations
                    ]) \
                    and not self.flyout.persist:
                self._flyout = None
        else:
            material = material.crop((0, 0, self._size[0], self._size[1]))

        return material


class Animation:
    """
    Class representing animations for objects.
    """
    def __init__(self, duration, position_from,
                 position_to=(0, 0), delay=0):
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
            and ticks remaining.
        Use offset_static to not update.
        """
        if self._delay > 0:
            self._delay -= 1
            return 0, 0
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
        self.animations = list()
        self._margin = margin
        self._size = size
        self.ups = ups
        self.persist = False

    @abc.abstractmethod
    def _make_material(self):
        """
        Create flyout.
        """


class TimeFlyout(Flyout):
    """
    Abstract class representing a flyout that displays time values.
    """
    color = (0, 0, 0, 200)

    _session_best_text_color = (255, 0, 255, 255)
    _personal_best_text_color = (0, 255, 0, 255)
    _text_color = (255, 255, 255, 255)
    _invalid_text_color = (255, 0, 0, 255)

    def __init__(self, race_data, driver, size=None, margin=20, ups=30):
        super().__init__(size=size, margin=margin, ups=ups)
        self._driver = driver
        self._race_data = race_data

        self.animations.append(
            Animation(
                duration=int(self.ups/2),
                position_from=(-self._size[0], 0)))
        self.animations.append(
            Animation(
                duration=int(self.ups/2),
                position_from=(0, 0),
                position_to=(-self._size[0], 0),
                delay=self.ups*5))

    @property
    def text_color(self):
        if self._driver.last_lap_invalid:
            return self._invalid_text_color
        elif self._race_data.best_lap is not None \
                and self._driver.last_lap_time is not None \
                and self._driver.last_lap_time <= self._race_data.best_lap:
            return self._session_best_text_color
        elif self._driver.best_lap is not None \
                and self._driver.last_lap_time is not None \
                and self._driver.last_lap_time <= self._driver.best_lap:
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

    @abc.abstractmethod
    def _make_material(self):
        """
        Create flyout.
        """


class LapTimeFlyout(TimeFlyout):
    """
    Class representing a flyout for the last lap's time.
    """

    def __init__(self, race_data, driver, font, size, *,
                 margin=20, ups=30):
        super().__init__(
            race_data,
            driver,
            size=size,
            margin=margin,
            ups=ups)

        self._font = font

    def to_frame(self):
        return self._make_material()

    def _make_material(self):
        material = Image.new('RGBA', self._size, self.color)

        block_height = self._font.getsize("A")[1]
        block_width = self._font.getsize(
            self.format_time(self._driver.last_lap_time))[0]

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
    def __init__(self, race_data, driver, font, size, *,
                 margin=20, ups=30):
        super().__init__(
            race_data,
            driver,
            size=size,
            margin=margin,
            ups=ups)

        self._font = font
        classification = sorted(
            self._race_data.classification,
            key=lambda x: x.position)

        lap_difference = \
            classification[0].driver.laps_complete \
            - self._driver.laps_complete

        if lap_difference == 0:
            leader_time = sum(
                classification[0].driver.lap_times)
            driver_time = sum(
                self._driver.lap_times)

            # If gap time is less than zero (which can happen in the
            # first few laps of a race), we just turn this into a
            # laptime flyout.
            # TODO: There's gotta be a better way.

            if (driver_time-leader_time) > 0:
                self._gap = "+{}".format(
                    self.format_time(driver_time-leader_time))
            else:
                self._gap = "{}".format(
                    self.format_time(self._driver.last_lap_time))
        elif lap_difference == 1:
            self._gap = "+{} lap".format(lap_difference)
        else:
            self._gap = "+{} laps".format(lap_difference)

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


class PitStopFlyout(TimeFlyout):
    """Creates a flyout that appears when a car makes a pit stop.

    Parameters
    ----------
    race_data : RaceData
        RaceData object for the race.
    driver : Driver
        Driver object representing the driver of the line.
    font : PIL.ImageFont
        ImageFont object representing the font used to write text.
    size : (int, int)
        Tuple representing the size of the flyout.
    location : tuple
        The world position of the car. Used for stop detection.
    margin : int, optional
        Margin to use on the left and right of the flyout.
    ups : int, optional
        Updates per second for the flyout.
    """
    _pit_in_color = (255, 0, 0, 255)
    _pit_color = (255, 255, 255, 255)

    def __init__(self, race_data, driver, font, size, location,
                 *, margin=20, ups=30):
        super().__init__(race_data, driver, size=size, margin=margin, ups=ups)

        self._locations = [location]
        self._font = font

        self._stop_time = 0.0
        self._base_time = 0.0
        self._add_time = 0.0
        self._last_time = None

        self.persist = True
        self.is_closing = False

        _ = self.animations.pop()

    def close_flyout(self):
        """Adds an animation to close the flyout.

        """
        self.persist = False
        self.is_closing = True
        self.animations.append(
            Animation(
                duration=int(self.ups / 2),
                position_from=(0, 0),
                position_to=(-self._size[0], 0)))

    def to_frame(self):
        return self._make_material()

    def update(self, location, time=None):
        """Updates flyout data with current position.

        Updates the flyout with the current position (used to determine the pit
        stop status) and time (used to determine the pit stop duration).
        """
        self._locations.append(location)

        if self._is_stopped:
            if time is None or time == -1.0:
                self._base_time = 0.0
                self._add_time = 0.0
                self._last_time = None
            else:
                if self._last_time is None:
                    self._base_time = time
                    self._stop_time = 0.0
                    self._add_time = 0.0
                    self._last_time = time
                elif self._last_time > time:
                    self._add_time += (self._last_time - self._base_time)
                    self._base_time = 0.0
                    self._last_time = time
                else:
                    self._last_time = time

                self._stop_time = (time - self._base_time) + self._add_time

    def _make_material(self):
        material = Image.new('RGBA', self._size, self.color)

        block_height = self._font.getsize("A")[1]

        display_text = "PIT" if self._stop_time <= 0.0 else self.format_time(
            self._stop_time)
        block_width = self._font.getsize(display_text)[0]

        draw = ImageDraw.Draw(material)

        x_position = self._size[0] - self._margin - block_width
        y_position = int((self._size[1] - block_height) / 2)

        draw.text(
            (x_position, y_position),
            display_text,
            fill=self.text_color,
            font=self._font)

        return material

    @property
    def _is_stopped(self):
        """bool : Is the car stopped?

        Notes
        -----
        Determines if the car is stopped. Uses a quarter second of location
        data to determine this, as the accuracy of the location may return
        false positives.
        """
        window_size = math.ceil(self._ups * 0.25)
        if len(self._locations) < window_size:
            return False

        try:
            data = iter(self._locations[-window_size:])
            first = next(data)
            return all(first == rest for rest in data)
        except StopIteration:
            return True

    @property
    def text_color(self):
        """(int, int, int, int) : Color to write text.

        """
        return self._pit_in_color if self._stop_time == 0.0 else self._pit_color
