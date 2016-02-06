from collections import deque
from numpy import diff, nonzero

from PIL import Image, ImageDraw

from StaticBase import StaticBase

class Results(StaticBase):
    def __init__(self, replay):
        self.replay = replay

        participants = {x for x in self.replay.participant_lookup.values()}
        self.lap_finish = {n:-1 for n in participants}

    def _write_data(self):
        draw = ImageDraw.Draw(self.material)

        yPos = self.replay.margin

        draw.text((20, yPos), self.replay.heading_text, fill='white', font=self.replay.heading_font)
        yPos += self.replay.heading_font.getsize(self.replay.heading_text)[1]

        draw.text((20, yPos), self.replay.subheading_text, fill='white', font=self.replay.font)
        yPos += self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin
        yPos += self.replay.margin/2

        column_positions = [self.replay.margin if i == 0 else self.replay.margin+self.replay.column_margin*i+sum(self.widths[0:i]) if self.widths[i-1] != 0 else self.replay.margin+self.replay.column_margin*(i-1)+sum(self.widths[0:(i-1)]) for i, w in enumerate(self.widths)]

        for p, n, t, c, l, et, bl, bs1, bs2, bs3, pts in [list(zip(x, column_positions)) for x in self.classification]:
            draw.text((p[1], yPos), str(p[0]), fill='black', font=self.replay.font)
            draw.text((n[1], yPos), str(n[0]), fill='black', font=self.replay.font)
            if t != "":
                draw.text((t[1], yPos), str(t[0]), fill='black', font=self.replay.font)
            draw.text((c[1], yPos), str(c[0]), fill='black', font=self.replay.font)
            draw.text((l[1]+(self.widths[4]-self.replay.font.getsize(str(l[0]))[0])/2, yPos), str(l[0]), fill='black', font=self.replay.font)
            draw.text((et[1]+(self.widths[5]-self.replay.font.getsize(str(et[0]))[0])/2, yPos), str(et[0]), fill='black', font=self.replay.font)
            draw.text((bl[1]+(self.widths[6]-self.replay.font.getsize(str(bl[0]))[0])/2, yPos), str(bl[0]), fill='black', font=self.replay.font)
            draw.text((bs1[1]+(self.widths[7]-self.replay.font.getsize(str(bs1[0]))[0])/2, yPos), str(bs1[0]), fill='black', font=self.replay.font)
            draw.text((bs2[1]+(self.widths[8]-self.replay.font.getsize(str(bs2[0]))[0])/2, yPos), str(bs2[0]), fill='black', font=self.replay.font)
            draw.text((bs3[1]+(self.widths[9]-self.replay.font.getsize(str(bs3[0]))[0])/2, yPos), str(bs3[0]), fill='black', font=self.replay.font)
            draw.text((pts[1]+(self.widths[10]-self.replay.font.getsize(str(pts[0]))[0])/2, yPos), str(pts[0]), fill='black', font=self.replay.font)
            yPos += self.data_height+self.replay.margin

        return self.material

    def _make_material(self, bgOnly):
        participants = {x for x in self.replay.participant_lookup.values()}
        sector_bests = {n:[-1, -1, -1] for n in participants}
        sector_times = {n:[] for n in participants}
        laps_finished = {n:0 for n in participants}
        lap_times = {n:[] for n in participants}
        valid_lap_times = {n:[] for n in participants}
        personal_best_laps = {n:'' for n in participants}
        invalid_laps = {n:[] for n in participants}

        '''
        sector_bests = [[-1, -1, -1] for x in range(len(self.classification))]
        sector_times = [list() for x in range(len(self.classification))]
        lap_times = [list() for x in range(len(self.classification))]
        personal_best_laps = ['' for x in range(len(self.classification))]
        '''

        telemetry_data, participant_data, offset = zip(*[(x[0], x[-1], x[2]) for x in self.replay.telemetry_data if x[2] < self.replay.race_finish])
        participant_data = participant_data[-1]
        offset = offset[-1]
        telemetry_data = telemetry_data[-1][self.replay.race_finish-offset]
        #telemetry_data = telemetry_data[0][self.replay.race_finish-telemetry_data[2]]

        lead_lap_indexes = [i for i, *rest in participant_data if int(telemetry_data[184+i*9]) >= int(telemetry_data[10])]
        lapped_indexes = [i for i, *rest in participant_data if int(telemetry_data[184+i*9]) < int(telemetry_data[10])]

        telemetry_data = [x[0] for x in self.replay.telemetry_data if x[2] < self.replay.race_end]
        telemetry_data = telemetry_data[-1][-1]
        self.classification = sorted((int(telemetry_data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(telemetry_data[10])) for i, n, t, c in participant_data if i in lead_lap_indexes)
        self.classification += sorted((int(telemetry_data[182+i*9]) & int('01111111', 2), n, t if t is not None else "", c, i, int(telemetry_data[183+i*9]) & int('01111111', 2)) for i, n, t, c in participant_data if i in lapped_indexes)
        self.classification = [(p,) + tuple(rest) for p, (i, *rest) in enumerate(self.classification, 1)]

        telemetry_data = [x for x in zip(*self.replay.telemetry_data)][0]
        telemetry_data = [item for chunk in telemetry_data for item in chunk]

        for p, n, t, c, i, l in self.classification[:16]:
            lap_finish_number = self.replay.race_finish
            if p != 1:
                try:
                    while telemetry_data[self.replay.race_finish][183+i*9] == telemetry_data[lap_finish_number][183+i*9]:
                        lap_finish_number += 1
                except IndexError:
                    lap_finish_number = len(telemetry_data)-1
                self.lap_finish[n] = lap_finish_number
            #sector_times[n] += [float(telemetry_data[lap_finish_number][186+i*9])]

        for telemetry_data, participant_number, index_offset, participant_data in self.replay.telemetry_data:
            for i, n, *rest in participant_data:
                lap_finish = self.lap_finish[n] if self.lap_finish[n] != -1 else self.replay.race_end
                new_sector_times = [float(telemetry_data[x][186+i*9]) for x in nonzero(diff([int(y[185+i*9]) & int('111', 2) for data_index, y in enumerate(telemetry_data, index_offset) if data_index <= lap_finish]))[0].tolist() if float(telemetry_data[x][186+i*9]) != -123.0]
                if float(telemetry_data[-1][186+i*9]) != -123.0:
                    new_sector_times += [float(telemetry_data[-1][186+i*9])]
                
                try:
                    if sector_times[n][-1] == new_sector_times[0]:
                        sector_times[n] += new_sector_times[1:]
                    else:
                        raise IndexError
                except IndexError:
                    sector_times[n] += new_sector_times

                laps_finished[n] = len(sector_times[n]) // 3

                invalid_laps[n] += list({int(x[184+i*9]) for x in telemetry_data if int(x[183+i*9]) & int('10000000') and float(x[186+i*9]) != -123.0})

        #Pull lap times. This doesn't filter out invalids, as this is used for the total time.
        #I recognize this is insanely sloppy, but at this point, I just can't care.
        for n, v in sector_times.items():
            lap_times[n] = [sum(sector_times[n][x:x+3]) for x in range(0, len(sector_times[n]), 3)]

        for n, laps in invalid_laps.items():
            for lap in reversed(sorted({x for x in laps})):
                del sector_times[n][(lap-1)*3:(lap-1)*3+3]

        for n, v in sector_times.items():
            #sector_times[n] += [sector_times[n].pop(0)]
            try:
                sector_bests[n][0] = min([x for x in sector_times[n][::3]])
            except ValueError:
                sector_bests[n][0] = -1

            try:
                sector_bests[n][1] = min([x for x in sector_times[n][1::3]])
            except ValueError:
                sector_bests[n][1] = -1

            try:
                sector_bests[n][2] = min([x for x in sector_times[n][2::3]])
            except ValueError:
                sector_bests[n][2] = -1

            sector_times[n] = sector_times[n][:divmod(len(sector_times[n]), 3)[0]*3]
            valid_lap_times[n] = [sum(sector_times[n][x:x+3]) for x in range(0, len(sector_times[n]), 3)]
            try:
                personal_best_laps[n] = min([x for x in valid_lap_times[n]])
            except ValueError:
                personal_best_laps[n] = -1


            #sector_times[n] = [float(self.replay.telemetry_data[x][186+i*9]) for x in where(diff([int(y[185+i*9]) & int('111', 2) for y in self.replay.telemetry_data[:lap_finish+1]]) != 0)[0].tolist() if float(self.replay.telemetry_data[x][186+i*9]) != -123.0]+[float(self.replay.telemetry_data[lap_finish][186+i*9])]

            #sector_times[n] = sector_times[n][:divmod(len(sector_times[n]), 3)[0]*3]

            #lap_times[n] = [sum(sector_times[n][x:x+3]) for x in range(0, len(sector_times[n]), 3)]
            #personal_best_laps[n] = min([x for x in lap_times[n]])

            #sector_bests[n][0] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 2 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
            #sector_bests[n][1] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 3 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])
            #sector_bests[n][2] = min([float(x[186+i*9]) for x in self.replay.telemetry_data if int(x[185+i*9]) & int('111', 2) == 1 and float(x[186+i*9]) != -123.0 and int(x[183+i*9]) & int('10000000', 2) == 0])

        #Add in DNFs to the classification.
        in_classification = [n for _, n, *rest in self.classification]
        participant_data = self.replay.update_participants(deque(self.replay.participant_configurations))
        for n in sorted(laps_finished, key=laps_finished.get, reverse=True):
            if n not in in_classification:
                dnf_data = [x for x in participant_data if x[1] == n][0]
                self.classification.append(("DNF", dnf_data[1], dnf_data[2], dnf_data[3], "-1", laps_finished[n]))

        columnHeadings = [("Pos.", "Driver", "Team", "Car", "Laps", "Time", "Best Lap", "Best S1", "Best S2", "Best S3", "Points")]
        
        if len(self.replay.point_structure) < 17:
            self.replay.point_structure += [0] * (17-len(self.replay.point_structure))

        #self.classification = [(str(p), n, t, c, str(l), self.format_time(sum(lap_times[n])), "{:.2f}".format(float(min(lap_times[n]))), "{:.2f}".format(float(sector_bests[n][0])), "{:.2f}".format(float(sector_bests[n][1])), "{:.2f}".format(float(sector_bests[n][2])), str(self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personal_best_laps if isinstance(x, float)]) == personal_best_laps[n] else self.replay.point_structure[p])) for p, n, t, c, i, l in self.classification[:16]]
        self.classification = [(str(p), n, t, c, str(l), self.format_time(sum(lap_times[n])), self.format_time(float(min(valid_lap_times[n]))) if len(valid_lap_times[n]) else "", self.format_time(float(sector_bests[n][0])) if sector_bests[n][0] != -1 else "", self.format_time(float(sector_bests[n][1])) if sector_bests[n][1] != -1 else "", self.format_time(float(sector_bests[n][2])) if sector_bests[n][2] != -1 else "", "0" if p == "DNF" else "0" if l < 1 else str(self.replay.point_structure[p]+self.replay.point_structure[0] if min([x for x in personal_best_laps.values() if isinstance(x, float)]) == personal_best_laps[n] else self.replay.point_structure[p])) for p, n, t, c, i, l in self.classification[:16]]
        columnHeadings = [tuple([x if len([y[i] for y in self.classification if len(y[i])]) else "" for i, x in enumerate(*columnHeadings)])]
        self.classification = columnHeadings+self.classification

        self.widths = [max([self.replay.font.getsize(x[i])[0] for x in self.classification]) for i in range(len(self.classification[0]))]
        self.widths.append(sum(self.widths))

        heights = [max([self.replay.font.getsize(x[i])[1] for x in self.classification]) for i in range(len(self.classification[0]))]
        self.data_height = max(heights)
        heights = [self.data_height for x in self.classification]
        heights.append(self.replay.heading_font.getsize(self.replay.heading_text)[1])
        heights.append(self.replay.font.getsize(self.replay.subheading_text)[1])

        header_height = self.replay.heading_font.getsize(self.replay.heading_text)[1]+self.replay.font.getsize(self.replay.subheading_text)[1]+self.replay.margin*2

        text_width = max(self.widths[-1]+self.replay.column_margin*(len([x for x in self.widths[:-1] if x != 0])-1), self.replay.heading_font.getsize(self.replay.heading_text)[0]+self.replay.column_margin+header_height, self.replay.font.getsize(self.replay.subheading_text)[0]+self.replay.column_margin+header_height)
        text_height = sum(heights)+self.replay.margin*len(heights)-1

        heading_material = Image.new('RGBA', (text_width+self.replay.margin*2, header_height), self.replay.heading_color)

        if len(self.replay.series_logo):
            series_logo = Image.open(self.replay.series_logo).resize((heading_material.height, heading_material.height))
            heading_material.paste(series_logo, (heading_material.width-series_logo.width, 0))

        self.material = Image.new('RGBA', (text_width+self.replay.margin*2, text_height))
        self.material.paste(heading_material, (0, 0))
        
        yPos = header_height
        for i, r in enumerate(self.classification):
            if i % 2:
                self.material_color = (255, 255, 255)
            else:
                self.material_color = (192, 192, 192)

            row_material = Image.new('RGBA', (text_width+self.replay.margin*2, self.data_height+self.replay.margin), self.material_color)
            self.material.paste(row_material, (0, yPos))
            yPos += self.data_height+self.replay.margin

        return self.material if bgOnly else self._write_data()

    def to_frame(self):
        return super(Results, self).to_frame()
    
    def make_mask(self):
        return super(Results, self).make_mask()

if __name__ == '__main__':
    print('Subclass:', issubclass(Results, StaticBase))
    print('Instance:', isinstance(Results(0), StaticBase))
