"""
Provides classes for the storage and management of participant data.
"""

class ParticipantData():
    """
    Represents data for all participants in the race field.
    """

    def __init__(self):
        self._participants = set()

    def update_drivers(self, telemetry_data, participant_data):
        self._participants = {Driver(
            telemetry_data,
            participant_index,
            participant_name) for participant_index, \
                participant_name, *reset in participant_data}

    @property
    def drivers_by_position(self):
        return sorted(
            self._participants,
            key=lambda x: x.race_position)

class Driver():
    """
    Represents a race participant.
    """

    def __init__(
            self,
            telemetry_data,
            participant_index,
            participant_name):
        offset = int(participant_index)*9
        self.race_position = int(telemetry_data[182+offset]) & \
            int('01111111', 2)
        self.name = participant_name
        self.progress = float(telemetry_data[181+offset])/\
            float(telemetry_data[682]) \
            if float(telemetry_data[181+offset]) <= \
                float(telemetry_data[682]) \
            else float(0)
        self.participant_index = int(participant_index)
        self.sector = int(telemetry_data[185+offset]) & \
            int('111', 2)
        self.last_sector_time = float(telemetry_data[186+offset])
        self.elapsed_time = float(telemetry_data[-1])
        self.laps_completed = int(telemetry_data[183+offset]) & \
            int('01111111', 2)
        self.valid_lap = int(telemetry_data[183+offset]) & \
            int('10000000', 2)
        self.current_lap = int(telemetry_data[184+offset])
        self.current_position = (
            float(telemetry_data[178+offset]),
            float(telemetry_data[180+offset]))
