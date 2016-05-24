"""
Provides the default Results screen for the Project CARS Replay
Enhancer
"""
from numpy import diff, nonzero

from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Results(StaticBase):
    """
    Defines a static Results card, consisting of the following columns:

    - Classification (Finish position or DNF)
    - Driver Name
    - Team (if provided)
    - Car
    - Laps Completed
    - Race Time
    - Personal Best Lap Time
    - Personal Best Sector 1 Time
    - Personal Best Sector 2 Time
    - Personal Best Sector 3 Time
    - Points Earned
    """
    def __init__(self, replay):
        self.replay = replay

        participants = {x for x \
            in self.replay.participant_lookup.values()}
        self.lap_finish = {n:None for n in participants}

        self.classification = None
        self.material = None
        self.widths = None
        self.data_height = None


    def _write_data(self):
        draw = ImageDraw.Draw(self.material)

        y_pos = self.replay.margin

        draw.text(
            (20, y_pos),
            self.replay.heading_text,
            fill=self.replay.heading_font_color,
            font=self.replay.heading_font)
        y_pos += self.replay.heading_font.getsize(
            self.replay.heading_text)[1]

        draw.text(
            (20, y_pos),
            self.replay.subheading_text,
            fill=self.replay.heading_font_color,
            font=self.replay.font)
        y_pos += self.replay.font.getsize(
            self.replay.subheading_text)[1]+self.replay.margin
        y_pos += self.replay.margin/2

        column_positions = [self.replay.margin if i == 0 \
            else self.replay.margin+self.replay.column_margin*i+sum(
                self.widths[0:i]) if self.widths[i-1] != 0 \
                    else self.replay.margin+ \
                        self.replay.column_margin*(i-1)+\
                        sum(self.widths[0:(i-1)])
                            for i, w in enumerate(self.widths)]

        for position, name, team, car, laps, elapsed_time, best_lap, \
                best_sector_1, best_sector_2, best_sector_3, points \
                in [list(zip(x, column_positions)) \
                for x in self.classification]:
            draw.text(
                (position[1], y_pos),
                str(position[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (name[1], y_pos),
                name[0],
                fill=self.replay.font_color,
                font=self.replay.font)
            if team != "":
                draw.text(
                    (team[1], y_pos),
                    str(team[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)
            draw.text(
                (car[1], y_pos),
                str(car[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (laps[1]+(self.widths[4]-self.replay.font.getsize(
                    str(laps[0]))[0])/2, y_pos),
                str(laps[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (elapsed_time[1]+(
                    self.widths[5]-self.replay.font.getsize(
                        str(elapsed_time[0]))[0])/2, y_pos),
                str(elapsed_time[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_lap[1]+(self.widths[6]-self.replay.font.getsize(
                    str(best_lap[0]))[0])/2, y_pos),
                str(best_lap[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_1[1]+(
                    self.widths[7]-self.replay.font.getsize(
                        str(best_sector_1[0]))[0])/2, y_pos),
                str(best_sector_1[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_2[1]+(
                    self.widths[8]-self.replay.font.getsize(
                        str(best_sector_2[0]))[0])/2, y_pos),
                str(best_sector_2[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            draw.text(
                (best_sector_3[1]+(
                    self.widths[9]-self.replay.font.getsize(
                        str(best_sector_3[0]))[0])/2, y_pos),
                str(best_sector_3[0]),
                fill=self.replay.font_color,
                font=self.replay.font)
            if points != "":
                draw.text(
                    (points[1]+(self.widths[10]-self.replay.font.getsize(
                        str(points[0]))[0])/2, y_pos),
                    str(points[0]),
                    fill=self.replay.font_color,
                    font=self.replay.font)
            y_pos += self.data_height+self.replay.margin

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
            for index, name, *rest in participant_data:
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

        column_headings = [(
            "Pos.",
            "Driver",
            "Team",
            "Car",
            "Laps",
            "Time",
            "Best Lap",
            "Best S1",
            "Best S2",
            "Best S3",
            "Points")]

        if self.replay.point_structure is not None and \
                len(self.replay.point_structure) < 17:
            self.replay.point_structure += [0] * \
                (17-len(self.replay.point_structure))

        self.classification = [(
            str(p),
            n,
            t,
            c,
            str(l),
            self.format_time(sum(lap_times[n])),
            self.format_time(float(min(valid_lap_times[n]))) \
                if len(valid_lap_times[n]) \
                else "",
            self.format_time(float(sector_bests[n][0])) \
                if sector_bests[n][0] != -1 \
                else "",
            self.format_time(float(sector_bests[n][1])) \
                if sector_bests[n][1] != -1 \
                else "",
            self.format_time(float(sector_bests[n][2])) \
                if sector_bests[n][2] != -1 \
                else "",
            "" if self.replay.point_structure is None else "0" \
                if p == "DNF" \
                else "0" \
                    if l < 1 \
                    else str(
                        self.replay.point_structure[p]+\
                            self.replay.point_structure[0]
                        if min([x for x \
                            in personal_best_laps.values() \
                                if isinstance(x, float)]) == \
                                    personal_best_laps[n] \
                                else self.replay.point_structure[p])) \
            for p, n, t, c, l in self.classification[:16]]

        #Remap to display names
        self.classification = [(
            p,
            self.replay.name_display[n]) + tuple(rest) \
            for p, n, *rest in self.classification]


        column_headings = [tuple([x \
            if len([y[i] \
                for y in self.classification \
                if len(y[i])]) \
            else "" for i, x in enumerate(*column_headings)])]
        self.classification = column_headings+self.classification

        self.widths = [max([self.replay.font.getsize(x[i])[0] \
                for x in self.classification]) \
            for i in range(len(self.classification[0]))]
        self.widths.append(sum(self.widths))

        heights = [max([self.replay.font.getsize(x[i])[1] \
                for x in self.classification]) \
            for i in range(len(self.classification[0]))]
        self.data_height = max(heights)
        heights = [self.data_height for x in self.classification]
        heights.append(self.replay.heading_font.getsize(
            self.replay.heading_text)[1])
        heights.append(self.replay.font.getsize(
            self.replay.subheading_text)[1])

        header_height = self.replay.heading_font.getsize(
            self.replay.heading_text)[1]+\
            self.replay.font.getsize(
                self.replay.subheading_text)[1]+\
                self.replay.margin*2

        text_width = max(
            self.widths[-1]+self.replay.column_margin*(len(
                [x for x in self.widths[:-1] if x != 0])-1),
            self.replay.heading_font.getsize(
                self.replay.heading_text)[0]+\
                self.replay.column_margin+header_height,
            self.replay.font.getsize(
                self.replay.subheading_text)[0]+\
                self.replay.column_margin+header_height)
        text_height = sum(heights)+self.replay.margin*len(heights)-1

        heading_material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, header_height),
            self.replay.heading_color)

        if len(self.replay.series_logo):
            series_logo = Image.open(
                self.replay.series_logo).resize(
                    (heading_material.height, heading_material.height))
            heading_material.paste(
                series_logo,
                (heading_material.width-series_logo.width, 0))

        self.material = Image.new(
            'RGBA',
            (text_width+self.replay.margin*2, text_height))
        self.material.paste(heading_material, (0, 0))

        y_pos = header_height
        for i, _ in enumerate(self.classification):
            if i % 2:
                material_color = (255, 255, 255)
            else:
                material_color = (192, 192, 192)

            row_material = Image.new(
                'RGBA',
                (
                    text_width+self.replay.margin*2,
                    self.data_height+self.replay.margin),
                material_color)
            self.material.paste(row_material, (0, y_pos))
            y_pos += self.data_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

    def to_frame(self):
        return super(Results, self).to_frame()

    def make_mask(self):
        return super(Results, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Results, StaticBase))
    print('Instance:', isinstance(Results(0), StaticBase))
