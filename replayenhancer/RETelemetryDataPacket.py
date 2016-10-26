"""
Provides a class for the Telemetry Data packets output by
Project CARS.

Customized for use by the Project CARS Replay Enhancer.
"""

from hashlib import md5

from replayenhancer.TelemetryDataPacket import \
    ParticipantInfo, TelemetryDataPacket


class REParticipantInfo(ParticipantInfo):
    # pylint: disable=super-init-not-called
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-statements
    """
    Creates an object containing the participant info from the
    telemetry data.

    Customized for use by the Project CARS Replay Enhancer.
    We do not call the parent constructor.
    """
    def __init__(self, unpacked_data):
        self._world_position = list()
        for _ in range(3):
            self._world_position.append(int(unpacked_data.popleft()))
        self._race_position = int(unpacked_data.popleft())
        self._laps_completed = int(unpacked_data.popleft())
        self.current_lap = int(unpacked_data.popleft())
        self._sector = int(unpacked_data.popleft())
        self.last_sector_time = float(unpacked_data.popleft())


class RETelemetryDataPacket(TelemetryDataPacket):
    # pylint: disable=super-init-not-called
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-statements
    """
    Creates an object from a telemetry data packet.

    The telemetry data packet has a length of 1367 and is packet type
    0.

    Customized for use by the Project CARS Replay Enhancer.
    We do not call the parent constructor.
    """

    def __init__(self, packet_data):
        self.data_hash = md5(packet_data).hexdigest()
        unpacked_data = self._unpack_data(packet_data)

        self.build_version_number = int(unpacked_data.popleft())

        self._test_packet_type(unpacked_data.popleft())

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
    def _packet_string(self):
        """
        Original definition:
        _packet_string = "HB"
        _packet_string += "B"
        _packet_string += "bb"
        _packet_string += "BBbBB"
        _packet_string += "B"
        _packet_string += "21f"
        _packet_string += "H"
        _packet_string += "B"
        _packet_string += "B"
        _packet_string += "hHhHHBBBBBbffHHBBbB"
        _packet_string += "22f"
        _packet_string += "8B12f8B8f12B4h20H16f4H"
        _packet_string += "2f"
        _packet_string += "2B"
        _packet_string += "bbBbbb"

        _packet_string += "hhhHBBBBf"*56

        _packet_string += "fBBB"
        """
        packet_string = "HB"
        packet_string += "B"  # Game states
        packet_string += "bb"  # Participant info
        packet_string += "4xB"  # Unfiltered input
        packet_string += "B"  # Event Information
        packet_string += "8xf12xf56x"  # Timings
        packet_string += "2x"  # Joypad
        packet_string += "x"  # Flags
        packet_string += "x"  # Pit info
        packet_string += "10x6x8x4x4x"  # Car state
        packet_string += "88x"
        packet_string += "228x"  # Wheels / tyres
        packet_string += "8x"  # Extras
        packet_string += "2x"  # Car damage
        packet_string += "6x"  # Weather
        packet_string += "hhh2xBBBBf"*56  # Participant info
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
        # TODO: Time
        return int(self.laps_in_event)

    @property
    def event_type(self):
        """Returns 'laps' or 'time'."""
        if isinstance(self.event_duration, int):
            return 'laps'
        else:
            return 'time'

    @property
    def drivers_by_position(self):
        """Returns drivers, sorted by race position."""
        return sorted(
            self.drivers_by_index,
            key=lambda x: x.race_position)

    @property
    def drivers_by_index(self):
        """Returns drivers, sorted by their index."""
        return [x for x in self.participant_info if x.is_active]\
            [:self.num_participants]

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
            [
                x.race_position
                for x in self.participant_info
                if x.is_active])
