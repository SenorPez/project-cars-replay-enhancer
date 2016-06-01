"""
Provides classes for race standings.
"""

class RaceStandings():
    """
    Class to hold and manage race standings.
    """
    
    def __init__(self, telemetry_data, participant_data):
        self.standings = sorted({(
            int(telemetry_data[182+i*9]) & int('01111111', 2),
            name,
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
            ) for i, name, *rest in participant_data})

    def get_standings(self):
        return self.standings
