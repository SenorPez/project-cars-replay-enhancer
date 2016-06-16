"""
Provides classes for the creation of a Standings overlay.
"""
from numpy import diff, where
from PIL import Image, ImageDraw, ImageFont

from DynamicBase import DynamicBase
from ParticipantData import Driver, ParticipantData

class Standings(DynamicBase):
    """
    Creates a standings overlay that constantly updates with the
    following columns of information for each driver:
    Position | Driver | Graphical Sector Info | Time (Gap or Lap)
    Lap Progress Crawler
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

    def __init__(self, replay, clip_t=0, ups=30, process_data=True):
        self.replay = replay
        self.clip_t = clip_t
        self.ups = ups
        self.process_data = process_data

        self.participant_data = ParticipantData()

        self.material = None
        self.data_height = None
        self.column_widths = list()

        participants = {x \
            for x in self.replay.participant_lookup.values()}

        self.sector_status = {n:['current', 'none', 'none'] \
            for n in participants}
        self.pit_status = {n:False for n in participants}
        self.last_lap_valid = {n:True for n in participants}
        self.last_lap_sectors = {n:[-1, -1, -1] for n in participants}
        self.last_lap_time = None

        self.sector_bests = [-1, -1, -1]
        self.personal_bests = {n:[-1, -1, -1] for n in participants}
        self.best_lap = -1
        self.personal_best_laps = {n:-1 for n in participants}
        self.elapsed_times = {n:-1 for n in participants}

        self.current_laps = {n:1 for n in participants}
        self.last_lap_splits = {n:-1 for n in participants}
        self.leader_elapsed_time = -1
        self.leader_laps_completed = 0

        self.pit_font_path = self.replay.font.path
        self.pit_font_size = self.replay.font.size
        self.pit_font = ImageFont.truetype(
            self.pit_font_path,
            self.pit_font_size)

        self.current_group = 10
        self.next_change_time = self.clip_t+5

        #What's the slowest lap time in the entire race.
        #Used for spacing.
        telemetry_data = [x \
            for x in zip(*self.replay.telemetry_data)][0]
        telemetry_data = [item \
            for chunk in telemetry_data \
            for item in chunk]
        split_data = [[float(telemetry_data[y+1][186+i*9]) \
            for y in where(diff([float(x[186+i*9]) \
            for x in telemetry_data]) != 0)[0].tolist()] \
            for i in range(56)]
        self.max_lap_time = max([sum(x[i:i+3]) \
            for x in split_data \
            for i in range(0, len(x), 3)])

    def __sector_rectangles(self, data, pit_stop, height):
        invalid_color = (255, 0, 0)
        current_color = (255, 255, 0)
        race_best_color = (128, 0, 128)
        personal_best_color = (0, 128, 0)
        base_color = (255, 255, 255)
        border_color = (0, 0, 0)
        x_position = 0

        output = Image.new(
            'RGB',
            (int(self.replay.margin*1.5)+4, height))
        draw = ImageDraw.Draw(output)

        if pit_stop:
            draw.rectangle(
                [
                    (x_position, 0),
                    (
                        (x_position+int(self.replay.margin/2)+1)*3,
                        height-1)
                ],
                fill=(0, 0, 255),
                outline=border_color)
            width_target = ((
                x_position+int(self.replay.margin/2))*3)*0.80
            height_target = height*0.80
            while self.pit_font.getsize("PIT")[0] > width_target or \
                    self.pit_font.getsize("PIT")[1] > height_target:
                self.pit_font_size -= 1
                self.pit_font = ImageFont.truetype(
                    self.pit_font_path,
                    self.pit_font_size)
            position_x = int(
                (output.size[0]-self.pit_font.getsize("PIT")[0])/2)
            position_y = int(
                (output.size[1]-self.pit_font.getsize("PIT")[1])/2)
            draw.text(
                (position_x, position_y),
                "PIT",
                fill='white',
                font=self.pit_font)
        else:
            for sector in data:
                if sector == 'invalid':
                    fill_color = invalid_color
                elif sector == 'current':
                    fill_color = current_color
                elif sector == 'racebest':
                    fill_color = race_best_color
                elif sector == 'personalbest':
                    fill_color = personal_best_color
                elif sector == 'none':
                    fill_color = base_color
                else:
                    fill_color = (0, 0, 255)

                draw.rectangle(
                    [
                        (x_position, 0),
                        (
                            x_position+int(self.replay.margin/2)+1,
                            height-1)
                    ],
                    fill=fill_color,
                    outline=border_color)
                x_position += int(self.replay.margin/2)+1

        return output

    def _write_data(self):
        material_width = self.material.size[0]
        line_length = material_width-self.replay.margin*2

        draw = ImageDraw.Draw(self.material)

        column_positions = [
            self.replay.margin*(i+1)+sum(self.column_widths[0:i]) \
            if i == 0 \
            else self.replay.margin+self.replay.column_margin*(i)+\
            sum(self.column_widths[0:i]) \
            for i, w in enumerate(self.column_widths)]
        y_position = self.replay.margin/2

        """
        for position, name, progress, _, sector, last_sector_time, \
                _, _, _, _, orig_name in \
        """
        for driver in \
                self.participant_data.drivers_by_position[:10]+\
                self.participant_data.drivers_by_position[self.current_group:self.current_group+6]:
            position = driver.race_position
            name = self.replay.short_name_display[driver.name]
            progress = driver.progress
            sector = driver.sector
            last_sector_time = driver.last_sector_time
            orig_name = driver.name

            for print_position, print_name, print_sector, _, \
                    print_progress in [list(zip(
                            (
                                position,
                                name,
                                sector,
                                last_sector_time,
                                progress
                            ),
                            column_positions+[0]))]:
                draw.text(
                    (print_position[1], y_position),
                    str(print_position[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)
                draw.text(
                    (print_name[1], y_position),
                    str(print_name[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)

                if isinstance(
                        self.last_lap_splits[orig_name],
                        int) and \
                        self.last_lap_splits[orig_name] < 0:
                    last_lap_time = "{}".format('')
                elif isinstance(
                        self.last_lap_splits[orig_name],
                        int):
                    suffix = " laps" \
                        if self.last_lap_splits[orig_name] > 1 \
                        else " lap"
                    last_lap_time = "{:+d}".format(
                        self.last_lap_splits[orig_name])+suffix
                elif isinstance(
                        self.last_lap_splits[orig_name],
                        float) and \
                        self.last_lap_splits[orig_name] > 0:
                    last_lap_time = self.format_time(
                        self.last_lap_splits[orig_name])
                elif isinstance(
                        self.last_lap_splits[orig_name],
                        float):
                    last_lap_time = "+"+self.format_time(
                        self.last_lap_splits[orig_name]*-1)

                time_width = self.replay.font.getsize(last_lap_time)[0]

                time_position = int(
                    material_width-self.replay.margin-time_width)

                draw.text(
                    (
                        time_position,
                        y_position),
                    str(last_lap_time),
                    fill=self.replay.font_color,
                    font=self.replay.font)

                draw.line(
                    [
                        (
                            self.replay.margin,
                            y_position+self.data_height),
                        (
                            self.replay.margin+line_length*\
                                print_progress[0],
                            y_position+self.data_height)],
                    fill=(255, 0, 0),
                    width=2)
                draw.line(
                    [
                        (
                            self.replay.margin+line_length*\
                                print_progress[0],
                            y_position+self.data_height),
                        (
                            material_width-self.replay.margin,
                            y_position+self.data_height)],
                    fill=(255, 192, 192),
                    width=2)

                self.material.paste(
                    self.__sector_rectangles(
                        self.sector_status[orig_name],
                        self.pit_status[orig_name],
                        self.data_height),
                    (print_sector[1]-2, int(y_position)))

                draw.ellipse(
                    [
                        (
                            self.replay.margin+line_length*\
                                print_progress[0]-2,
                            y_position+self.data_height-2),
                        (
                            self.replay.margin+line_length*\
                                print_progress[0]+2,
                            y_position+self.data_height+2)],
                    fill=(255, 0, 0))

            y_position += self.data_height+self.replay.margin

        return self.material

    def _make_material(self, bgOnly):
        self.standings = self.update(force_process=True)

        max_minutes, _ = divmod(self.max_lap_time, 60)
        max_hours, max_minutes = divmod(max_minutes, 60)

        if max_hours > 0:
            size_string = "+24:00:00.00"
        elif max_minutes > 0:
            size_string = "+60:00.00"
        else:
            size_string = "+00.00"

        #Remap to display names
        """
        self.standings = [(p, self.replay.short_name_display[n]) + \
            tuple(rest) + (n,) for p, n, *rest \
            in self.participant_data.drivers_by_position]
        """

        self.standings = [(
            driver.race_position,
            self.replay.short_name_display[driver.name],
            driver.progress,
            driver.participant_index,
            driver.sector,
            driver.last_sector_time,
            driver.elapsed_time,
            driver.laps_completed,
            driver.current_lap,
            driver.current_position,
            driver.name) for driver \
            in self.participant_data.drivers_by_position]

        widths = [(
            self.replay.font.getsize(str(p))[0],
            self.replay.font.getsize(str(
                n.split(" ")[0][0]+". "+n.split(" ")[-1] \
                    if len(n.split(" ")) > 1 \
                    else n))[0],
            int(self.replay.margin*1.5),
            max(
                [
                    self.replay.font.getsize(str(size_string))[0],
                    self.replay.font.getsize("+00 laps")[0]])) \
            for p, n, *rest in self.standings]

        heights = [max(
            self.replay.font.getsize(str(p))[1],
            self.replay.font.getsize(str(n))[1],
            self.replay.font.getsize(str("{:.2f}".format(0.00)))[1]) \
            for p, n, *rest in self.standings]
        self.data_height = max(heights)
        heights = [self.data_height for x in self.standings[:16]]

        self.column_widths = [max(widths, key=lambda x: x[y])[y] \
            for y in range(len(widths[0]))]
        text_width = sum(self.column_widths)+\
            self.replay.column_margin*(len(widths[0])-1)
        text_height = sum(heights)+self.replay.margin*(len(heights)-1)

        self.material = Image.new('RGBA', (
            text_width+self.replay.margin*2,
            text_height+self.replay.margin))
        y_position = 0

        for i, _ in enumerate(self.standings[:16]):
            if i % 2:
                material_color = (255, 255, 255, 128)
            else:
                material_color = (192, 192, 192, 128)

            data_material = Image.new('RGBA', (
                text_width+self.replay.margin*2,
                self.data_height+self.replay.margin), material_color)
            self.material.paste(data_material, (0, y_position))
            y_position += self.data_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

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
            """
            self.standings = sorted({(
                int(telemetry_data[182+i*9]) & int('01111111', 2),
                n,
                float(telemetry_data[181+i*9])/\
                    float(telemetry_data[682]) \
                    if float(telemetry_data[181+i*9]) <= \
                        float(telemetry_data[682]) \
                    else float(0),
                int(i),
                int(telemetry_data[185+i*9]) & int('111', 2),
                float(telemetry_data[186+i*9]),
                float(telemetry_data[-1]),
                int(telemetry_data[183+i*9]),
                int(telemetry_data[184+i*9]),
                (
                    float(telemetry_data[178+i*9]),
                    float(telemetry_data[180+i*9]))
                ) for i, n, *rest in participant_data})
            """


            if self.clip_t > self.next_change_time:
                self.current_group = self.current_group+6 if \
                    self.current_group+6 < len(self.participant_data.drivers_by_position) else 10
                self.next_change_time = self.clip_t+5

            for standing in self.participant_data.drivers_by_position:
                position = standing.race_position
                name = standing.name
                progress = standing.progress
                sector = standing.sector
                last_sector_time = standing.last_sector_time
                laps_complete = standing.laps_completed
                valid_lap = standing.valid_lap
                current_lap = standing.current_lap
                location = standing.current_position
                """
                Standings Data Structure
                    p 0: int Race Position (sorted)
                    n 1: string Name
                    r 2: float Percentage of lap completed
                    i 3: int Participant index
                    s 4: int Current sector
                    l 5: float Last sector time (-123 if none)
                   et 6: float Elapsed time
                   lx 7: int Laps completed and valid lap
                   cl 8: int Current lap
                  loc 9: tuple(float, float) x,z position
                """
                if self.pit_status[name] is False and \
                        self.replay.track.at_pit_entry(location):
                    self.pit_status[name] = True
                elif self.pit_status[name] is True and \
                        self.replay.track.at_pit_exit(location):
                    self.pit_status[name] = False

                if sector == 1:
                    #If we're in the first sector, we need to check to
                    #see if we've set a record in sector 3.
                    if last_sector_time != -123:
                        self.sector_status[name][0] = 'current'

                        if self.last_lap_sectors[name][0] != \
                                last_sector_time:
                            self.last_lap_sectors[name][0] = \
                                last_sector_time

                        if laps_complete & int('10000000', 2) and \
                                progress > 0:
                            self.sector_status[name][1] = 'invalid'
                            self.sector_status[name][2] = 'invalid'
                            self.last_lap_valid[name] = False
                        elif self.sector_status[name][2] != 'invalid':
                            if self.sector_bests[2] == -1 or \
                                    self.sector_bests[2] >= \
                                    last_sector_time:
                                self.sector_bests[2] = \
                                    last_sector_time
                                self.personal_bests[name][2] = \
                                    last_sector_time
                                self.sector_status[name][2] = \
                                    'racebest'
                            elif self.personal_bests[name][2] == -1 or \
                                    self.personal_bests[name][2] >= \
                                    last_sector_time:
                                self.personal_bests[name][2] = \
                                    last_sector_time
                                self.sector_status[name][2] = \
                                    'personalbest'
                            else:
                                self.sector_status[name][2] = \
                                    'none'

                        #Test to see if we've just started a new lap.
                        if self.current_laps[name] != current_lap:
                            self.elapsed_times[name] += float(
                                sum(self.last_lap_sectors[name]))
                            self.current_laps[name] = current_lap

                            #Do we have a valid last lap? If so,
                            #compare records.
                            #If not, set Sector 3 to invalid (to hold
                            #it at red until we get back there and
                            #reset the flag.
                            if self.last_lap_valid[name] and \
                                    -1 not in \
                                    self.last_lap_sectors[name]:
                                self.last_lap_time = float(
                                    sum(self.last_lap_sectors[name]))
                                if self.best_lap == -1 or \
                                        self.best_lap > \
                                        self.last_lap_time:
                                    self.best_lap = self.last_lap_time
                                    self.personal_best_laps[name] = \
                                        self.last_lap_time
                                elif self.personal_best_laps[name] == \
                                        -1 or \
                                        self.personal_best_laps[name] \
                                        >= self.last_lap_time:
                                    self.personal_best_laps[name] = \
                                        self.last_lap_time
                            else:
                                self.sector_status[name][2] = 'invalid'
                                self.last_lap_valid[name] = True

                            if position == 1:
                                self.leader_laps_completed = \
                                    current_lap
                                self.leader_elapsed_time = \
                                    self.elapsed_times[name]
                                self.last_lap_splits[name] = float(
                                    sum(self.last_lap_sectors[name]))
                            #Test to see if you're down a lap.
                            elif self.leader_laps_completed > \
                                    current_lap:
                                self.last_lap_splits[name] = \
                                    int(
                                        self.leader_laps_completed-\
                                        current_lap)
                            #Just a laggard.
                            elif laps_complete & int(
                                    '01111111', 2) != 0:
                                self.last_lap_splits[name] = float(
                                    self.leader_elapsed_time-\
                                        self.elapsed_times[name])
                elif sector == 2:
                    #Sector 2 checks sector 1 records
                    if last_sector_time != -123:
                        self.sector_status[name][1] = 'current'

                        if self.last_lap_sectors[name][1] != \
                                last_sector_time:
                            self.last_lap_sectors[name][1] = \
                                last_sector_time

                        if laps_complete & int('10000000', 2) and \
                                progress > 0:
                            self.sector_status[name][0] = 'invalid'
                            self.sector_status[name][2] = 'invalid'
                            self.last_lap_valid[name] = False
                        elif self.sector_status[name][0] != 'invalid':
                            if self.sector_bests[0] == -1 or \
                                    self.sector_bests[0] >= \
                                    laps_complete:
                                self.sector_bests[0] = laps_complete
                                self.personal_bests[name][0] = \
                                    laps_complete
                                self.sector_status[name][0] = \
                                    'racebest'
                            elif self.personal_bests[name][0] == -1 or \
                                    self.personal_bests[name][0] >= \
                                    laps_complete:
                                self.personal_bests[name][0] = \
                                    laps_complete
                                self.sector_status[name][0] = \
                                    'personalbest'
                            else:
                                self.sector_status[name][0] = \
                                    'none'
                elif sector == 3:
                    #Sector 3 checks sector 2 records.
                    if last_sector_time != -123:
                        self.sector_status[name][2] = 'current'

                        if self.last_lap_sectors[name][2] != \
                                last_sector_time:
                            self.last_lap_sectors[name][2] = \
                                last_sector_time

                        if laps_complete & int('10000000', 2) and \
                                progress > 0:
                            self.sector_status[name][0] = 'invalid'
                            self.sector_status[name][1] = 'invalid'
                            self.last_lap_valid[name] = False
                        elif self.sector_status[name][1] != 'invalid':
                            if self.sector_bests[1] == -1 or \
                                    self.sector_bests[1] >= \
                                    last_sector_time:
                                self.sector_bests[1] = last_sector_time
                                self.personal_bests[name][1] = \
                                    last_sector_time
                                self.sector_status[name][1] = \
                                    'racebest'
                            elif self.personal_bests[name][1] == -1 or \
                                    self.personal_bests[name][1] >= \
                                    last_sector_time:
                                self.personal_bests[name][1] = \
                                    last_sector_time
                                self.sector_status[name][1] = \
                                    'personalbest'
                            else:
                                self.sector_status[name][1] = 'none'

                self.last_lap_time = self.last_lap_splits[name]

        self.clip_t += float(1/self.ups)

        return self.participant_data.drivers_by_position

    def to_frame(self):
        return super(Standings, self).to_frame()

    def make_mask(self):
        return super(Standings, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Standings, DynamicBase))
    print('Instance:', isinstance(Standings(30), DynamicBase))
