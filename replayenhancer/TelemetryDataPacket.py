"""
Provides a class for the Telemetry Data packets output by
Project CARS
"""

from hashlib import md5

from replayenhancer.Packet import Packet


class ParticipantInfo:
    """
    Creates an object containing the participant info from the
    telemetry data.
    """
    def __init__(self, unpacked_data):
        self._world_position = list()
        for _ in range(3):
            self._world_position.append(int(unpacked_data.popleft()))

        self.current_lap_distance = int(unpacked_data.popleft())
        self._race_position = int(unpacked_data.popleft())
        self._laps_completed = int(unpacked_data.popleft())
        self.current_lap = int(unpacked_data.popleft())
        self._sector = int(unpacked_data.popleft())
        self.last_sector_time = float(unpacked_data.popleft())

    @property
    def world_position(self):
        """Returns world position (high accuracy for x and z)."""
        world_position = [float(x) for x in self._world_position]
        world_position[0] += float(
            ((self._sector & int('00011000', 2)) >> 3) / 4)
        world_position[2] += float(
            ((self._sector & int('01100000', 2)) >> 5) / 4)

        return world_position

    @property
    def is_active(self):
        """Determines if the Participant is active."""
        return self._race_position & int('10000000', 2)

    @property
    def race_position(self):
        """Determines the Participant's race position."""
        return self._race_position & int('01111111', 2)

    @property
    def invalid_lap(self):
        """
        Determines if the Participant's lap is valid.

        Project CARS flags the start of the race (Sector 3, before you
        reach the start-finish line to begin the 'first lap proper')
        as invalid, so we need to deal with that. Dumb.

        That will have sector equal to 3 (since you start the race
        in Sector 3) and a previous sector time of -123 (since you
        don't have a previous sector time).
        """
        invalid_lap = self._laps_completed & int('10000000', 2)

        if invalid_lap and \
                self.sector == 3 and \
                self.last_sector_time == -123:
            return 0
        else:
            return invalid_lap

    @property
    def laps_completed(self):
        """Determines the laps completed by Participant."""
        return self._laps_completed & int('01111111', 2)

    @property
    def sector(self):
        """Determines the Participant's current sector."""
        return self._sector & int('00000111', 2)


class TelemetryDataPacket(Packet):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    """
    Creates an object from a telemetry data packet.

    The telemetry data packet has a length of 1367 and is packet type
    0.
    """
    def __init__(self, packet_data):
        self.data_hash = md5(packet_data).hexdigest()
        unpacked_data = self._unpack_data(packet_data)

        self.build_version_number = int(unpacked_data.popleft())

        self._test_packet_type(unpacked_data.popleft())

        self._game_session_state = int(unpacked_data.popleft())

        self.viewed_participant_index = int(unpacked_data.popleft())
        self.num_participants = int(unpacked_data.popleft())

        self.unfiltered_throttle = int(unpacked_data.popleft())
        self.unfiltered_brake = int(unpacked_data.popleft())
        self.unfiltered_steering = int(unpacked_data.popleft())
        self.unfiltered_clutch = int(unpacked_data.popleft())
        self._race_state_flags = int(unpacked_data.popleft())

        self.laps_in_event = int(unpacked_data.popleft())

        self.best_lap_time = float(unpacked_data.popleft())
        self.last_lap_time = float(unpacked_data.popleft())
        self.current_time = float(unpacked_data.popleft())
        self.split_time_ahead = float(unpacked_data.popleft())
        self.split_time_behind = float(unpacked_data.popleft())
        self.split_time = float(unpacked_data.popleft())
        self.event_time_remaining = float(unpacked_data.popleft())
        self.personal_fastest_lap_time = float(
            unpacked_data.popleft())
        self.world_fastest_lap_time = float(unpacked_data.popleft())
        self.current_s1_time = float(unpacked_data.popleft())
        self.current_s2_time = float(unpacked_data.popleft())
        self.current_s3_time = float(unpacked_data.popleft())
        self.fastest_s1_time = float(unpacked_data.popleft())
        self.fastest_s2_time = float(unpacked_data.popleft())
        self.fastest_s3_time = float(unpacked_data.popleft())
        self.personal_fastest_s1_time = float(
            unpacked_data.popleft())
        self.personal_fastest_s2_time = float(
            unpacked_data.popleft())
        self.personal_fastest_s3_time = float(
            unpacked_data.popleft())
        self.world_fastest_s1_time = float(unpacked_data.popleft())
        self.world_fastest_s2_time = float(unpacked_data.popleft())
        self.world_fastest_s3_time = float(unpacked_data.popleft())

        self.joypad = int(unpacked_data.popleft())

        self.highest_flag = int(unpacked_data.popleft())

        self.pit_mode_schedule = int(unpacked_data.popleft())

        self.oil_temp = int(unpacked_data.popleft())
        self.oil_pressure = int(unpacked_data.popleft())
        self.water_temp = int(unpacked_data.popleft())
        self.water_pressure = int(unpacked_data.popleft())
        self.fuel_pressure = int(unpacked_data.popleft())
        self.car_flags = int(unpacked_data.popleft())
        self.fuel_capacity = int(unpacked_data.popleft())
        self.brake = int(unpacked_data.popleft())
        self.throttle = int(unpacked_data.popleft())
        self.clutch = int(unpacked_data.popleft())
        self.steering = int(unpacked_data.popleft())
        self.fuel_level = float(unpacked_data.popleft())
        self.speed = float(unpacked_data.popleft())
        self.rpm = int(unpacked_data.popleft())
        self.max_rpm = int(unpacked_data.popleft())
        self.gear_num_gears = int(unpacked_data.popleft())
        self.boost_amount = int(unpacked_data.popleft())
        self.enforced_pit_stop_lap = int(unpacked_data.popleft())
        self.crash_state = int(unpacked_data.popleft())

        self.odometer = float(unpacked_data.popleft())
        self.orientation = list()
        self.local_velocity = list()
        self.world_velocity = list()
        self.angular_velocity = list()
        self.local_acceleration = list()
        self.world_acceleration = list()
        self.extents_centre = list()
        for _ in range(3):
            self.orientation.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.local_velocity.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.world_velocity.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.angular_velocity.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.local_acceleration.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.world_acceleration.append(float(
                unpacked_data.popleft()))
        for _ in range(3):
            self.extents_centre.append(float(
                unpacked_data.popleft()))

        self.tyre_flags = list()
        self.terrain = list()
        self.tyre_y = list()
        self.tyre_rps = list()
        self.tyre_slip_speed = list()
        self.tyre_temp = list()
        self.tyre_grip = list()
        self.tyre_height_above_ground = list()
        self.tyre_lateral_stiffness = list()
        self.tyre_wear = list()
        self.brake_damage = list()
        self.suspension_damage = list()
        self.brake_temp = list()
        self.tyre_tread_temp = list()
        self.tyre_layer_temp = list()
        self.tyre_carcass_temp = list()
        self.tyre_rim_temp = list()
        self.tyre_internal_air_temp = list()
        self.wheel_local_position_y = list()
        self.ride_height = list()
        self.suspension_travel = list()
        self.suspension_velocity = list()
        self.air_pressure = list()

        for _ in range(4):
            self.tyre_flags.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.terrain.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_y.append(float(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_rps.append(float(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_slip_speed.append(float(
                unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_temp.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_grip.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_height_above_ground.append(
                float(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_lateral_stiffness.append(float(
                unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_wear.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.brake_damage.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.suspension_damage.append(int(
                unpacked_data.popleft()))
        for _ in range(4):
            self.brake_temp.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_tread_temp.append(int(
                unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_layer_temp.append(int(
                unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_carcass_temp.append(int(
                unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_rim_temp.append(int(unpacked_data.popleft()))
        for _ in range(4):
            self.tyre_internal_air_temp.append(int(
                unpacked_data.popleft()))
        for _ in range(4):
            self.wheel_local_position_y.append(float(
                unpacked_data.popleft()))
        for _ in range(4):
            self.ride_height.append(float(unpacked_data.popleft()))
        for _ in range(4):
            self.suspension_travel.append(float(
                unpacked_data.popleft()))
        for _ in range(4):
            self.suspension_velocity.append(float(
                unpacked_data.popleft()))
        for _ in range(4):
            self.air_pressure.append(int(unpacked_data.popleft()))

        self.engine_speed = float(unpacked_data.popleft())
        self.engine_torque = float(unpacked_data.popleft())

        self.aero_damage = int(unpacked_data.popleft())
        self.engine_damage = int(unpacked_data.popleft())

        self.ambient_temperature = int(unpacked_data.popleft())
        self.track_temperature = int(unpacked_data.popleft())
        self.rain_density = int(unpacked_data.popleft())
        self.wind_speed = int(unpacked_data.popleft())
        self.wind_direction_x = int(unpacked_data.popleft())
        self.wind_direction_y = int(unpacked_data.popleft())

        self.participant_info = list()
        for _ in range(56):
            self.participant_info.append(ParticipantInfo(
                unpacked_data))

        self.track_length = float(unpacked_data.popleft())
        self.wings = list()
        for _ in range(2):
            self.wings.append(int(unpacked_data.popleft()))
        self.d_pad = int(unpacked_data.popleft())

    @property
    def packet_type(self):
        return 0

    @property
    def _packet_string(self):
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

        return packet_string

    def __str__(self):
        return "TelemetryDataPacket"

    @property
    def game_state(self):
        """Extracts and returns the game state."""
        return self._game_session_state & int('00001111', 2)

    @property
    def session_state(self):
        """Extracts and returns the session state."""
        return (self._game_session_state & int('11110000', 2)) >> 4

    @property
    def race_state(self):
        """Extracts and returns the race state."""
        return self._race_state_flags & int('00000111', 2)
