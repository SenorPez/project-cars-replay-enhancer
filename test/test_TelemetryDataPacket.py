"""
Tests TelemetryDataPacket.py
"""

import os
import struct
import sys
import unittest

from replayenhancer.TelemetryDataPacket \
    import TelemetryDataPacket, ParticipantInfo


class TestValidPacket(unittest.TestCase):
    """
    Unit tests for a valid Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata11'
    packet = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            cls.packet = TelemetryDataPacket(packet_data.read())

    @classmethod
    def tearDownClass(cls):
        del cls.packet

    def test_property_data_hash(self):
        self.assertEqual(
            self.packet.data_hash,
            "9ddd3e436527473165f0e80d214a6fcd")

    def test_property_build_version_number(self):
        self.assertIsInstance(self.packet.build_version_number, int)

    def test_property_game_state(self):
        self.assertIsInstance(self.packet.game_state, int)

    def test_property_session_state(self):
        self.assertIsInstance(self.packet.session_state, int)

    def test_property_viewed_participant_index(self):
        self.assertIsInstance(self.packet.viewed_participant_index, int)

    def test_property_num_participants(self):
        self.assertIsInstance(self.packet.num_participants, int)

    def test_property_unfiltered_throttle(self):
        self.assertIsInstance(self.packet.unfiltered_throttle, int)

    def test_property_unfiltered_brake(self):
        self.assertIsInstance(self.packet.unfiltered_brake, int)

    def test_property_unfiltered_steering(self):
        self.assertIsInstance(self.packet.unfiltered_steering, int)

    def test_property_unfiltered_clutch(self):
        self.assertIsInstance(self.packet.unfiltered_clutch, int)

    def test_property_race_state(self):
        self.assertIsInstance(self.packet.race_state, int)

    def test_property_laps_in_event(self):
        self.assertIsInstance(self.packet.laps_in_event, int)

    def test_property_best_lap_time(self):
        self.assertIsInstance(self.packet.best_lap_time, float)

    def test_property_last_lap_time(self):
        self.assertIsInstance(self.packet.last_lap_time, float)

    def test_property_current_time(self):
        self.assertIsInstance(self.packet.current_time, float)

    def test_property_split_time_ahead(self):
        self.assertIsInstance(self.packet.split_time_ahead, float)

    def test_property_split_time_behind(self):
        self.assertIsInstance(self.packet.split_time_behind, float)

    def test_property_split_time(self):
        self.assertIsInstance(self.packet.split_time, float)

    def test_property_event_time_remaining(self):
        self.assertIsInstance(self.packet.event_time_remaining, float)

    def test_property_personal_fastest_lap_time(self):
        self.assertIsInstance(
            self.packet.personal_fastest_lap_time,
            float)

    def test_property_world_fastest_lap_time(self):
        self.assertIsInstance(self.packet.world_fastest_lap_time, float)

    def test_property_current_s1_time(self):
        self.assertIsInstance(self.packet.current_s1_time, float)

    def test_property_current_s2_time(self):
        self.assertIsInstance(self.packet.current_s2_time, float)

    def test_property_current_s3_time(self):
        self.assertIsInstance(self.packet.current_s3_time, float)

    def test_property_fastest_s1_time(self):
        self.assertIsInstance(self.packet.fastest_s1_time, float)

    def test_property_fastest_s2_time(self):
        self.assertIsInstance(self.packet.fastest_s2_time, float)

    def test_property_fastest_s3_time(self):
        self.assertIsInstance(self.packet.fastest_s3_time, float)

    def test_property_personal_fastest_s1_time(self):
        self.assertIsInstance(
            self.packet.personal_fastest_s1_time,
            float)

    def test_property_personal_fastest_s2_time(self):
        self.assertIsInstance(
            self.packet.personal_fastest_s2_time,
            float)

    def test_property_personal_fastest_s3_time(self):
        self.assertIsInstance(
            self.packet.personal_fastest_s3_time,
            float)

    def test_property_world_fastest_s1_time(self):
        self.assertIsInstance(self.packet.world_fastest_s1_time, float)

    def test_property_world_fastest_s2_time(self):
        self.assertIsInstance(self.packet.world_fastest_s2_time, float)

    def test_property_world_fastest_s3_time(self):
        self.assertIsInstance(self.packet.world_fastest_s3_time, float)

    def test_property_joypad(self):
        self.assertIsInstance(self.packet.joypad, int)

    def test_property_highest_flag(self):
        self.assertIsInstance(self.packet.highest_flag, int)

    def test_property_pit_mode_schedule(self):
        self.assertIsInstance(self.packet.pit_mode_schedule, int)

    def test_property_oil_temp(self):
        self.assertIsInstance(self.packet.oil_temp, int)

    def test_property_oil_pressure(self):
        self.assertIsInstance(self.packet.oil_pressure, int)

    def test_property_water_temp(self):
        self.assertIsInstance(self.packet.water_temp, int)

    def test_property_water_pressure(self):
        self.assertIsInstance(self.packet.water_pressure, int)

    def test_property_fuel_pressure(self):
        self.assertIsInstance(self.packet.fuel_pressure, int)

    def test_property_car_flags(self):
        self.assertIsInstance(self.packet.car_flags, int)

    def test_property_fuel_capacity(self):
        self.assertIsInstance(self.packet.fuel_capacity, int)

    def test_property_brake(self):
        self.assertIsInstance(self.packet.brake, int)

    def test_property_throttle(self):
        self.assertIsInstance(self.packet.throttle, int)

    def test_property_clutch(self):
        self.assertIsInstance(self.packet.clutch, int)

    def test_property_steering(self):
        self.assertIsInstance(self.packet.steering, int)

    def test_property_fuel_level(self):
        self.assertIsInstance(self.packet.fuel_level, float)

    def test_property_speed(self):
        self.assertIsInstance(self.packet.speed, float)

    def test_property_rpm(self):
        self.assertIsInstance(self.packet.rpm, int)

    def test_property_max_rpm(self):
        self.assertIsInstance(self.packet.max_rpm, int)

    def test_property_gear_num_gears(self):
        self.assertIsInstance(self.packet.gear_num_gears, int)

    def test_property_boost_amount(self):
        self.assertIsInstance(self.packet.boost_amount, int)

    def test_property_enforced_pit_stop_lap(self):
        self.assertIsInstance(self.packet.enforced_pit_stop_lap, int)

    def test_property_crash_state(self):
        self.assertIsInstance(self.packet.crash_state, int)

    def test_property_odometer(self):
        self.assertIsInstance(self.packet.odometer, float)

    def test_property_orientation(self):
        self.assertIsInstance(self.packet.orientation, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_orientation_values(self):
        for value in self.packet.orientation:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_orientation_values_nosubtest(self):
        for value in self.packet.orientation:
            self.assertIsInstance(value, float)

    def test_property_local_velocity(self):
        self.assertIsInstance(self.packet.local_velocity, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_local_velocity_values(self):
        for value in self.packet.local_velocity:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_local_velocity_values_nosubtest(self):
        for value in self.packet.local_velocity:
            self.assertIsInstance(value, float)

    def test_property_world_velocity(self):
        self.assertIsInstance(self.packet.world_velocity, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_velocity_values(self):
        for value in self.packet.world_velocity:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_velocity_values_nosubtest(self):
        for value in self.packet.world_velocity:
            self.assertIsInstance(value, float)

    def test_property_angular_velocity(self):
        self.assertIsInstance(self.packet.angular_velocity, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_angular_velocity_values(self):
        for value in self.packet.angular_velocity:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_angular_velocity_values_nosubtest(self):
        for value in self.packet.angular_velocity:
            self.assertIsInstance(value, float)

    def test_property_local_acceleration(self):
        self.assertIsInstance(self.packet.local_acceleration, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_local_acceleration_values(self):
        for value in self.packet.local_acceleration:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_local_acceleration_values_nosubtest(self):
        for value in self.packet.local_acceleration:
            self.assertIsInstance(value, float)

    def test_property_world_acceleration(self):
        self.assertIsInstance(self.packet.world_acceleration, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_acceleration_values(self):
        for value in self.packet.world_acceleration:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_acceleration_values_nosubtest(self):
        for value in self.packet.world_acceleration:
            self.assertIsInstance(value, float)

    def test_property_extents_centre(self):
        self.assertIsInstance(self.packet.extents_centre, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_extents_centre_values(self):
        for value in self.packet.extents_centre:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_extents_centre_values_nosubtest(self):
        for value in self.packet.extents_centre:
            self.assertIsInstance(value, float)

    def test_property_tyre_flags(self):
        self.assertIsInstance(self.packet.tyre_flags, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_flags_values(self):
        for value in self.packet.tyre_flags:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_flags_values_nosubtest(self):
        for value in self.packet.tyre_flags:
            self.assertIsInstance(value, int)

    def test_property_terrain(self):
        self.assertIsInstance(self.packet.terrain, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_terrain_values(self):
        for value in self.packet.terrain:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_terrain_values_nosubtest(self):
        for value in self.packet.terrain:
            self.assertIsInstance(value, int)

    def test_property_tyre_y(self):
        self.assertIsInstance(self.packet.tyre_y, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_y_values(self):
        for value in self.packet.tyre_y:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_y_values_nosubtest(self):
        for value in self.packet.tyre_y:
            self.assertIsInstance(value, float)

    def test_property_tyre_rps(self):
        self.assertIsInstance(self.packet.tyre_rps, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_rps_values(self):
        for value in self.packet.tyre_rps:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_rps_values_nosubtest(self):
        for value in self.packet.tyre_rps:
            self.assertIsInstance(value, float)

    def test_property_tyre_slip_speed(self):
        self.assertIsInstance(self.packet.tyre_slip_speed, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_slip_speed_values(self):
        for value in self.packet.tyre_slip_speed:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_slip_speed_values_nosubtest(self):
        for value in self.packet.tyre_slip_speed:
            self.assertIsInstance(value, float)

    def test_property_tyre_temp(self):
        self.assertIsInstance(self.packet.tyre_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_temp_values(self):
        for value in self.packet.tyre_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_temp_values_nosubtest(self):
        for value in self.packet.tyre_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_grip(self):
        self.assertIsInstance(self.packet.tyre_grip, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_grip_values(self):
        for value in self.packet.tyre_grip:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_grip_values_nosubtest(self):
        for value in self.packet.tyre_grip:
            self.assertIsInstance(value, int)

    def test_property_tyre_height_above_ground(self):
        self.assertIsInstance(
            self.packet.tyre_height_above_ground,
            list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_height_above_ground_values(self):
        for value in self.packet.tyre_height_above_ground:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_height_above_ground_values_nosubtest(self):
        for value in self.packet.tyre_height_above_ground:
            self.assertIsInstance(value, float)

    def test_property_tyre_lateral_stiffness(self):
        self.assertIsInstance(self.packet.tyre_lateral_stiffness, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_lateral_stiffness_values(self):
        for value in self.packet.tyre_lateral_stiffness:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_lateral_stiffness_values_nosubtest(self):
        for value in self.packet.tyre_lateral_stiffness:
            self.assertIsInstance(value, float)

    def test_property_tyre_wear(self):
        self.assertIsInstance(self.packet.tyre_wear, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_wear_values(self):
        for value in self.packet.tyre_wear:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_wear_values_nosubtest(self):
        for value in self.packet.tyre_wear:
            self.assertIsInstance(value, int)

    def test_property_brake_damage(self):
        self.assertIsInstance(self.packet.brake_damage, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_brake_damage_values(self):
        for value in self.packet.brake_damage:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_brake_damage_values_nosubtest(self):
        for value in self.packet.brake_damage:
            self.assertIsInstance(value, int)

    def test_property_suspension_damage(self):
        self.assertIsInstance(self.packet.suspension_damage, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_suspension_damage_values(self):
        for value in self.packet.suspension_damage:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_suspension_damage_values_nosubtest(self):
        for value in self.packet.suspension_damage:
            self.assertIsInstance(value, int)

    def test_property_brake_temp(self):
        self.assertIsInstance(self.packet.brake_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_brake_temp_values(self):
        for value in self.packet.brake_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_brake_temp_values_nosubtest(self):
        for value in self.packet.brake_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_tread_temp(self):
        self.assertIsInstance(self.packet.tyre_tread_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_tread_temp_values(self):
        for value in self.packet.tyre_tread_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_tread_temp_values_nosubtest(self):
        for value in self.packet.tyre_tread_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_layer_temp(self):
        self.assertIsInstance(self.packet.tyre_layer_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_layer_temp_values(self):
        for value in self.packet.tyre_layer_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_layer_temp_values_nosubtest(self):
        for value in self.packet.tyre_layer_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_carcass_temp(self):
        self.assertIsInstance(self.packet.tyre_carcass_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_carcass_temp_values(self):
        for value in self.packet.tyre_carcass_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_carcass_temp_values_nosubtest(self):
        for value in self.packet.tyre_carcass_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_rim_temp(self):
        self.assertIsInstance(self.packet.tyre_rim_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_rim_temp_values(self):
        for value in self.packet.tyre_rim_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_rim_temp_values_nosubtest(self):
        for value in self.packet.tyre_rim_temp:
            self.assertIsInstance(value, int)

    def test_property_tyre_internal_air_temp(self):
        self.assertIsInstance(self.packet.tyre_internal_air_temp, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_tyre_internal_air_temp_values(self):
        for value in self.packet.tyre_internal_air_temp:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_tyre_internal_air_temp_values_nosubtest(self):
        for value in self.packet.tyre_internal_air_temp:
            self.assertIsInstance(value, int)

    def test_property_wheel_local_position_y(self):
        self.assertIsInstance(self.packet.wheel_local_position_y, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_wheel_local_position_y_values(self):
        for value in self.packet.wheel_local_position_y:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_wheel_local_position_y_values_nosubtest(self):
        for value in self.packet.wheel_local_position_y:
            self.assertIsInstance(value, float)

    def test_property_ride_height(self):
        self.assertIsInstance(self.packet.ride_height, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_ride_height_values(self):
        for value in self.packet.ride_height:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_ride_height_values_nosubtest(self):
        for value in self.packet.ride_height:
            self.assertIsInstance(value, float)

    def test_property_suspension_travel(self):
        self.assertIsInstance(self.packet.suspension_travel, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_suspension_travel_values(self):
        for value in self.packet.suspension_travel:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_suspension_travel_values_nosubtest(self):
        for value in self.packet.suspension_travel:
            self.assertIsInstance(value, float)

    def test_property_suspension_velocity(self):
        self.assertIsInstance(self.packet.suspension_velocity, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_suspension_velocity_values(self):
        for value in self.packet.suspension_velocity:
            with self.subTest(item=value):
                self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_suspension_velocity_values_nosubtest(self):
        for value in self.packet.suspension_velocity:
            self.assertIsInstance(value, float)

    def test_property_air_pressure(self):
        self.assertIsInstance(self.packet.air_pressure, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_air_pressure_values(self):
        for value in self.packet.air_pressure:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_air_pressure_values_nosubtest(self):
        for value in self.packet.air_pressure:
            self.assertIsInstance(value, int)

    def test_property_engine_speed(self):
        self.assertIsInstance(self.packet.engine_speed, float)

    def test_property_engine_torque(self):
        self.assertIsInstance(self.packet.engine_torque, float)

    def test_property_aero_damage(self):
        self.assertIsInstance(self.packet.aero_damage, int)

    def test_property_engine_damage(self):
        self.assertIsInstance(self.packet.engine_damage, int)

    def test_property_ambient_temperature(self):
        self.assertIsInstance(self.packet.ambient_temperature, int)

    def test_property_track_temperature(self):
        self.assertIsInstance(self.packet.track_temperature, int)

    def test_property_rain_density(self):
        self.assertIsInstance(self.packet.rain_density, int)

    def test_property_wind_speed(self):
        self.assertIsInstance(self.packet.wind_speed, int)

    def test_property_wind_direction_x(self):
        self.assertIsInstance(self.packet.wind_direction_x, int)

    def test_property_wind_direction_y(self):
        self.assertIsInstance(self.packet.wind_direction_y, int)

    def test_property_track_length(self):
        self.assertIsInstance(self.packet.track_length, float)

    def test_property_wings(self):
        self.assertIsInstance(self.packet.wings, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_wings_values(self):
        for value in self.packet.wings:
            with self.subTest(item=value):
                self.assertIsInstance(value, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_wings_values_nosubtest(self):
        for value in self.packet.wings:
            self.assertIsInstance(value, int)

    def test_property_packet_type(self):
        self.assertEqual(self.packet.packet_type, 0)

    def test_property_packet_length(self):
        self.assertEqual(self.packet.packet_length, 1367)

    def test_property_packet_string(self):
        self.assertEqual(
            self.packet.packet_string,
            "HBBbbBBbBBB21fHBBhHhHHBBBBBbffHHBBbB22f8B12f8B8f12B4h20H16f4H2f2BbbBbbbhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBfhhhHBBBBffBBB")
        
    def test_property_participant_info(self):
        self.assertIsInstance(self.packet.participant_info, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_participant_info_values(self):
        for value in self.packet.participant_info:
            with self.subTest(item=value):
                self.assertIsInstance(value, ParticipantInfo)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_participant_info_values_nosubtest(self):
        for value in self.packet.participant_info:
            self.assertIsInstance(value, ParticipantInfo)

    def test_method_str(self):
        self.assertEqual(str(self.packet), "TelemetryData")

    def test_method_repr(self):
        self.assertEqual(repr(self.packet), "TelemetryData")
        
        
class TestParticipantInfo(unittest.TestCase):
    """
    Unit tests for the Participant Info object contained in the
    Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata11'
    participant_info = None

    @classmethod
    def setUpClass(cls):
        with open(cls.packet_file, 'rb') as packet_data:
            packet = TelemetryDataPacket(packet_data.read())
            cls.participant_info = packet.participant_info

    @classmethod
    def tearDownClass(cls):
        del cls.participant_info

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_position(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.world_position, list)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_position_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.world_position, list)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_world_position_values(self):
        for participant in self.participant_info:
            for value in participant.world_position:
                with self.subTest(item=(participant, value)):
                    self.assertIsInstance(value, float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_world_postion_values_nosubtest(self):
        for participant in self.participant_info:
            for value in participant.world_position:
                self.assertIsInstance(value, float)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_current_lap_distance(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(
                    participant.current_lap_distance,
                    int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_current_lap_distance_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.current_lap_distance, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_is_active(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.is_active, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_is_active_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.is_active, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_race_position(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.race_position, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_race_position_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.race_position, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_invalid_lap(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.invalid_lap, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_invalid_lap_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.invalid_lap, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_laps_completed(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.laps_completed, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_laps_completed_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.laps_completed, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_current_lap(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.current_lap, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_current_lap_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.current_lap, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_sector(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(participant.sector, int)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_sector_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.sector, int)

    @unittest.skipIf(sys.version_info < (3, 4), "subTest not supported")
    def test_property_last_sector_time(self):
        for participant in self.participant_info:
            with self.subTest(item=participant):
                self.assertIsInstance(
                    participant.last_sector_time,
                    float)

    @unittest.skipUnless(
        sys.version_info < (3, 4),
        "subTest not supported")
    def test_property_last_sector_time_nosubtest(self):
        for participant in self.participant_info:
            self.assertIsInstance(participant.last_sector_time, float)


class TestAdditionalParticipantPacket(unittest.TestCase):
    """
    Unit tests for an Additional Participant Packet incorrectly placed
    into a Telemetry Data Packet.
    """
    packet_file = 'assets/race21/pdata9'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = TelemetryDataPacket(packet_data.read())


class TestParticipantPacket(unittest.TestCase):
    """
    Unit tests for a Participant Packet incorrectly placed into a
    Telemetry Data Packet
    """
    packet_file = 'assets/race21/pdata4'
    packet = None

    def test_initialization(self):
        with self.assertRaises(struct.error):
            with open(self.packet_file, 'rb') as packet_data:
                self.packet = TelemetryDataPacket(packet_data.read())


class TestGarbageData(unittest.TestCase):
    """
    Unit tests for data that is complete garbage.
    Everything turns to garbage.
    """
    def test_initialization(self):
        with self.assertRaises(struct.error):
            garbage = os.urandom(1000)
            self.packet = TelemetryDataPacket(garbage)
