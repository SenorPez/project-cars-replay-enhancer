"""
Provides the default Series Champion screen for the Project CARS
Replay Enhancer
"""
from numpy import diff, nonzero
from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Champion(StaticBase):
    """
    Defines a static Champion card, consisting of the top three
    finishers in points, as Champions and Runners Up.
    """
    def __init__(self, replay):
        self.replay = replay

        participants = {
            x for x in self.replay.participant_lookup.values()}
        self.lap_finish = {n:None for n in participants}

        self.classification = list()
        self.material = None
        self.heading_height = None

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)

        draw.text(
            (self.replay.margin, self.replay.margin),
            self.replay.heading_text,
            fill=self.heading_font_color,
            font=self.replay.heading_font)

        x_pos = 300+self.replay.margin
        y_pos = self.heading_height+self.replay.margin

        for rank, name, team, car, *_ in self.classification[0:3]:
            if rank == '1':
                draw.text(
                    (x_pos, y_pos),
                    "Champion",
                    fill=self.font_color,
                    font=self.replay.heading_font)
                y_pos += self.replay.heading_font.getsize("Champion")[1]
                draw.text(
                    (x_pos, y_pos),
                    str(name),
                    fill=self.font_color,
                    font=self.replay.heading_font)
                y_pos += self.replay.heading_font.getsize(name)[1]
            else:
                draw.text(
                    (x_pos, y_pos),
                    "Runner Up",
                    fill=self.font_color,
                    font=self.replay.font)
                y_pos += self.replay.font.getsize("Runner Up")[1]
                draw.text(
                    (x_pos, y_pos),
                    str(name),
                    fill=self.font_color,
                    font=self.replay.font)
                y_pos += self.replay.font.getsize(name)[1]
            draw.text(
                (x_pos+self.replay.column_margin, y_pos),
                team,
                fill=self.font_color,
                font=self.replay.font)
            y_pos += self.replay.font.getsize(team)[1]
            draw.text(
                (x_pos+self.replay.column_margin, y_pos),
                car,
                fill=self.font_color,
                font=self.replay.font)
            y_pos += self.replay.font.getsize(car)[1]+self.replay.margin

        return self.material

    def _make_material(self, bgOnly):
        participants = {x for x \
            in self.replay.participant_lookup.values()}
        sector_bests = {n:[-1, -1, -1] for n in participants}
        sector_times = {n:[] for n in participants}
        laps_finished = {n:0 for n in participants}
        lap_times = {n:[] for n in participants}

        valid_lap_times = {n:[] for n in participants}
        personal_best_laps = {n:'' for n in participants}
        invalid_laps = {n:[] for n in participants}

        laps_at_p1_finish = {n:None for n in participants}
        finish_status = {n:{'laps':None, 'dnf':True, 'position':None} \
            for n in participants}

        #Get the telemetry data from P1 finish to race end.
        index = -1
        participant_data = [sorted(self.replay.telemetry_data[-1][-1])]
        offset = [self.replay.telemetry_data[-1][2]]
        telemetry_data = [self.replay.telemetry_data[-1][0]]

        while offset[0] > self.replay.race_p1_finish:
            index -= 1
            offset.insert(0, self.replay.telemetry_data[index][2])
            participant_data.insert(
                0,
                self.replay.telemetry_data[index][-1])
            telemetry_data.insert(
                0,
                self.replay.telemetry_data[index][0])
        combined_data = [x for x in zip(
            telemetry_data,
            offset,
            participant_data)]

        p1_offset = self.replay.race_p1_finish-offset[0]

        #Lap data at P1 finish.
        for name, laps in [(
                participant_data[0][i][1],
                int(telemetry_data[0][p1_offset][184+i*9])) \
                    for i in range(int(
                        telemetry_data[0][p1_offset][4]))]:
            laps_at_p1_finish[name] = laps

        position_1 = max(
            [(name, laps) for name, laps \
             in laps_at_p1_finish.items()
             if laps is not None],
            key=lambda x: x[1])

        finish_position = 1
        finish_status[position_1[0]]['position'] = finish_position
        finish_status[position_1[0]]['dnf'] = False
        finish_status[position_1[0]]['laps'] = position_1[1]-1

        #Lap data at race finish.
        for telemetry_data, offset, participant_data in combined_data:
            finish_data = [(
                participant_data[i][1],
                int(x[184+participant_data[i][0]*9])) \
                for telemetry_index, x in enumerate(telemetry_data) \
                for i in range(int(x[4])) \
                if telemetry_index+offset > self.replay.race_p1_finish]

            for name, laps in finish_data:
                if finish_status[name]['laps'] is None:
                    finish_status[name]['laps'] = laps
                elif laps > finish_status[name]['laps'] and \
                        finish_status[name]['dnf']:
                    finish_status[name]['dnf'] = False
                    finish_position += 1
                    finish_status[name]['position'] = finish_position

            #The DNFs might have finished ahead of P1 (but after time
            #expired) in a timed race.
            if self.replay.race_mode == "Time":
                finish_data = {(
                    participant_data[i][1],
                    int(x[184+participant_data[i][0]*9])) \
                    for telemetry_index, x in enumerate(telemetry_data) \
                    for i in range(int(x[4])) \
                    if telemetry_index+offset > self.replay.time_expired}
                for name, laps in finish_data:
                    if laps < finish_status[name]['laps'] and \
                           finish_status[name]['dnf']:
                        finish_status[name]['dnf'] = False
                        finish_position += 1
                        finish_status[name]['position'] = finish_position
                        finish_status[name]['laps'] = laps                    

            #Find the indexes when the last laps end.
            for index, name, *_ in participant_data:
                if self.lap_finish[name] is None:
                    lap_finish_index = self.replay.race_p1_finish
                    if name == position_1[0]:
                        self.lap_finish[name] = lap_finish_index
                    else:
                        try:
                            telemetry_offset = \
                                self.replay.race_p1_finish-offset
                            while telemetry_data[telemetry_offset]\
                                    [184+index*9] == \
                                telemetry_data[lap_finish_index-offset]\
                                    [184+index*9]:
                                lap_finish_index += 1
                        except IndexError:
                            lap_finish_index = None
                        self.lap_finish[name] = lap_finish_index

        #Assign finish positions to the DNFs that didn't drop out.
        for name, laps in sorted(
                [(name, value['laps']) \
                    for name, value in finish_status.items() \
                    if value['laps'] is not None and value['dnf']],
                key=lambda x: x[1],
                reverse=True):
            finish_status[name]['laps'] = laps-1
            finish_position += 1
            finish_status[name]['position'] = finish_position

        all_participants = {x[1:] \
            for i in range(len(self.replay.telemetry_data)) \
            for x in self.replay.telemetry_data[i][-1]}
        self.classification = sorted(
            [(
                finish_status[name]['position'],
                name,
                team,
                car,
                finish_status[name]['laps'])
             for name, team, car \
                in all_participants \
            if finish_status[name]['position'] is not None])

        dnf_classification = sorted(
            [(
                finish_status[name]['position'],
                name,
                team,
                car,
                finish_status[name]['laps'])
             for name, team, car \
                in all_participants \
            if finish_status[name]['position'] is None],
            key=lambda x: x[1].lower())
        self.classification.extend(dnf_classification)

        self.classification = [
            (
                ("DNF",) if finish_status[n]['dnf'] \
                    else (p,)) + (n,) + tuple(rest)
            for p, (i, n, *rest) in enumerate(self.classification, 1)]

        for telemetry_data, _, index_offset, participant_data \
                in self.replay.telemetry_data:
            for index, name, *_ in participant_data:
                lap_finish = self.lap_finish[name] \
                    if self.lap_finish[name] is not None \
                    else self.replay.race_end
                new_sector_times = [
                    float(telemetry_data[x][186+index*9]) \
                        for x in nonzero(diff([int(y[185+index*9]) & \
                            int('111', 2) \
                        for data_index, y \
                        in enumerate(telemetry_data, index_offset) \
                        if data_index <= lap_finish]))[0].tolist() \
                        if float(telemetry_data[x][186+index*9]) \
                            != -123.0]
                if float(telemetry_data[-1][186+index*9]) != -123.0:
                    new_sector_times += \
                        [float(telemetry_data[-1][186+index*9])]

                try:
                    if sector_times[name][-1] == new_sector_times[0]:
                        sector_times[name] += new_sector_times[1:]
                    else:
                        raise IndexError
                except IndexError:
                    sector_times[name] += new_sector_times

                laps_finished[name] = len(sector_times[name]) // 3

                invalid_laps[name] += list({int(x[184+index*9]) \
                    for x in telemetry_data \
                    if int(x[183+index*9]) & int('10000000') and \
                        float(x[186+index*9]) != -123.0})

        #Pull lap times. This doesn't filter out invalids, as this is
        #used for the total time.
        #I recognize this is insanely sloppy, but at this point, I
        #just can't care.
        for name, _ in sector_times.items():
            lap_times[name] = [sum(sector_times[name][x:x+3]) \
                for x in range(0, len(sector_times[name]), 3)]


        for name, laps in invalid_laps.items():
            for lap in reversed(sorted({x for x in laps})):
                del sector_times[name][(lap-1)*3:(lap-1)*3+3]

        for name, _ in sector_times.items():
            #sector_times[n] += [sector_times[n].pop(0)]
            try:
                sector_bests[name][0] = \
                    min([x for x in sector_times[name][::3]])
            except ValueError:
                sector_bests[name][0] = -1

            try:
                sector_bests[name][1] = \
                    min([x for x in sector_times[name][1::3]])
            except ValueError:
                sector_bests[name][1] = -1

            try:
                sector_bests[name][2] = \
                    min([x for x in sector_times[name][2::3]])
            except ValueError:
                sector_bests[name][2] = -1

            sector_times[name] = sector_times[name][:divmod(len(
                sector_times[name]), 3)[0]*3]
            valid_lap_times[name] = [sum(sector_times[name][x:x+3]) \
                for x in range(0, len(sector_times[name]), 3)]
            try:
                personal_best_laps[name] = \
                    min([x for x in valid_lap_times[name]])
            except ValueError:
                personal_best_laps[name] = -1

        #Remove the early-quitters.
        #Add in their lap data and sort.
        #Readd.
        #There has to be a better way?
        dnf_classification = [x for x in self.classification \
            if x[-1] is None]
        #self.classification = [x for x in self.classification \
            #if x[-1] is not None]

        self.classification = sorted(
            [(
                position,
                name,
                team,
                car,
                laps)
             for position, name, team, car, laps \
                in self.classification
             if laps is not None],
            key=lambda x: sum(lap_times[x[1]]))

        self.classification = sorted(
            [(
                position,
                name,
                team,
                car,
                laps)
             for position, name, team, car, laps \
                in self.classification],
            key=lambda x: x[-1], reverse=True)

        self.classification = [
            ("DNF" if position == "DNF" else index,) + \
            tuple(rest) \
            for index, (position, *rest) \
                in enumerate(self.classification, 1)]

        dnf_classification = sorted(
            [(
                "DNF",
                name,
                team,
                car,
                laps_finished[name])
             for position, name, team, car, laps \
                in dnf_classification],
            key=lambda x: sum(lap_times[x[1]]))

        dnf_classification = sorted(
            [(
                "DNF",
                name,
                team,
                car,
                laps_finished[name])
             for position, name, team, car, laps \
                in dnf_classification],
            key=lambda x: x[-1], reverse=True)
        self.classification.extend(dnf_classification)

        if self.replay.point_structure is not None and \
                len(self.replay.point_structure) < 17:
            self.replay.point_structure += [0] * \
                (17-len(self.replay.point_structure))

        self.classification = [(
            name,
            team,
            car,
            str(16-16) if self.replay.point_structure is None \
                and position == "DNF"
            else str(16-int(position)) if self.replay.point_structure is None \
            else str(self.replay.points[name]) if position == "DNF"
            else str(self.replay.points[name]) if laps < 1 else str(
                self.replay.points[name]+\
                self.replay.point_structure[position]+\
                self.replay.point_structure[0] \
                    if min([x for x in personal_best_laps.values() \
                        if isinstance(x, float)]) == \
                        personal_best_laps[name] \
                    else \
                self.replay.points[name]+\
                self.replay.point_structure[position])) \
            for position, name, team, car, laps \
            in self.classification[:16]]

        self.classification = sorted(
            self.classification,
            key=lambda x: x[0].lower())
        self.classification = sorted(
            self.classification,
            key=lambda x: int(x[-1]),
            reverse=True)

        for rank, data in enumerate(self.classification):
            if rank == 0:
                self.classification[rank] = (str(rank+1),)+data
            elif self.classification[rank-1][-1] == data[-1]:
                self.classification[rank] = (str(
                    self.classification[rank-1][0]),)+data
            else:
                self.classification[rank] = (str(rank+1),)+data

        #Remap to display names
        self.classification = [
            (p, self.replay.name_display[n]) + tuple(rest) \
            for p, n, *rest \
            in self.classification]

        heading_width = self.replay.heading_font.getsize(
            self.replay.heading_text)[0]+self.replay.margin*2
        text_width = max(
            [max(
                [self.replay.heading_font.getsize(n)[0] \
                     if r == '1' \
                     else self.replay.font.getsize(n)[0],
                 self.replay.font.getsize(t)[0]+\
                    self.replay.column_margin,
                 self.replay.font.getsize(c)[0]+\
                    self.replay.column_margin]) \
            for r, n, t, c, *rest \
            in self.classification[0:3]]+\
                [self.replay.heading_font.getsize("Champion")[0]]+\
                [self.replay.font.getsize("Runner Up")[0]])+\
                self.replay.margin*2

        self.heading_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]+self.replay.margin*2
        text_height = max(
            [300, sum(
                [self.replay.heading_font.getsize(n)[1]+\
                    self.replay.font.getsize(t)[1]+\
                    self.replay.font.getsize(c)[1] \
                    if r == '1' \
                    else self.replay.font.getsize(n)[1]+\
                    self.replay.font.getsize(t)[1]+\
                    self.replay.font.getsize(c)[1] \
                    for r, n, t, c, *rest \
                    in self.classification[0:3]]+\
                    [self.replay.heading_font.getsize("Champion")[1]]+\
                    [self.replay.font.getsize("Runner Up")[1]*2])+\
                    self.replay.margin*4])

        width = max((heading_width, 300+text_width))
        height = self.heading_height+text_height

        heading_material = Image.new(
            'RGBA',
            (width, self.heading_height),
            self.replay.heading_color)

        self.material = Image.new(
            'RGBA',
            (width, height),
            (255, 255, 255))
        self.material.paste(heading_material, (0, 0))

        if len(self.replay.series_logo):
            series_logo = Image.open(
                self.replay.series_logo).resize((300, 300))
            self.material.paste(
                series_logo,
                (0, self.heading_height))

        return self.material if bgOnly else self._write_data()

    def to_frame(self):
        return super(Champion, self).to_frame()

    def make_mask(self):
        return super(Champion, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Champion, StaticBase))
    print('Instance:', isinstance(Champion(0), StaticBase))
