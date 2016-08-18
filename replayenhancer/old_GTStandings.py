"""
Provides classes for the creation of a GT Sport style
Standings overlay.
"""
import abc
import math

from PIL import Image, ImageDraw
from moviepy.video.io.bindings import PIL_to_npimage

from DynamicBase import DynamicBase

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

    def __init__(self, replay, clip_t=0, ups=30,
                 process_data=True, mask=False):
        self.replay = replay
        self.clip_t = clip_t
        self.ups = ups
        self.process_data = process_data
        self.mask = mask

        self.material = None

        self.telemetry_data = self.replay.race_data.get_data()

        self.text_width, self.text_height = \
            self.replay.race_data.max_name_dimensions(
                self.replay.font)
        self.short_text_width, self.short_text_height = \
            self.replay.race_data.max_short_name_dimensions(
                self.replay.font)

        self.standings_lines = list()
        for driver in self.telemetry_data.drivers_by_position:
            self.standings_lines.append(Standing(
                self.replay,
                driver,
                (self.short_text_width, self.short_text_height),
                self.replay.font,
                self.mask,
                ups=self.ups))
        self.timer = Timer(
            self.replay,
            (self.short_text_width, self.short_text_height),
            self.replay.font,
            self.mask,
            ups=self.ups)

    def update(self, force_process=False):
        if self.process_data or force_process:
            if self.clip_t > self.replay.sync_racestart:
                self.telemetry_data = self.replay.race_data.get_data(
                    self.clip_t-self.replay.sync_racestart)
            else:
                self.telemetry_data = self.replay.race_data.get_data()

        self.clip_t += float(1/self.ups)

        return self.telemetry_data

    def _make_material(self, bg_only):
        if not bg_only:
            self.telemetry_data = self.update(force_process=True)

        if len(self.replay.car_classes):
            material_width = \
                self.short_text_height*3+self.short_text_width+10*2
        else:
            material_width = \
                self.short_text_height*2+self.short_text_width+10*2

        last_position = self.telemetry_data.last_place
        subject_y = None
        draw_middle_line = False

        base_material = Image.new(
            'RGBA',
            (
                material_width*2,
                self.text_height*2*last_position+\
                    1*(last_position+1)))
        output_material = base_material.copy()
        y_position = (self.telemetry_data.num_participants-1)*\
            self.text_height*2+\
            (self.telemetry_data.num_participants-1)*\
            1
        x_position = 0

        for driver in reversed(self.telemetry_data.drivers_by_position):
            x_offset = 0
            y_offset = 0
            standings_line = next(
                line for line in self.standings_lines \
                if line.driver.name == driver.name)

            #TODO: Clean up masking behavior.
            #Set to False at all times for proper text masking
            #right now.
            standings_line_output = standings_line.render(
                driver,
                False)


            for animation in standings_line.animations:
                x_adj, y_adj = animation.offset
                x_offset += x_adj
                y_offset += y_adj

            if self.replay.viewed is None and \
                    driver.viewed:
                subject_y = y_position+y_offset
            elif self.replay.viewed is not None and \
                    self.replay.viewed == driver.name:
                subject_y = y_position+y_offset

            output_material.paste(
                standings_line_output,
                (x_position+x_offset, y_position+y_offset))

            y_position -= self.text_height*2+1

        top_five = output_material.crop((
            0,
            0,
            material_width*2,
            self.text_height*2*5+1*5))
        if subject_y-(self.text_height*2*2+1*2) <= \
                self.text_height*2*5+1*5:
            window_top = self.text_height*2*5+1*5
            window_bottom = self.text_height*2*10+1*10
            window_five = output_material.crop((
                0,
                window_top,
                material_width*2,
                window_bottom))
            draw_middle_line = False
        elif subject_y+(self.text_height*2*3+1*2) >= \
                self.text_height*2*last_position+1*last_position:
            adjust_y = last_position-5
            window_top = self.text_height*2*adjust_y+\
                1*adjust_y
            window_bottom = self.text_height*2*last_position+\
                1*last_position
            window_five = output_material.crop((
                0,
                window_top,
                material_width*2,
                window_bottom))
            draw_middle_line = True
        else:
            window_top = subject_y-(self.text_height*2*2+1*2)
            window_bottom = subject_y+(self.text_height*2*3+1*2)
            window_five = output_material.crop((
                0,
                window_top,
                material_width*2,
                window_bottom))
            draw_middle_line = True

        self.material = Image.new(
            'RGBA',
            self.replay.size)

        #Composite the timer and the top and bottom standings blocks.
        #TODO: Clean up masking behavior.
        #Set to False at all times for proper text masking right now.
        self.material.paste(
            self.timer.render(self.telemetry_data, False),
            (self.replay.margin, self.replay.margin))
        self.material.paste(
            top_five,
            (
                self.replay.margin,
                self.replay.margin+self.text_height*2*1+1*1))
        self.material.paste(
            window_five,
            (
                self.replay.margin,
                self.replay.margin+self.text_height*2*6+1*6))

        #Draw separator lines as needed.
        draw = ImageDraw.Draw(self.material)
        draw.line(
            [
                (
                    0,
                    self.replay.margin+self.text_height*2),
                (
                    self.replay.margin+material_width+1,
                    self.replay.margin+self.text_height*2)],
            fill='white',
            width=1)

        draw = ImageDraw.Draw(self.material)
        draw.line(
            [
                (
                    0,
                    self.replay.margin+self.text_height*2*11+1*10),
                (
                    self.replay.margin+material_width+1,
                    self.replay.margin+self.text_height*2*11+1*10)],
            fill='white',
            width=1)

        if draw_middle_line:
            draw = ImageDraw.Draw(self.material)
            draw.line(
                [
                    (
                        0,
                        self.replay.margin+self.text_height*2*6+1*5),
                    (
                        self.replay.margin+material_width+1,
                        self.replay.margin+self.text_height*2*6+1*5)],
                fill='white',
                width=1)

        #TODO: Clean up masking behavior.
        #Set to False at all times for proper text masking right now.
        #return self.material if bg_only else self._write_data()
        return self._write_data()

    def _write_data(self):
        #Do nothing. Data writing is handled by the Standing row class.
        return self.material

    def to_frame(self):
        return super(GTStandings, self).to_frame()

    def make_mask(self):
        """
        Returns mask.
        """
        out = self._make_material(True)
        out = out.split()[-1].convert('RGB')
        out = PIL_to_npimage(out)
        out = out[:, :, 0]/255
        return out

class Timer():
    """
    Represents a timer line in the standings display.
    """

    _background_color = (51, 51, 51, 200)
    _mask_background_color = (210, 210, 210, 200)

    _background_text_color = (255, 255, 255, 255)

    _ups = 30

    @property
    def background_color(self):
        """
        Gets the material color for the line.
        """
        return self._background_color

    @property
    def background_text_color(self):
        """
        Gets the text color for the line.
        """
        return self._background_text_color

    @property
    def ups(self):
        """
        Gets the number of updates per second, for animation timing.
        """
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

    def render(self, telemetry_data, bg_only):
        """
        Renders the line.
        """
        self.mask = bg_only
        self.telemetry_data = telemetry_data

        return self._make_material()

    def __init__(self, replay, text_size, font,
                 mask=False, ups=None):
        """
        Creates a new Timer object.
        """
        self.replay = replay
        self.race_data = self.replay.race_data
        self.telemetry_data = self.race_data.packet
        self.mask = mask

        self.text_width, self.text_height = text_size
        self.font = font
        if len(self.replay.car_classes):
            self.material_width = \
                self.text_height*3+self.text_width+10*2+2
        else:
            self.material_width = \
                self.text_height*2+self.text_width+10*2+2
        self.material = None

        if ups is not None:
            self.ups = ups

    def _make_material(self):
        self.material = Image.new(
            'RGBA',
            (
                self.material_width,
                self.text_height*2),
            self.background_color)

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]
        output = self.material.copy()
        draw = ImageDraw.Draw(output)

        y_position = int(
            (self.text_height*2-block_height)/2)

        if self.replay.viewed is None:
            for driver in self.telemetry_data.drivers_by_index:
                if driver.viewed:
                    break

            lap_display_width, _ = self.font.getsize(
                "Lap {total}/{total}".format(
                    total=self.telemetry_data.event_duration))

            current_time = 0 if self.telemetry_data.current_time == -1 \
                else self.telemetry_data.current_time
            draw.text(
                (10, y_position),
                "{time}".format(
                    time=self.format_time(current_time)),
                fill=self.background_text_color,
                font=self.font)
            draw.text(
                (self.material_width-10-lap_display_width, y_position),
                "Lap {current}/{total}".format(
                    current=str(self.telemetry_data.leader_lap),
                    total=str(self.telemetry_data.event_duration)),
                fill=self.background_text_color,
                font=self.font)
        else:
            draw.text(
                (10, y_position),
                "Lap {current}/{total}".format(
                    current=str(self.telemetry_data.leader_lap),
                    total=str(self.telemetry_data.event_duration)),
                fill=self.background_text_color,
                font=self.font)

        return output

    @staticmethod
    def format_time(seconds):
        """
        Converts seconds into seconds, minutes:seconds, or
        hours:minutes:seconds as appropriate
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

    _position_text_color = (255, 255, 255, 255)
    _name_text_color = (255, 255, 255, 255)
    _viewed_position_text_color = (0, 0, 0, 255)
    _viewed_name_text_color = (0, 0, 0, 255)

    _ups = 30

    @property
    def position_color(self):
        """
        Gets the material color for the position, based on if it's the
        viewed car or not.
        """
        viewed = False
        if self.replay.viewed is not None and \
                self.replay.viewed == self.driver.name:
            viewed = True
        elif self.replay.viewed is None and \
                self.driver.viewed:
            viewed = True

        return self._viewed_position_color if viewed \
            else self._mask_position_color if self.mask \
            else self._position_color

    @property
    def position_text_color(self):
        """
        Gets the text color for the position, based on if it's the
        viewed car or not.
        """
        viewed = False
        if self.replay.viewed is not None and \
                self.replay.viewed == self.driver.name:
            viewed = True
        elif self.replay.viewed is None and \
                self.driver.viewed:
            viewed = True

        return self._viewed_position_text_color \
            if viewed \
            else self._position_text_color

    @property
    def name_color(self):
        """
        Gets the material color for a name, based on if it's the
        viewed car or not.
        """
        viewed = False
        if self.replay.viewed is not None and \
                self.replay.viewed == self.driver.name:
            viewed = True
        elif self.replay.viewed is None and \
                self.driver.viewed:
            viewed = True

        return self._viewed_name_color if viewed \
            else self._mask_name_color if self.mask \
            else self._name_color

    @property
    def name_text_color(self):
        """
        Gets the text color for a name, based on if it's the
        viewed car or not.
        """
        viewed = False
        if self.replay.viewed is not None and \
                self.replay.viewed == self.driver.name:
            viewed = True
        elif self.replay.viewed is None and \
                self.driver.viewed:
            viewed = True

        return self._viewed_name_text_color \
            if viewed \
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

    def render(self, driver, bg_only):
        """
        Determines if data has changed and renders line.
        """
        self.mask = bg_only

        #TODO: This is ugly as hell. Clean it up.
        """
        if driver.race_position == self.driver.race_position and \
                driver.current_lap == self.driver.current_lap and \
                self.material is not None and (
                        self.flyout is None or \
                    not any([any(animation.offset_static) \
                        for animation \
                        in self.flyout.animations])) and (
                            self.flyout is None or (
                                self.flyout.session_best and \
                                self.flyout.lap_time == \
                                    self.flyout.race_data.\
                                        best_lap_time()) or (
                                            not self.flyout.\
                                                session_best and \
                        self.flyout.lap_time != \
                            self.flyout.race_data.best_lap_time())):
            if self.mask:
                #If there's a flyout but it's static, it's delayed.
                #Grab the offset to advance the delay.
                if self.flyout is not None and \
                        not any([any(animation.offset_static) \
                            for animation \
                            in self.flyout.animations]):
                    _ = [animation.offset for animation \
                        in self.flyout.animations]
                return self.material
            else:
                #If there's a flyout but it's static, it's delayed.
                #Grab the offset to advance the delay.
                if self.flyout is not None and \
                        not any([any(animation.offset_static) \
                            for animation \
                            in self.flyout.animations]):
                    _ = [animation.offset for animation \
                        in self.flyout.animations]

                return self.material_with_data
        """

        if driver.race_position != self.driver.race_position:
            #Determine the difference.
            position_diff = \
                self.driver.race_position - driver.race_position

            #For each position gained, we need to animate upward
            #one position.
            offset = self.text_height*2*position_diff+1*position_diff
            self.animations.append(
                GTAnimation(
                    self.ups,
                    (0, offset)))

        if self.flyout is not None and \
                not self.flyout.persist and \
                all([x.complete for x in self.flyout.animations]):
            self.flyout = None

        if isinstance(self.flyout, PitStopFlyout):
            self.flyout.update(
                driver.world_position,
                self.replay.race_data.packet.current_time)
            if self.replay.track.at_pit_exit(driver.world_position):
                self.flyout.close_flyout()

        if self.replay.track.at_pit_entry(driver.world_position) and \
                not isinstance(self.flyout, PitStopFlyout):
            self.flyout = PitStopFlyout(
                driver.world_position,
                self.font,
                size=(
                    self.font.getsize("99:99:999")[0]+10*2,
                    self.text_height*2),
                ups=self.ups,
                persist=True)

        if driver.current_lap != self.driver.current_lap and \
                self.flyout is None:
            if driver.race_position == 1:
                self.flyout = LapTimeFlyout(
                    self.race_data,
                    self.driver,
                    self.font,
                    size=(
                        self.font.getsize("99:99:999")[0]+10*2,
                        self.text_height*2),
                    ups=self.ups)
            else:
                self.flyout = GapTimeFlyout(
                    self.race_data,
                    self.driver,
                    self.font,
                    size=(
                        self.font.getsize("99:99:999")[0]+10*2,
                        self.text_height*2),
                    ups=self.ups)

        self.driver = driver

        return self._make_material()

    def __init__(self, replay, driver, text_size,
                 font, mask=False, ups=None):
        """
        Creates a new Standings object.
        """
        self.replay = replay
        self.race_data = self.replay.race_data
        self.driver = driver
        self.name = self.replay.short_name_display[self.race_data.driver_lookup[driver.name]]
        self.mask = mask

        self.text_width, self.text_height = text_size
        self.font = font
        if len(self.replay.car_classes):
            self.material_width = \
                self.text_height*3+self.text_width+10*2
        else:
            self.material_width = \
                self.text_height*2+self.text_width+10*2

        self.material = None
        self.material_with_data = None
        self.flyout = None

        self.animations = list()

        if ups is not None:
            self.ups = ups

    def _attach_flyout(self):
        x_offset = 0
        y_offset = 0

        for animation in self.flyout.animations:
            x_adj, y_adj = animation.offset
            x_offset += x_adj
            y_offset += y_adj

        flyout = self.flyout.render(self.mask)
        flyout = flyout.crop((
            0-x_offset,
            0-y_offset,
            flyout.size[0],
            flyout.size[1]))

        self.material.paste(
            flyout,
            (
                self.material_width+2,
                0))
        self.material = self.material.crop((
            0,
            0,
            self.material_width+2+flyout.size[0],
            max(
                self.text_height*2,
                self.flyout.size[1])))
        return self.material

    def _make_material(self):
        if self.flyout is not None:
            self.material = Image.new(
                'RGBA',
                (
                    self.material_width+self.flyout.size[0],
                    max(
                        self.text_height*2,
                        self.flyout.size[1])),
                color=(255, 0, 0, 255))
            self.material = self._attach_flyout()
        else:
            self.material = Image.new(
                'RGBA',
                (
                    self.material_width+2,
                    self.text_height*2),
                color=(255, 0, 0, 255))

        draw = ImageDraw.Draw(self.material)
        draw.rectangle(
            (
                0,
                0,
                self.text_height*2+1,
                self.text_height*2+1),
            fill=self.position_color)

        if len(self.replay.car_classes):
            width = self.text_height*3+self.text_width+10*2+1
        else:
            width = self.text_height*2+self.text_width+10*2+1

        draw.rectangle(
            (
                self.text_height*2,
                0,
                width,
                self.text_height*2+1),
            fill=self.name_color)

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]
        self.material_with_data = self.material.copy()
        draw = ImageDraw.Draw(self.material_with_data)

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

        try:
            color = [data['color'] \
                for data in self.replay.car_classes.values() \
                if self.replay.car_data[self.driver.name] \
                in data['cars']][0]
            x_divisions = int(self.text_height/3)

            draw.polygon(
                [
                    (x_position, y_position+self.text_height),
                    (x_position+x_divisions, y_position),
                    (x_position+x_divisions*3, y_position),
                    (
                        x_position+x_divisions*2,
                        y_position+self.text_height
                    )
                ],
                outline=(0, 0, 0),
                fill=tuple(color))
            x_position += self.text_height
        except IndexError:
            if len(self.replay.car_classes):
                x_position += self.text_height

        draw.text(
            (x_position, y_position),
            str(self.name),
            fill=self.name_text_color,
            font=self.font)

        return self.material_with_data

class Flyout():
    """
    Class representing standings flyouts.
    """
    _ups = 30

    @abc.abstractmethod
    def _make_material(self):
        """Create material used as a canvas."""

    @abc.abstractmethod
    def _write_data(self):
        """Write data to the material."""

    @property
    def ups(self):
        """
        Gets the number of updates per second, for animation timing.
        """
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

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

class LapTimeFlyout(Flyout):
    """
    Class representing a flyout for the last lap's time.
    """
    _color = (0, 0, 0, 200)
    _mask_color = (210, 210, 210, 200)

    _session_best_text_color = (255, 0, 255, 255)
    _personal_best_text_color = (0, 255, 0, 255)
    _text_color = (255, 255, 255, 255)
    _invalid_text_color = (255, 0, 0, 255)

    _ups = 30

    @property
    def color(self):
        """
        Gets the material color for the line.
        """
        return self._mask_color if self.mask \
            else self._color

    @property
    def text_color(self):
        """
        Gets the text color for the line.
        """
        if self.driver.current_lap in \
                self.race_data.invalid_laps[self.driver.index]:
            self.session_best = False
            return self._invalid_text_color
        elif self.lap_time == self.race_data.best_lap_time():
            self.session_best = True
            return self._session_best_text_color
        elif self.lap_time == self.race_data.best_lap_time(
                self.driver.index):
            self.session_best = False
            return self._personal_best_text_color
        else:
            self.session_best = False
            return self._text_color

    def __init__(self, race_data, driver,
                 font, mask=False, ups=None, size=None):
        self.race_data = race_data
        self.driver = driver
        self.lap_time = self.race_data.lap_time(
            self.driver.index,
            self.driver.current_lap)
        self.font = font
        self.mask = mask
        self.persist = False

        if size is None:
            width, _ = self.font.getsize("99:99:999")
            _, height = self.font.getsize("Srp")
            self.size = (width+10*2, height*2)
        else:
            self.size = size

        if ups is not None:
            self.ups = ups

        self.animations = list()
        self.animations.append(
            GTAnimation(
                duration=int(ups/2),
                position_from=(-self.size[0], 0)))
        self.animations.append(
            GTAnimation(
                duration=int(ups/2),
                position_from=(0, 0),
                position_to=(-self.size[0], 0),
                delay=ups*5))
        self.material = None
        self.material_with_data = None
        self.session_best = False

    def render(self, bg_only):
        """
        Determines if the flyout needs to be updated, and returns a
        rendering.
        """
        self.mask = bg_only

        if self.material is None:
            return self._make_material()
        elif self.session_best and \
                not self.mask and \
                self.lap_time != self.race_data.best_lap_time():
            return self._make_material()
        elif self.mask:
            return self.material
        else:
            return self.material_with_data

    def _make_material(self):
        self.material = Image.new(
            'RGBA',
            self.size,
            self.color)

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]
        block_width = self.font.getsize(self.format_time(
            self.lap_time))[0]
        self.material_with_data = self.material.copy()
        draw = ImageDraw.Draw(self.material_with_data)

        x_position = self.size[0]-10-block_width
        y_position = int(
            (self.size[1]-block_height)/2)

        draw.text(
            (x_position, y_position),
            self.format_time(self.lap_time),
            fill=self.text_color,
            font=self.font)

        return self.material_with_data

class GapTimeFlyout(Flyout):
    """
    Class representing a flyout for the gap time.
    """
    _color = (0, 0, 0, 200)
    _mask_color = (210, 210, 210, 200)

    _session_best_text_color = (255, 0, 255, 255)
    _personal_best_text_color = (0, 255, 0, 255)
    _text_color = (255, 255, 255, 255)
    _invalid_text_color = (255, 0, 0, 255)

    _ups = 30

    @property
    def color(self):
        """
        Gets the material color for the line.
        """
        return self._mask_color if self.mask \
            else self._color

    @property
    def text_color(self):
        """
        Gets the text color for the line.
        """
        if self.driver.current_lap in \
                self.race_data.invalid_laps[self.driver.index]:
            self.session_best = False
            return self._invalid_text_color
        elif self.lap_time == self.race_data.best_lap_time():
            self.session_best = True
            return self._session_best_text_color
        elif self.lap_time == self.race_data.best_lap_time(
                self.driver.index):
            self.session_best = False
            return self._personal_best_text_color
        else:
            self.session_best = False
            return self._text_color

    def __init__(self, race_data, driver,
                 font, mask=False, ups=None, size=None):
        self.race_data = race_data
        self.driver = driver
        self.persist = False

        self.lap_time = self.race_data.lap_time(
            self.driver.index,
            self.driver.current_lap)

        if len(self.race_data.lap_time(
                self.race_data.leader_index)) != len(
                    self.race_data.lap_time(
                        driver.index)):
            self.gap = int(len(self.race_data.lap_time(
                self.race_data.leader_index))-\
                len(self.race_data.lap_time(
                    driver.index)))
        else:
            self.gap = float(
                sum(
                    self.race_data.lap_time(
                        driver.index))-sum(
                            self.race_data.lap_time(
                                self.race_data.leader_index)))

        self.font = font
        self.mask = mask

        if size is None:
            width, _ = self.font.getsize("99:99:999")
            _, height = self.font.getsize("Srp")
            self.size = (width+10*2, height*2)
        else:
            self.size = size

        self.animations = list()
        self.animations.append(
            GTAnimation(
                duration=int(ups/2),
                position_from=(-self.size[0], 0)))
        self.animations.append(
            GTAnimation(
                duration=int(ups/2),
                position_from=(0, 0),
                position_to=(-self.size[0], 0),
                delay=ups*5))
        self.material = None
        self.material_with_data = None
        self.session_best = False

        if ups is not None:
            self.ups = ups

    def render(self, bg_only):
        """
        Determines if the flyout needs to be updated, and returns a
        rendering.
        """
        self.mask = bg_only

        if self.material is None:
            return self._make_material()
        elif self.session_best and \
                not self.mask and \
                self.lap_time != self.race_data.best_lap_time():
            return self._make_material()
        elif self.mask:
            return self.material
        else:
            return self.material_with_data

    def _make_material(self):
        self.material = Image.new(
            'RGBA',
            self.size,
            self.color)

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]

        if isinstance(self.gap, int) and self.gap == 1:
            gap = "+"+str(self.gap)+" lap"
        elif isinstance(self.gap, int):
            gap = "+"+str(self.gap)+" laps"
        else:
            gap = "+"+self.format_time(self.gap)

        block_width = self.font.getsize(gap)[0]

        self.material_with_data = self.material.copy()
        draw = ImageDraw.Draw(self.material_with_data)

        x_position = self.size[0]-10-block_width
        y_position = int(
            (self.size[1]-block_height)/2)

        draw.text(
            (x_position, y_position),
            gap,
            fill=self.text_color,
            font=self.font)

        return self.material_with_data

class PitStopFlyout(Flyout):
    """
    Class representing a flyout for pit stop.
    """
    _color = (0, 0, 0, 200)
    _mask_color = (210, 210, 210, 200)

    _pit_in_color = (255, 0, 0, 255)
    _pit_color = (255, 255, 255, 255)

    _ups = 30

    """
    @property
    def old_location(self):
        return self._locations[0]

    @property
    def location(self):
        return self._locations[1]

    @property
    def new_location(self):
        return self._locations[2]
    """

    @property
    def stopped(self):
        """
        Returns if a car is stopped. Uses a quarter second of
        locations to determine, as the accuracy of the location
        may return false positives.
        """
        window_size = math.ceil(self.ups*0.25)
        if len(self._locations) < window_size:
            return False

        try:
            data = iter(
                self._locations[-window_size:])
            first = next(data)
            return all(first == rest for rest in data)
        except StopIteration:
            return True

    def update(self, location, time=None):
        """
        Updates the flyout with the current position (used to
        determine the pit stop status) and time (used to
        determine the pit stop duration).
        """
        self._locations.append(location)
        if self.stopped:
            if time is None or time == -1.0:
                self.base_time = 0.0
                self.add_time = 0.0
                self.last_time = None
            else:
                if self.last_time is None:
                    self.base_time = time
                    self.stop_time = 0.0
                    self.add_time = 0.0
                    self.last_time = time
                elif self.last_time > time:
                    self.add_time += (self.last_time-self.base_time)
                    self.base_time = 0.0
                    self.last_time = time
                else:
                    self.last_time = time
                self.stop_time = (time-self.base_time) + \
                    self.add_time

    @property
    def color(self):
        """
        Gets the material color for the flyout.
        """
        return self._mask_color if self.mask \
            else self._color

    @property
    def text_color(self):
        """
        Gets the text color for the line.
        """
        return self._pit_in_color if self.stop_time == 0.0 \
            else self._pit_color

    def __init__(self, loc, font, mask=False, ups=None, size=None,
                 persist=False):
        self._locations = [loc]

        self.font = font
        self.mask = mask

        self.stop_time = 0.0
        self.base_time = 0.0
        self.add_time = 0.0
        self.last_time = None

        if size is None:
            width, _ = self.font.getsize("99:99:999")
            _, height = self.font.getsize("Srp")
            self.size = (width+10*2, height*2)
        else:
            self.size = size

        self.animations = list()
        self.animations.append(
            GTAnimation(
                duration=int(ups/2),
                position_from=(-self.size[0], 0)))

        self.material = None
        self.material_with_data = None

        if ups is not None:
            self.ups = ups

        self.persist = persist

    def close_flyout(self):
        """
        Adds an animation to close the flyout.
        """
        self.persist = False
        self.animations.append(
            GTAnimation(
                duration=int(self.ups/2),
                position_from=(0, 0),
                position_to=(-self.size[0], 0)))

    def render(self, bg_only):
        """
        Determines if the flyout needs to be updated, and returns a
        rendering.
        """
        self.mask = bg_only

        """
        if self.material is None:
            return self._make_material()
        elif self.new_location == self.location and \
                all([self._locations]) and \
                self.location != self.old_location:
            return self._make_material()
        elif self.old_location == self.location and \
                all([self._locations]) and \
                self.location != self.new_location:
            self.stop_time = 0.0
            return self._make_material()
        elif self.mask:
            return self.material
        else:
            return self.material_with_data
        """
        return self._make_material()

    def _make_material(self):
        self.material = Image.new(
            'RGBA',
            self.size,
            self.color)

        return self.material if self.mask else self._write_data()

    def _write_data(self):
        block_height = self.font.getsize("A")[1]

        display_text = "PIT" if self.stop_time == 0.0 \
            else self.format_time(self.stop_time)
        block_width = self.font.getsize(display_text)[0]

        self.material_with_data = self.material.copy()
        draw = ImageDraw.Draw(self.material_with_data)

        x_position = self.size[0]-10-block_width
        y_position = int(
            (self.size[1]-block_height)/2)

        draw.text(
            (x_position, y_position),
            display_text,
            fill=self.text_color,
            font=self.font)

        return self.material_with_data

class GTAnimation():
    """
    Class representing animations for objects.
    """
    def __init__(
            self,
            duration,
            position_from,
            position_to=(0, 0),
            delay=0):
        """
        Defines an animation action.
        duration = The duration, in frames, of the animation.
        position_from = (x, y) defining the starting position for the
            object.
        position_to = (x, y) defining the ending position for the
            object.
        delay = The number of frames to wait until starting the
            animation.

        Note that the coordinate system is non-standard, to match
        the system used by MoviePy and Pillow. (0, 0) is located at
        the TOP-LEFT of the image.
        """
        self.position_from = position_from
        self.position_to = position_to
        self.ticks_remaining = duration
        self.offset_adjustment = tuple((p_from-p_to)/dur \
            for p_from, p_to, dur in zip(
                self.position_from,
                self.position_to,
                (duration, duration)))
        self.delay = delay

    @property
    def offset(self):
        """
        Returns the offset, and then updates the offset and the ticks
        remaining.
        Use offset_static to not update.
        """
        if self.delay > 0:
            self.delay -= 1
            return (0, 0)
        else:
            self.ticks_remaining = max(
                self.ticks_remaining-1,
                0)

            if self.ticks_remaining <= 0:
                self.position_from = self.position_to
                self.offset_adjustment = (0, 0)
            else:
                self.position_from = tuple(x-y for x, y in zip(
                    self.position_from,
                    self.offset_adjustment))
                self.position_from = tuple([(
                    y if abs(x-y) <= z else x) \
                    for x, y, z in zip(
                        self.position_from,
                        self.position_to,
                        self.offset_adjustment)])

            return_value = tuple([int(x) for x in self.position_from])
            return return_value

    @property
    def offset_static(self):
        """
        Returns the current offset without updating anything.
        """
        return tuple([int(x) for x in self.position_from])

    @property
    def complete(self):
        """
        Returns if the animation is complete.
        """
        return False if self.ticks_remaining else True
