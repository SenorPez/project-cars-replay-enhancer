"""
Provides a class for the Telemetry Data packets output by
Project CARS.

Customized for use by the Project CARS Replay Enhancer.
"""

from TelemetryDataPacket import ParticipantInfo, TelemetryDataPacket

class REParticipantInfo(ParticipantInfo):
    # pylint: disable=super-init-not-called
    """
    Creates an object containing the participant info from the
    telemetry data.

    Customized for use by the Project CARS Replay Enhancer.
    We do not call the parent constructor.
    """
    def __init__(self, unpacked_data):
        self.index = None
        self.name = None
        self.viewed = False

        self._race_position = int(unpacked_data.popleft())
        self._laps_completed = int(unpacked_data.popleft())
        self.current_lap = int(unpacked_data.popleft())
        self._sector = int(unpacked_data.popleft())
        self.last_sector_time = float(unpacked_data.popleft())

class RETelemetryDataPacket(TelemetryDataPacket):
    # pylint: disable=super-init-not-called
    """
    Creates an object from a telemetry data packet.

    The telemetry data packet has a length of 1367 and is packet type
    0.

    Customized for use by the Project CARS Replay Enhancer.
    We do not call the parent constructor.
    """

    _last_time = None
    _elapsed_time = 0.0
    _add_time = 0.0

    def __init__(self, packet_data):
        # pylint: disable=too-many-instance-attributes
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        unpacked_data = self.unpack_data(packet_data)

        self.build_version_number = int(unpacked_data.popleft())

        self.test_packet_type(unpacked_data.popleft())

        self._game_session_state = int(unpacked_data.popleft())

        self.viewed_participant_index = int(unpacked_data.popleft())
        self.num_participants = int(unpacked_data.popleft())

        self._race_state_flags = int(unpacked_data.popleft())

        self.laps_in_event = int(unpacked_data.popleft())

        self.current_time = float(unpacked_data.popleft())
        self.event_time_remaining = float(unpacked_data.popleft())

        self.participant_info = list()
        for _ in range(56):
            self.participant_info.append(REParticipantInfo(
                unpacked_data))
        self.participant_info[self.viewed_participant_index].\
            viewed = True

        self.track_length = float(unpacked_data.popleft())

    @property
    def packet_string(self):
        """
        Original definition:
        packet_string = "HB"
        packet_string += "B"
        packet_string += "bb"
        packet_string += "BBbBB"
        packet_string += "B"
        packet_string += "21f"
        packet_string += "H"
        packet_string += "B"
        packet_string += "B"
        packet_string += "hHhHHBBBBBbffHHBBbB"
        packet_string += "22f"
        packet_string += "8B12f8B8f12B4h20H16f4H"
        packet_string += "2f"
        packet_string += "2B"
        packet_string += "bbBbbb"

        packet_string += "hhhHBBBBf"*56

        packet_string += "fBBB"
        """
        packet_string = "HB"
        packet_string += "B" #Game states
        packet_string += "bb" #Participant info
        packet_string += "4xB" #Unfiltered infput
        packet_string += "B" #Event Information
        packet_string += "8xf12xf56x" #Timings
        packet_string += "2x" #Joypad
        packet_string += "x" #Flags
        packet_string += "x" #Pit info
        packet_string += "10x6x8x4x4x" #Car state
        packet_string += "88x"
        packet_string += "228x" #Wheels / tyres
        packet_string += "8x" #Extras
        packet_string += "2x" #Car damage
        packet_string += "6x" #Weather
        packet_string += "2x2x2x2xBBBBf"*56 #Participant info
        packet_string += "fxxx"

        return packet_string

    def __str__(self):
        return "RETelemetryData"

    def set_name(self, name, index):
        """Sets the name for the specified index."""
        self.participant_info[index].name = name
        self.participant_info[index].viewed = \
            index == self.viewed_participant_index

    @property
    def event_duration(self):
        """Returns the event duration, in laps or time."""
        #TODO: Time
        return self.laps_in_event

    @property
    def drivers_by_position(self):
        """Returns drivers, srted by race position."""
        return sorted(
            [x for x in self.participant_info if x.is_active],
            key=lambda x: x.race_position)

    @property
    def drivers_by_index(self):
        """Returns drivers, sorted by their index."""
        return [x for x in self.participant_info if x.is_active]

    @property
    def leader_lap(self):
        """Returns the leader's current lap."""
        return min(
            self.drivers_by_position[0].current_lap,
            self.event_duration)

    @property
    def last_place(self):
        """Returns the last place race position."""
        return max(
            [x.race_position \
                for x in self.participant_info \
                if x.is_active])


    def previous_packet(self, packet):
        """
        Takes the previous packet, to calculate the elapsed time.
        This is a set-only property.
        """
        if self.current_time == -1.0:
            self._elapsed_time = 0.0
            self._add_time = 0.0
        else:
            self._add_time = packet.add_time
            if packet.current_time > self.current_time:
                self._add_time += packet.current_time

            self._elapsed_time = self._add_time + self.current_time
    previous_packet = property(None, previous_packet)

    @property
    def add_time(self):
        """
        Returns the time adjustment, used for calculating elapsed
        time.
        """
        return self._add_time

    @property
    def elapsed_time(self):
        """Returns the calculated elapsed time."""
        return self._elapsed_time
