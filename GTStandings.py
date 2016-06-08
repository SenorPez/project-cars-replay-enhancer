"""
Provides classes for the creation of a GT Sport style
Standings overlay.
"""
from PIL import Image, ImageDraw

from DynamicBase import DynamicBase
from RaceStandings import ParticipantData

class GTStandings(DynamicBase):
    """
    Creates a standings overlay that constaly updates with the
    following columns of information:
    Position | Driver | Lap / Sector Times | Lap Difference

    Up to 10 drivers are displayed.
    Positions 1-5 are always displayed.
    Postions n-2 through n+2, where n is the viewed car are
        displayed if there is no overlap with P1-5.
    Additional positions are added to display 10.
    """

    _clip_t = 0
    _ups = 30

    @property
    def clip_t(self):
        return self._clip_t

    @clip_t.setter
    def clip_t(self, value):
        self._clip_t = value

    @property
    def ups(self):
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

    def get_mask(self, _):
        """
        Gets the mask. Drops the time argument from the
        caller.
        """
        out = super(GTStandings, self).make_mask()
        out = out[:, :, 0]/255
        return out

    def __init__(self, replay, clip_t=0, ups=30,
                 process_data=True, mask=False):
        self.replay = replay
        self.clip_t = clip_t
        self.ups = ups
        self.process_data = process_data

        self.participant_data = ParticipantData()
        self.standings = None

        telemetry_data = self.replay.telemetry_data[0][0][0]
        participant_data = self.replay.telemetry_data[0][-1]
        self.participant_data.update_drivers(
            telemetry_data,
            participant_data)

        text_width, text_height = \
            self.participant_data.max_name_dimensions(
                self.replay.font)
        self.material = None

        self.standings_lines = list()
        self.mask = mask

        for driver in self.participant_data.drivers_by_position:
            self.standings_lines.append(Standing(
                driver,
                (text_width, text_height),
                self.replay.font,
                self.mask))

    def update(self, force_process=False):
        if self.process_data or force_process:
            if self.clip_t > self.replay.sync_racestart:
                try:
                    telemetry_data, participant_data = \
                        [(x[0], x[-1]) \
                            for x in self.replay.telemetry_data \
                            if x[0][-1][-1] > \
                            self.clip_t-self.replay.sync_racestart][0]
                    telemetry_data = \
                        [x for x in telemetry_data \
                        if x[-1] > \
                            self.clip_t-self.replay.sync_racestart][0]
                except IndexError:
                    telemetry_data, participant_data, index_offset = \
                        [(x[0], x[-1], x[2]) \
                            for x in self.replay.telemetry_data \
                            if x[2] < self.replay.race_finish][-1]
                    telemetry_data = \
                        telemetry_data[self.replay.race_finish-\
                            index_offset]
            else:
                telemetry_data = self.replay.telemetry_data[0][0][0]
                participant_data = self.replay.telemetry_data[0][-1]

            self.participant_data.update_drivers(
                telemetry_data,
                participant_data)

        self.clip_t += float(1/self.ups)

        return self.participant_data.drivers_by_position

    def __standings_filter(self):
        subject_position = self.participant_data.drivers_by_index[0].\
            race_position
        last_place = self.participant_data.last_place

        if subject_position <= 8:
            return self.participant_data.drivers_by_position[:10]
        elif subject_position == last_place \
                or subject_position+1 == last_place:
            return self.participant_data.drivers_by_position[:5] + \
                self.participant_data.drivers_by_position[-5:]
        else:
            #Remember that python is 0-indexed.
            slice_start = subject_position-3
            slice_end = subject_position+2
            return self.participant_data.drivers_by_position[:5] + \
                self.participant_data.drivers_by_position[\
                    slice_start:slice_end]

    def _make_material(self, bg_only):
        if not bg_only:
            self.standings = self.update(force_process=True)

        text_width, text_height = \
            self.participant_data.max_name_dimensions(
                self.replay.font)
        material_width = self.replay.margin+\
            text_height*2+text_width+10*2
        self.material = Image.new(
            'RGBA',
            (
                material_width,
                self.replay.margin+text_height*2*10+1*11))
        y_position = self.replay.margin
        x_position = self.replay.margin
        last_race_position = None

        for driver in self.__standings_filter():
            x_offset = 0
            y_offset = 0
            try:
                standings_line = next(
                    line for line in self.standings_lines \
                    if line.driver.name == driver.name)
            except StopIteration:
                raise

            standings_line_output = standings_line.render(
                driver,
                bg_only)

            for animation in standings_line.animations:
                x_adj, y_adj = animation.offset
                x_offset += x_adj
                y_offset += y_adj

            self.material.paste(
                standings_line_output,
                (x_position+x_offset, y_position+y_offset))

            if last_race_position is None:
                draw = ImageDraw.Draw(self.material)
                draw.line(
                    [
                        (
                            0,
                            self.replay.margin),
                        (
                            material_width,
                            self.replay.margin)],
                    fill='white',
                    width=1)
            elif last_race_position+1 != \
                    standings_line.driver.race_position:
                draw = ImageDraw.Draw(self.material)
                draw.line(
                    [
                        (
                            0,
                            y_position),
                        (
                            material_width,
                            y_position)],
                    fill='white',
                    width=1)

            last_race_position = standings_line.driver.race_position
            y_position += text_height*2+1

        draw = ImageDraw.Draw(self.material)
        draw.line(
            [
                (
                    0,
                    y_position),
                (
                    material_width,
                    y_position)],
            fill='white',
            width=1)

        return self.material if bg_only else self._write_data()

    def _write_data(self):
        #Do nothing. Data writing is handled by the Standing row class.
        return self.material

    def to_frame(self):
        return super(GTStandings, self).to_frame()

    def make_mask(self):
        return super(GTStandings, self).make_mask()

class Standing():
    """
    Represents a single line in the standings display.
    """

    _position_color = (0, 0, 0, 200)
    _name_color = (51, 51, 51, 200)
    _viewed_position_color = (255, 215, 0, 200)
    _viewed_name_color = (255, 215, 0, 200)
    _mask_position_color = (210, 210, 210, 200)
    _mask_name_color = (210, 210, 210, 200)

    _position_text_color = (255, 255, 255)
    _name_text_color = (255, 255, 255)
    _viewed_position_text_color = (0, 0, 0)
    _viewed_name_text_color = (0, 0, 0)

    _ups = 30

    @property
    def position_color(self):
        """
        Gets the material color for the position, based on if it's the
        viewed car or not.
        """
        return self._viewed_position_color if self.driver.viewed \
            else self._mask_position_color if self.mask \
            else self._position_color

    @property
    def position_text_color(self):
        """
        Gets the text color for the position, based on if it's the
        viewed car or not.
        """
        return self._viewed_position_text_color \
            if self.driver.viewed \
            else self._position_text_color

    @property
    def name_color(self):
        """
        Gets the material color for a name, based on if it's the
        viewed car or not.
        """
        return self._viewed_name_color if self.driver.viewed \
            else self._mask_name_color if self.mask \
            else self._name_color

    @property
    def name_text_color(self):
        """
        Gets the text color for a name, based on if it's the
        viewed car or not.
        """
        return self._viewed_name_text_color \
            if self.driver.viewed \
            else self._name_text_color

    @property
    def ups(self):
        """
        Gets the number of updates per second, for animation timing.
        """
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

    def render(self, driver, bg_only, force_same_name=True):
        """
        Determines if data has changed and renders line.
        """
        self.mask = bg_only
        if driver.name != self.driver.name \
                and force_same_name:
            raise ValueError("ValueError: Names do not match.")

        if driver.race_position != self.driver.race_position:
            #Determine the difference.
            position_diff = \
                self.driver.race_position - driver.race_position

            #For each position gained, we need to animate upward
            #one position.
            offset = self.text_height*2*position_diff+1*position_diff
            self.animations.append(
                GTAnimation(
                    (0, offset),
                    self.ups))
        self.driver = driver

        return self._make_material()

    def __init__(self, driver, text_size, font, mask=False, ups=None):
        """
        Creates a new Standings object.
        """
        self.driver = driver
        self.mask = mask

        self.text_width, self.text_height = text_size
        self.font = font
        self.material_width = self.text_height*2+self.text_width+10*2

        self.material = None

        self.animations = list()

        if ups is not None:
            self.ups = ups

    def _make_material(self):
        self.material = Image.new(
            'RGBA',
            (
                self.material_width,
                self.text_height*2))

        position_material = Image.new(
            'RGBA',
            (
                self.text_height*2,
                self.text_height*2),
            self.position_color)
        name_material = Image.new(
            'RGBA',
            (
                self.text_width+10*2,
                self.text_height*2),
            self.name_color)
        self.material.paste(
            position_material,
            (0, 0))
        self.material.paste(
            name_material,
            (self.text_height*2, 0))

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]
        output = self.material.copy()
        draw = ImageDraw.Draw(output)

        position_width = self.font.getsize(
            str(self.driver.race_position))[0]
        x_position = int(
            (self.text_height*2-position_width)/2)
        y_position = int(
            (self.text_height*2-block_height)/2)

        draw.text(
            (x_position, y_position),
            str(self.driver.race_position),
            fill=self.position_text_color,
            font=self.font)

        x_position = self.text_height*2+10
        draw.text(
            (x_position, y_position),
            str(self.driver.name),
            fill=self.name_text_color,
            font=self.font)

        return output

class GTAnimation():
    """
    Class representing animations for objects.
    """
    def __init__(
            self,
            position_offset,
            duration):
        """
        Defines an animation action.
        position_offset = (x, y) defining the position offset for the
            object. Initial setting of this determines the starting
            position of the object.
        ticks = Number of ticks remaining on the animation.

        The object will animate to an offset of (0, 0) over the
        number of ticks initially provided.

        Note that the coordinate system is non-standard, to match
        the system used by MoviePy and Pillow. (0, 0) is located at
        the TOP-LEFT of the image.
        """
        self.position_offset = position_offset
        self.ticks_remaining = duration
        self.offset_adjustment = tuple(x/y for x, y in zip(
            self.position_offset,
            (duration, duration)))

    @property
    def offset(self):
        """
        Returns the offset, and then updates the offset and the ticks
        remaining.
        Use offset_static to not update.
        """
        #return_value = tuple(map(int, self.position_offset))
        return_value = tuple([int(x) for x in self.position_offset])

        self.ticks_remaining -= 1

        if self.ticks_remaining <= 0:
            self.position_offset = (0, 0)
            self.offset_adjustment = (0, 0)
        else:
            self.position_offset = tuple(x-y for x, y in zip(
                self.position_offset,
                self.offset_adjustment))
            self.position_offset = tuple([(
                0 if abs(x) <= y else x) \
                for x, y in zip(
                    self.position_offset,
                    self.offset_adjustment)])

        return return_value

    @property
    def offset_static(self):
        """
        Returns the offset without updating anything.
        """
        #return tuple(map(int, self.position_offset))
        return tuple([int(x) for x in self.position_offset])
