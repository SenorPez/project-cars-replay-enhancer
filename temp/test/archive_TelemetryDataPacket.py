"""
Tests TelemetryDataPacket.py
"""

import unittest
from struct import pack
from unittest.mock import sentinel

from replayenhancer.TelemetryDataPacket \
    import TelemetryDataPacket


def make_char(value):
    while value > 127:
        value //= 2
    return value


def make_short(value):
    while value > 16383:
        value //= 2
    return value


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid Telemetry Data Packet.
    """
    expected_build_version = make_short(abs(id(sentinel.build_version)))
    expected_packet_type = 0

    expected_game_session_state = make_char(abs(id(sentinel.game_session_state)))

    expected_viewed_participant_index = make_char(abs(id(sentinel.viewed_participant_index)))
    expected_num_participants = make_char(abs(id(sentinel.num_participants)))

    expected_unfiltered_throttle = make_char(abs(id(sentinel.unfiltered_throttle)))
    expected_unfiltered_brake = make_char(abs(id(sentinel.unfiltered_brake)))
    expected_unfiltered_steering = make_char(abs(id(sentinel.unfiltered_steering)))
    expected_unfiltered_clutch = make_char(abs(id(sentinel.unfiltered_clutch)))
    expected_race_state_flags = make_char(abs(id(sentinel.race_state_flags)))

    expected_laps_in_event = make_char(abs(id(sentinel.laps_in_event)))

    expected_best_lap_time = abs(float(id(sentinel.best_lap_time)))
    expected_last_lap_time = abs(float(id(sentinel.last_lap_time)))
    expected_current_time = abs(float(id(sentinel.current_time)))
    expected_split_time_ahead = abs(float(id(sentinel.split_time_ahead)))
    expected_split_time_behind = abs(float(id(sentinel.split_time_behind)))
    expected_split_time = abs(float(id(sentinel.split_time)))
    expected_event_time_remaining = abs(float(id(sentinel.event_time_remaining)))
    expected_personal_fastest_lap_time = abs(float(id(sentinel.personal_fastest_lap_time)))
    expected_world_fastest_lap_time = abs(float(id(sentinel.world_fastest_lap_time)))
    expected_current_sector_1_time = abs(float(id(sentinel.current_sector_1_time)))
    expected_current_sector_2_time = abs(float(id(sentinel.current_sector_2_time)))
    expected_current_sector_3_time = abs(float(id(sentinel.current_sector_3_time)))
    expected_fastest_sector_1_time = abs(float(id(sentinel.fastest_sector_1_time)))
    expected_fastest_sector_2_time = abs(float(id(sentinel.fastest_sector_2_time)))
    expected_fastest_sector_3_time = abs(float(id(sentinel.fastest_sector_3_time)))
    expected_personal_fastest_sector_1_time = abs(float(id(sentinel.personal_fastest_sector_1_time)))
    expected_personal_fastest_sector_2_time = abs(float(id(sentinel.personal_fastest_sector_2_time)))
    expected_personal_fastest_sector_3_time = abs(float(id(sentinel.personal_fastest_sector_3_time)))
    expected_world_fastest_sector_1_time = abs(float(id(sentinel.world_fastest_sector_1_time)))
    expected_world_fastest_sector_2_time = abs(float(id(sentinel.world_fastest_sector_2_time)))
    expected_world_fastest_sector_3_time = abs(float(id(sentinel.world_fastest_sector_3_time)))
    
    expected_joy_pad = make_short(abs(id(sentinel.joy_pad)))
    
    expected_highest_flag = make_char(abs(id(sentinel.highest_flag)))

    expected_pit_mode_schedule = make_char(abs(id(sentinel.pit_mode_schedule)))

    expected_oil_temp = make_short(abs(id(sentinel.oil_temp)))
    expected_oil_pressure = make_short(abs(id(sentinel.oil_pressure)))
    expected_water_temp = make_short(abs(id(sentinel.water_temp)))
    expected_water_pressure = make_short(abs(id(sentinel.water_pressure)))
    expected_fuel_pressure = make_short(abs(id(sentinel.fuel_pressure)))
    expected_car_flags = make_char(abs(id(sentinel.car_flags)))
    expected_fuel_capacity = make_char(abs(id(sentinel.fuel_capacity)))
    expected_brake = make_char(abs(id(sentinel.brake)))
    expected_throttle = make_char(abs(id(sentinel.throttle)))
    expected_clutch = make_char(abs(id(sentinel.clutch)))
    expected_steering = make_char(abs(id(sentinel.steering)))
    expected_fuel_level = abs(float(id(sentinel.fuel_level)))
    expected_speed = abs(float(id(sentinel.speed)))
    expected_rpm = make_short(abs(id(sentinel.rpm)))
    expected_max_rpm = make_short(abs(id(sentinel.max_rpm)))
    expected_gear_num_gears = make_char(abs(id(sentinel.gear_num_gears)))
    expected_boost_amount = make_char(abs(id(sentinel.boost_amount)))
    expected_enforced_pit_stop_lap = make_char(abs(id(sentinel.enforced_pit_stop_lap)))
    expected_crash_state = make_char(abs(id(sentinel.crash_state)))

    expected_odometer = abs(float(id(sentinel.odometer)))
    expected_orientation = list()
    expected_orientation.extend([abs(float(id(sentinel.orientation))) for _ in range(3)])
    expected_local_velocity = list()
    expected_local_velocity.extend([abs(float(id(sentinel.local_velocity))) for _ in range(3)])
    expected_world_velocity = list()
    expected_world_velocity.extend([abs(float(id(sentinel.world_velocity))) for _ in range(3)])
    expected_angular_velocity = list()
    expected_angular_velocity.extend([abs(float(id(sentinel.angular_velocity))) for _ in range(3)])
    expected_local_acceleration = list()
    expected_local_acceleration.extend([abs(float(id(sentinel.local_acceleration))) for _ in range(3)])
    expected_world_acceleration = list()
    expected_world_acceleration.extend([abs(float(id(sentinel.world_acceleration))) for _ in range(3)])
    expected_extents_centre = list()
    expected_extents_centre.extend([abs(float(id(sentinel.extents_centre))) for _ in range(3)])

    expected_tyre_flags = list()
    expected_tyre_flags.extend([make_char(abs(id(sentinel.tyre_flags))) for _ in range(4)])
    expected_terrain = list()
    expected_terrain.extend([make_char(abs(id(sentinel.terrain))) for _ in range(4)])
    expected_tyre_y = list()
    expected_tyre_y.extend([abs(float(id(sentinel.tyre_y))) for _ in range(4)])
    expected_tyre_rps = list()
    expected_tyre_rps.extend([abs(float(id(sentinel.tyre_rps))) for _ in range(4)])
    expected_tyre_slip_speed = list()
    expected_tyre_slip_speed.extend([abs(float(id(sentinel.tyre_slip_speed))) for _ in range(4)])
    expected_tyre_temp = list()
    expected_tyre_temp.extend([make_char(abs(id(sentinel.tyre_temp))) for _ in range(4)])
    expected_tyre_grip = list()
    expected_tyre_grip.extend([make_char(abs(id(sentinel.tyre_grip))) for _ in range(4)])
    expected_tyre_height_above_ground = list()
    expected_tyre_height_above_ground.extend([abs(float(id(sentinel.tyre_height_above_ground))) for _ in range(4)])
    expected_tyre_lateral_stiffness = list()
    expected_tyre_lateral_stiffness.extend([abs(float(id(sentinel.tyre_lateral_stiffness))) for _ in range(4)])
    expected_tyre_wear = list()
    expected_tyre_wear.extend([make_char(abs(id(sentinel.tyre_wear))) for _ in range(4)])
    expected_brake_damage = list()
    expected_brake_damage.extend([make_char(abs(id(sentinel.brake_damage))) for _ in range(4)])
    expected_suspension_damage = list()
    expected_suspension_damage.extend([make_char(abs(id(sentinel.suspension_damage))) for _ in range(4)])
    expected_brake_temp = list()
    expected_brake_temp.extend([make_short(abs(id(sentinel.brake_temp))) for _ in range(4)])
    expected_tyre_tread_temp = list()
    expected_tyre_tread_temp.extend([make_short(abs(id(sentinel.tyre_tread_temp))) for _ in range(4)])
    expected_tyre_layer_temp = list()
    expected_tyre_layer_temp.extend([make_short(abs(id(sentinel.tyre_layer_temp))) for _ in range(4)])
    expected_tyre_carcass_temp = list()
    expected_tyre_carcass_temp.extend([make_short(abs(id(sentinel.tyre_carcass_temp))) for _ in range(4)])
    expected_tyre_rim_temp = list()
    expected_tyre_rim_temp.extend([make_short(abs(id(sentinel.tyre_rim_temp))) for _ in range(4)])
    expected_tyre_internal_air_temp = list()
    expected_tyre_internal_air_temp.extend([make_short(abs(id(sentinel.tyre_internal_air_temp))) for _ in range(4)])
    expected_wheel_local_position_y = list()
    expected_wheel_local_position_y.extend([abs(float(id(sentinel.wheel_local_position_y))) for _ in range(4)])
    expected_ride_height = list()
    expected_ride_height.extend([abs(float(id(sentinel.ride_height))) for _ in range(4)])
    expected_suspension_travel = list()
    expected_suspension_travel.extend([abs(float(id(sentinel.suspension_travel))) for _ in range(4)])
    expected_suspension_velocity = list()
    expected_suspension_velocity.extend([abs(float(id(sentinel.suspension_velocity))) for _ in range(4)])
    expected_air_pressure = list()
    expected_air_pressure.extend([make_short(abs(id(sentinel.air_pressure))) for _ in range(4)])

    expected_engine_speed = abs(float(id(sentinel.engine_speed)))
    expected_engine_torque = abs(float(id(sentinel.engine_torque)))

    expected_aero_damage = make_char(abs(id(sentinel.aero_damage)))
    expected_engine_damage = make_char(abs(id(sentinel.engine_damage)))

    expected_ambient_temperature = make_char(abs(id(sentinel.ambient_temperature)))
    expected_track_temperature = make_char(abs(id(sentinel.track_temperature)))
    expected_rain_density = make_char(abs(id(sentinel.rain_density)))
    expected_wind_speed = make_char(abs(id(sentinel.wind_speed)))
    expected_wind_direction_x = make_char(abs(id(sentinel.wind_direction_x)))
    expected_wind_direction_y = make_char(abs(id(sentinel.wind_direction_y)))

    expected_world_position = list()
    expected_world_position.extend([make_short(abs(id(sentinel.world_position))) for _ in range(3)])
    expected_current_lap_distance = make_short(abs(id(sentinel.current_lap_distance)))
    expected_race_position = make_char(abs(id(sentinel.race_position)))
    expected_laps_completed = make_char(abs(id(sentinel.laps_completed)))
    expected_current_lap = make_char(abs(id(sentinel.current_lap)))
    expected_sector = make_char(abs(id(sentinel.sector)))
    expected_last_sector_time = abs(float(id(sentinel.last_sector_time)))

    expected_track_length = abs(float(id(sentinel.track_length)))
    expected_wings = list()
    expected_wings.extend([make_char(abs(id(sentinel.wings))) for _ in range(2)])
    expected_dpad = make_char(abs(id(sentinel.dpad)))

    packet_length = 1367
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

    packet_string += "hhhHBBBBf" * 56

    packet_string += "fBBB"

    test_data = list()
    test_data.append(expected_build_version)
    test_data.append(expected_packet_type)

    test_data.append(expected_game_session_state)

    test_data.append(expected_viewed_participant_index)
    test_data.append(expected_num_participants)

    test_data.append(expected_unfiltered_throttle)
    test_data.append(expected_unfiltered_brake)
    test_data.append(expected_unfiltered_steering)
    test_data.append(expected_unfiltered_clutch)
    test_data.append(expected_race_state_flags)

    test_data.append(expected_laps_in_event)

    test_data.append(expected_best_lap_time)
    test_data.append(expected_last_lap_time)
    test_data.append(expected_current_time)
    test_data.append(expected_split_time_ahead)
    test_data.append(expected_split_time_behind)
    test_data.append(expected_split_time)
    test_data.append(expected_event_time_remaining)
    test_data.append(expected_personal_fastest_lap_time)
    test_data.append(expected_world_fastest_lap_time)
    test_data.append(expected_current_sector_1_time)
    test_data.append(expected_current_sector_2_time)
    test_data.append(expected_current_sector_3_time)
    test_data.append(expected_fastest_sector_1_time)
    test_data.append(expected_fastest_sector_2_time)
    test_data.append(expected_fastest_sector_3_time)
    test_data.append(expected_personal_fastest_sector_1_time)
    test_data.append(expected_personal_fastest_sector_2_time)
    test_data.append(expected_personal_fastest_sector_3_time)
    test_data.append(expected_world_fastest_sector_1_time)
    test_data.append(expected_world_fastest_sector_2_time)
    test_data.append(expected_world_fastest_sector_3_time)

    test_data.append(expected_joy_pad)

    test_data.append(expected_highest_flag)

    test_data.append(expected_pit_mode_schedule)

    test_data.append(expected_oil_temp)
    test_data.append(expected_oil_pressure)
    test_data.append(expected_water_temp)
    test_data.append(expected_water_pressure)
    test_data.append(expected_fuel_pressure)
    test_data.append(expected_car_flags)
    test_data.append(expected_fuel_capacity)
    test_data.append(expected_brake)
    test_data.append(expected_throttle)
    test_data.append(expected_clutch)
    test_data.append(expected_steering)
    test_data.append(expected_fuel_level)
    test_data.append(expected_speed)
    test_data.append(expected_rpm)
    test_data.append(expected_max_rpm)
    test_data.append(expected_gear_num_gears)
    test_data.append(expected_boost_amount)
    test_data.append(expected_enforced_pit_stop_lap)
    test_data.append(expected_crash_state)

    test_data.append(expected_odometer)
    test_data.extend(expected_orientation)
    test_data.extend(expected_local_velocity)
    test_data.extend(expected_world_velocity)
    test_data.extend(expected_angular_velocity)
    test_data.extend(expected_local_acceleration)
    test_data.extend(expected_world_acceleration)
    test_data.extend(expected_extents_centre)

    test_data.extend(expected_tyre_flags)
    test_data.extend(expected_terrain)
    test_data.extend(expected_tyre_y)
    test_data.extend(expected_tyre_rps)
    test_data.extend(expected_tyre_slip_speed)
    test_data.extend(expected_tyre_temp)
    test_data.extend(expected_tyre_grip)
    test_data.extend(expected_tyre_height_above_ground)
    test_data.extend(expected_tyre_lateral_stiffness)
    test_data.extend(expected_tyre_wear)
    test_data.extend(expected_brake_damage)
    test_data.extend(expected_suspension_damage)
    test_data.extend(expected_brake_temp)
    test_data.extend(expected_tyre_tread_temp)
    test_data.extend(expected_tyre_layer_temp)
    test_data.extend(expected_tyre_carcass_temp)
    test_data.extend(expected_tyre_rim_temp)
    test_data.extend(expected_tyre_internal_air_temp)
    test_data.extend(expected_wheel_local_position_y)
    test_data.extend(expected_ride_height)
    test_data.extend(expected_suspension_travel)
    test_data.extend(expected_suspension_velocity)
    test_data.extend(expected_air_pressure)

    test_data.append(expected_engine_speed)
    test_data.append(expected_engine_torque)

    test_data.append(expected_aero_damage)
    test_data.append(expected_engine_damage)

    test_data.append(expected_ambient_temperature)
    test_data.append(expected_track_temperature)
    test_data.append(expected_rain_density)
    test_data.append(expected_wind_speed)
    test_data.append(expected_wind_direction_x)
    test_data.append(expected_wind_direction_y)

    for _ in range(56):
        test_data.extend(expected_world_position)
        test_data.append(expected_current_lap_distance)
        test_data.append(expected_race_position)
        test_data.append(expected_laps_completed)
        test_data.append(expected_current_lap)
        test_data.append(expected_sector)
        test_data.append(expected_last_sector_time)

    test_data.append(expected_track_length)
    test_data.extend(expected_wings)
    test_data.append(expected_dpad)

    test_binary_data = pack(packet_string, *test_data)

    def test_init(self):
        instance = TelemetryDataPacket(self.test_binary_data)
        expected_result = TelemetryDataPacket
        self.assertIsInstance(instance, expected_result)

    def init_wrong_packet_type(self):
        test_data = self.test_data
        test_data[1] = 1  # Set incorrect packet type

        test_binary_data = pack(self.packet_string, *test_data)

        with self.assertRaises(ValueError):
            TelemetryDataPacket(test_binary_data)



