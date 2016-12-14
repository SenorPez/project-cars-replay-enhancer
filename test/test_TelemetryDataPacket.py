"""Tests TelemetryDataPacket.py

"""
from unittest.mock import patch
import unittest
from struct import pack
from hashlib import md5
from collections import deque

from replayenhancer.TelemetryDataPacket \
    import ParticipantInfo, TelemetryDataPacket


class TestTelemetryDataPacket(unittest.TestCase):
    """Unit tests against the TelemetryDataPacket object.

    """
    from random import uniform, randrange
    expected_build_version_number = randrange(2000)
    expected_packet_type = 0

    expected_game_state = randrange(4)
    expected_session_state = randrange(7)

    expected_viewed_participant_index = randrange(57)
    expected_num_participants = randrange(57)

    expected_unfiltered_throttle = randrange(256)
    expected_unfiltered_brake = randrange(256)
    expected_unfiltered_steering = randrange(-128, 128)
    expected_unfiltered_clutch = randrange(256)
    expected_race_state = randrange(7)
    expected_lap_invalidated = randrange(2)
    expected_anti_lock = randrange(2)
    expected_boost = randrange(2)

    expected_laps_in_event = randrange(256)

    expected_best_lap_time = uniform(0, 360)
    expected_last_lap_time = uniform(0, 360)
    expected_current_time = uniform(0, 360)
    expected_split_time_ahead = uniform(0, 360)
    expected_split_time_behind = uniform(0, 360)
    expected_split_time = uniform(0, 360)
    expected_event_time_remaining = uniform(0, 360)
    expected_personal_fastest_lap_time = uniform(0, 360)
    expected_world_fastest_lap_time = uniform(0, 360)
    expected_current_s1_time = uniform(0, 360)
    expected_current_s2_time = uniform(0, 360)
    expected_current_s3_time = uniform(0, 360)
    expected_fastest_s1_time = uniform(0, 360)
    expected_fastest_s2_time = uniform(0, 360)
    expected_fastest_s3_time = uniform(0, 360)
    expected_personal_fastest_s1_time = uniform(0, 360)
    expected_personal_fastest_s2_time = uniform(0, 360)
    expected_personal_fastest_s3_time = uniform(0, 360)
    expected_world_fastest_s1_time = uniform(0, 360)
    expected_world_fastest_s2_time = uniform(0, 360)
    expected_world_fastest_s3_time = uniform(0, 360)

    expected_joypad = randrange(9)

    expected_highest_flag = randrange(65)

    expected_pit_mode_schedule = randrange(65)

    expected_oil_temp = randrange(-32767, 32767)
    expected_oil_pressure = randrange(65535)
    expected_water_temp = randrange(-32767, 32767)
    expected_water_pressure = randrange(65535)
    expected_fuel_pressure = randrange(65535)
    expected_car_flags = randrange(256)
    expected_fuel_capacity = randrange(256)
    expected_brake = randrange(256)
    expected_throttle = randrange(256)
    expected_clutch = randrange(256)
    expected_steering = randrange(-128, 128)
    expected_fuel_level = uniform(0, 256)
    expected_speed = uniform(0, 256)
    expected_rpm = randrange(65535)
    expected_max_rpm = randrange(65535)
    expected_gear_num_gears = randrange(256)
    expected_boost_amount = randrange(256)
    expected_enforced_pit_stop_lap = randrange(-128, 128)
    expected_crash_state = randrange(256)

    expected_odometer = uniform(0, 256)
    expected_orientation = [uniform(0, 360), uniform(0, 360), uniform(0, 360)]
    expected_local_velocity = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_world_velocity = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_angular_velocity = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_local_acceleration = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_world_acceleration = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_extents_centre = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]

    expected_tyre_flags = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_terrain = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_tyre_y = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_tyre_rps = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_tyre_slip_speed = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_tyre_temp = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_tyre_grip = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_tyre_height_above_ground = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_tyre_lateral_stiffness = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_tyre_wear = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_brake_damage = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_suspension_damage = [
        randrange(256),
        randrange(256),
        randrange(256),
        randrange(256)]
    expected_brake_temp = [
        randrange(-32767, 32767),
        randrange(-32767, 32767),
        randrange(-32767, 32767),
        randrange(-32767, 32767)]
    expected_tyre_tread_temp = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]
    expected_tyre_layer_temp = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]
    expected_tyre_carcass_temp = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]
    expected_tyre_rim_temp = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]
    expected_tyre_internal_air_temp = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]
    expected_wheel_local_position_y = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_ride_height = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_suspension_travel = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_suspension_velocity = [
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255),
        uniform(0, 255)]
    expected_air_pressure = [
        randrange(65535),
        randrange(65535),
        randrange(65535),
        randrange(65535)]

    expected_engine_speed = uniform(0, 256)
    expected_engine_torque = uniform(0, 256)

    expected_aero_damage = randrange(256)
    expected_engine_damage = randrange(256)

    expected_ambient_temperature = randrange(-128, 128)
    expected_track_temperature = randrange(-128, 128)
    expected_rain_density = randrange(256)
    expected_wind_speed = randrange(-128, 128)
    expected_wind_direction_x = randrange(-128, 128)
    expected_wind_direction_y = randrange(-128, 128)

    expected_track_length = uniform(0, 256)
    expected_wings = [randrange(128), randrange(128)]
    expected_d_pad = randrange(128)

    def assertListAlmostEqual(self, list1, list2, delta):
        for item1, item2 in zip(list1, list2):
            self.assertAlmostEqual(item1, item2, delta=delta)

    @classmethod
    def binary_data(cls, **kwargs):
        test_data = list()
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

        try:
            test_data.append(kwargs['build_version_number'])
        except KeyError:
            test_data.append(cls.expected_build_version_number)

        try:
            test_data.append(kwargs['packet_type'])
        except KeyError:
            test_data.append(cls.expected_packet_type)

        try:
            game_state = kwargs['game_state']
        except KeyError:
            game_state = cls.expected_game_state

        try:
            session_state = kwargs['session_state']
        except KeyError:
            session_state = cls.expected_session_state

        test_data.append((session_state << 4) + game_state)

        try:
            test_data.append(kwargs['viewed_participant_index'])
        except KeyError:
            test_data.append(cls.expected_viewed_participant_index)

        try:
            test_data.append(kwargs['num_participants'])
        except KeyError:
            test_data.append(cls.expected_num_participants)

        try:
            test_data.append(kwargs['unfiltered_throttle'])
        except KeyError:
            test_data.append(cls.expected_unfiltered_throttle)

        try:
            test_data.append(kwargs['unfiltered_brake'])
        except KeyError:
            test_data.append(cls.expected_unfiltered_brake)

        try:
            test_data.append(kwargs['unfiltered_steering'])
        except KeyError:
            test_data.append(cls.expected_unfiltered_steering)

        try:
            test_data.append(kwargs['unfiltered_clutch'])
        except KeyError:
            test_data.append(cls.expected_unfiltered_clutch)

        try:
            race_state = kwargs['race_state']
        except KeyError:
            race_state = cls.expected_race_state

        try:
            lap_invalidated = kwargs['lap_invalidated']
        except KeyError:
            lap_invalidated = cls.expected_lap_invalidated

        try:
            anti_lock = kwargs['anti_lock']
        except KeyError:
            anti_lock = cls.expected_anti_lock

        try:
            boost = kwargs['boost']
        except KeyError:
            boost = cls.expected_boost

        test_data.append(
            (boost << 5)
            + (anti_lock << 4)
            + (lap_invalidated << 3)
            + race_state)

        try:
            test_data.append(kwargs['laps_in_event'])
        except KeyError:
            test_data.append(cls.expected_laps_in_event)

        try:
            test_data.append(kwargs['best_lap_time'])
        except KeyError:
            test_data.append(cls.expected_best_lap_time)

        try:
            test_data.append(kwargs['last_lap_time'])
        except KeyError:
            test_data.append(cls.expected_last_lap_time)

        try:
            test_data.append(kwargs['current_time'])
        except KeyError:
            test_data.append(cls.expected_current_time)

        try:
            test_data.append(kwargs['split_time_ahead'])
        except KeyError:
            test_data.append(cls.expected_split_time_ahead)

        try:
            test_data.append(kwargs['split_time_behind'])
        except KeyError:
            test_data.append(cls.expected_split_time_behind)

        try:
            test_data.append(kwargs['split_time'])
        except KeyError:
            test_data.append(cls.expected_split_time)

        try:
            test_data.append(kwargs['event_time_remaining'])
        except KeyError:
            test_data.append(cls.expected_event_time_remaining)

        try:
            test_data.append(kwargs['personal_fastest_lap_time'])
        except KeyError:
            test_data.append(cls.expected_personal_fastest_lap_time)

        try:
            test_data.append(kwargs['world_fastest_lap_time'])
        except KeyError:
            test_data.append(cls.expected_world_fastest_lap_time)

        try:
            test_data.append(kwargs['current_s1_time'])
        except KeyError:
            test_data.append(cls.expected_current_s1_time)

        try:
            test_data.append(kwargs['current_s2_time'])
        except KeyError:
            test_data.append(cls.expected_current_s2_time)

        try:
            test_data.append(kwargs['current_s3_time'])
        except KeyError:
            test_data.append(cls.expected_current_s3_time)

        try:
            test_data.append(kwargs['fastest_s1_time'])
        except KeyError:
            test_data.append(cls.expected_fastest_s1_time)

        try:
            test_data.append(kwargs['fastest_s2_time'])
        except KeyError:
            test_data.append(cls.expected_fastest_s2_time)

        try:
            test_data.append(kwargs['fastest_s3_time'])
        except KeyError:
            test_data.append(cls.expected_fastest_s3_time)

        try:
            test_data.append(kwargs['personal_fastest_s1_time'])
        except KeyError:
            test_data.append(cls.expected_personal_fastest_s1_time)

        try:
            test_data.append(kwargs['personal_fastest_s2_time'])
        except KeyError:
            test_data.append(cls.expected_personal_fastest_s2_time)

        try:
            test_data.append(kwargs['personal_fastest_s3_time'])
        except KeyError:
            test_data.append(cls.expected_personal_fastest_s3_time)

        try:
            test_data.append(kwargs['world_fastest_s1_time'])
        except KeyError:
            test_data.append(cls.expected_world_fastest_s1_time)

        try:
            test_data.append(kwargs['world_fastest_s2_time'])
        except KeyError:
            test_data.append(cls.expected_world_fastest_s2_time)

        try:
            test_data.append(kwargs['world_fastest_s3_time'])
        except KeyError:
            test_data.append(cls.expected_world_fastest_s3_time)

        try:
            test_data.append(kwargs['joypad'])
        except KeyError:
            test_data.append(cls.expected_joypad)

        try:
            test_data.append(kwargs['highest_flag'])
        except KeyError:
            test_data.append(cls.expected_highest_flag)

        try:
            test_data.append(kwargs['pit_mode_schedule'])
        except KeyError:
            test_data.append(cls.expected_pit_mode_schedule)

        try:
            test_data.append(kwargs['oil_temp'])
        except KeyError:
            test_data.append(cls.expected_oil_temp)

        try:
            test_data.append(kwargs['oil_pressure'])
        except KeyError:
            test_data.append(cls.expected_oil_pressure)

        try:
            test_data.append(kwargs['water_temp'])
        except KeyError:
            test_data.append(cls.expected_water_temp)

        try:
            test_data.append(kwargs['water_pressure'])
        except KeyError:
            test_data.append(cls.expected_water_pressure)

        try:
            test_data.append(kwargs['fuel_pressure'])
        except KeyError:
            test_data.append(cls.expected_fuel_pressure)

        try:
            test_data.append(kwargs['car_flags'])
        except KeyError:
            test_data.append(cls.expected_car_flags)

        try:
            test_data.append(kwargs['fuel_capacity'])
        except KeyError:
            test_data.append(cls.expected_fuel_capacity)

        try:
            test_data.append(kwargs['brake'])
        except KeyError:
            test_data.append(cls.expected_brake)

        try:
            test_data.append(kwargs['throttle'])
        except KeyError:
            test_data.append(cls.expected_throttle)

        try:
            test_data.append(kwargs['clutch'])
        except KeyError:
            test_data.append(cls.expected_clutch)

        try:
            test_data.append(kwargs['steering'])
        except KeyError:
            test_data.append(cls.expected_steering)

        try:
            test_data.append(kwargs['fuel_level'])
        except KeyError:
            test_data.append(cls.expected_fuel_level)

        try:
            test_data.append(kwargs['speed'])
        except KeyError:
            test_data.append(cls.expected_speed)

        try:
            test_data.append(kwargs['rpm'])
        except KeyError:
            test_data.append(cls.expected_rpm)

        try:
            test_data.append(kwargs['max_rpm'])
        except KeyError:
            test_data.append(cls.expected_max_rpm)

        try:
            test_data.append(kwargs['gear_num_gears'])
        except KeyError:
            test_data.append(cls.expected_gear_num_gears)

        try:
            test_data.append(kwargs['boost_amount'])
        except KeyError:
            test_data.append(cls.expected_boost_amount)

        try:
            test_data.append(kwargs['enforced_pit_stop_lap'])
        except KeyError:
            test_data.append(cls.expected_enforced_pit_stop_lap)

        try:
            test_data.append(kwargs['crash_state'])
        except KeyError:
            test_data.append(cls.expected_crash_state)

        try:
            test_data.append(kwargs['odometer'])
        except KeyError:
            test_data.append(cls.expected_odometer)

        try:
            test_data.extend(kwargs['orientation'])
        except KeyError:
            test_data.extend(cls.expected_orientation)

        try:
            test_data.extend(kwargs['local_velocity'])
        except KeyError:
            test_data.extend(cls.expected_local_velocity)

        try:
            test_data.extend(kwargs['world_velocity'])
        except KeyError:
            test_data.extend(cls.expected_world_velocity)

        try:
            test_data.extend(kwargs['angular_velocity'])
        except KeyError:
            test_data.extend(cls.expected_angular_velocity)

        try:
            test_data.extend(kwargs['local_acceleration'])
        except KeyError:
            test_data.extend(cls.expected_local_acceleration)

        try:
            test_data.extend(kwargs['world_acceleration'])
        except KeyError:
            test_data.extend(cls.expected_world_acceleration)

        try:
            test_data.extend(kwargs['extents_centre'])
        except KeyError:
            test_data.extend(cls.expected_extents_centre)

        try:
            test_data.extend(kwargs['tyre_flags'])
        except KeyError:
            test_data.extend(cls.expected_tyre_flags)

        try:
            test_data.extend(kwargs['terrain'])
        except KeyError:
            test_data.extend(cls.expected_terrain)

        try:
            test_data.extend(kwargs['tyre_y'])
        except KeyError:
            test_data.extend(cls.expected_tyre_y)

        try:
            test_data.extend(kwargs['tyre_rps'])
        except KeyError:
            test_data.extend(cls.expected_tyre_rps)

        try:
            test_data.extend(kwargs['tyre_slip_speed'])
        except KeyError:
            test_data.extend(cls.expected_tyre_slip_speed)

        try:
            test_data.extend(kwargs['tyre_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_temp)

        try:
            test_data.extend(kwargs['tyre_grip'])
        except KeyError:
            test_data.extend(cls.expected_tyre_grip)

        try:
            test_data.extend(kwargs['tyre_height_above_ground'])
        except KeyError:
            test_data.extend(cls.expected_tyre_height_above_ground)

        try:
            test_data.extend(kwargs['tyre_lateral_stiffness'])
        except KeyError:
            test_data.extend(cls.expected_tyre_lateral_stiffness)

        try:
            test_data.extend(kwargs['tyre_wear'])
        except KeyError:
            test_data.extend(cls.expected_tyre_wear)

        try:
            test_data.extend(kwargs['brake_damage'])
        except KeyError:
            test_data.extend(cls.expected_brake_damage)

        try:
            test_data.extend(kwargs['suspension_damage'])
        except KeyError:
            test_data.extend(cls.expected_suspension_damage)

        try:
            test_data.extend(kwargs['brake_temp'])
        except KeyError:
            test_data.extend(cls.expected_brake_temp)

        try:
            test_data.extend(kwargs['tyre_tread_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_tread_temp)

        try:
            test_data.extend(kwargs['tyre_layer_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_layer_temp)

        try:
            test_data.extend(kwargs['tyre_carcass_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_carcass_temp)

        try:
            test_data.extend(kwargs['tyre_rim_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_rim_temp)

        try:
            test_data.extend(kwargs['tyre_internal_air_temp'])
        except KeyError:
            test_data.extend(cls.expected_tyre_internal_air_temp)

        try:
            test_data.extend(kwargs['wheel_local_position_y'])
        except KeyError:
            test_data.extend(cls.expected_wheel_local_position_y)

        try:
            test_data.extend(kwargs['ride_height'])
        except KeyError:
            test_data.extend(cls.expected_ride_height)

        try:
            test_data.extend(kwargs['suspension_travel'])
        except KeyError:
            test_data.extend(cls.expected_suspension_travel)

        try:
            test_data.extend(kwargs['suspension_velocity'])
        except KeyError:
            test_data.extend(cls.expected_suspension_velocity)

        try:
            test_data.extend(kwargs['air_pressure'])
        except KeyError:
            test_data.extend(cls.expected_air_pressure)

        try:
            test_data.append(kwargs['engine_speed'])
        except KeyError:
            test_data.append(cls.expected_engine_speed)

        try:
            test_data.append(kwargs['engine_torque'])
        except KeyError:
            test_data.append(cls.expected_engine_torque)

        try:
            test_data.append(kwargs['aero_damage'])
        except KeyError:
            test_data.append(cls.expected_aero_damage)

        try:
            test_data.append(kwargs['engine_damage'])
        except KeyError:
            test_data.append(cls.expected_engine_damage)

        try:
            test_data.append(kwargs['ambient_temperature'])
        except KeyError:
            test_data.append(cls.expected_ambient_temperature)

        try:
            test_data.append(kwargs['track_temperature'])
        except KeyError:
            test_data.append(cls.expected_track_temperature)

        try:
            test_data.append(kwargs['rain_density'])
        except KeyError:
            test_data.append(cls.expected_rain_density)

        try:
            test_data.append(kwargs['wind_speed'])
        except KeyError:
            test_data.append(cls.expected_wind_speed)

        try:
            test_data.append(kwargs['wind_direction_x'])
        except KeyError:
            test_data.append(cls.expected_wind_direction_x)

        try:
            test_data.append(kwargs['wind_direction_y'])
        except KeyError:
            test_data.append(cls.expected_wind_direction_y)

        # Add 896 bytes of pointless data to account for ParticipantInfo.
        for _ in range(56):
            test_data.append(1)
            test_data.append(1)
            test_data.append(1)
            test_data.append(2)
            test_data.append(3)
            test_data.append(3)
            test_data.append(3)
            test_data.append(3)
            test_data.append(4.0)

        try:
            test_data.append(kwargs['track_length'])
        except KeyError:
            test_data.append(cls.expected_track_length)

        try:
            test_data.extend(kwargs['wings'])
        except KeyError:
            test_data.extend(cls.expected_wings)

        try:
            test_data.append(kwargs['d_pad'])
        except KeyError:
            test_data.append(cls.expected_d_pad)

        return pack(packet_string, *test_data)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_init(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = TelemetryDataPacket
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_init_wrong_packet_length(self, _):
        test_binary_data = pack("H", 42)

        from struct import error
        with self.assertRaises(error):
            TelemetryDataPacket(test_binary_data)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_init_wrong_packet_type(self, _):
        with self.assertRaises(ValueError):
            TelemetryDataPacket(self.binary_data(packet_type=1))

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_build_version_number(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_build_version_number
        self.assertEqual(instance.build_version_number, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_data_hash(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = md5(self.binary_data()).hexdigest()
        self.assertEqual(instance.data_hash, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_game_state(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_game_state
        self.assertEqual(instance.game_state, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_session_state(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_session_state
        self.assertEqual(instance.session_state, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_viewed_participant_index(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_viewed_participant_index
        self.assertEqual(instance.viewed_participant_index, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_num_participants(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_num_participants
        self.assertEqual(instance.num_participants, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_unfiltered_throttle(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_unfiltered_throttle
        self.assertEqual(instance.unfiltered_throttle, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_unfiltered_brake(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_unfiltered_brake
        self.assertEqual(instance.unfiltered_brake, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_unfiltered_steering(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_unfiltered_steering
        self.assertEqual(instance.unfiltered_steering, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_unfiltered_clutch(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_unfiltered_clutch
        self.assertEqual(instance.unfiltered_clutch, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_race_state(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_race_state
        self.assertEqual(instance.race_state, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_laps_in_event(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_laps_in_event
        self.assertEqual(instance.laps_in_event, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_best_lap_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_best_lap_time
        self.assertAlmostEqual(instance.best_lap_time, expected_result, 4)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_last_lap_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_last_lap_time
        self.assertAlmostEqual(
            instance.last_lap_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_current_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_current_time
        self.assertAlmostEqual(instance.current_time, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_split_time_ahead(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_split_time_ahead
        self.assertAlmostEqual(
            instance.split_time_ahead,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_split_time_behind(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_split_time_behind
        self.assertAlmostEqual(
            instance.split_time_behind,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_split_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_split_time
        self.assertAlmostEqual(instance.split_time, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_event_time_remaining(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_event_time_remaining
        self.assertAlmostEqual(
            instance.event_time_remaining,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_personal_fastest_lap_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_personal_fastest_lap_time
        self.assertAlmostEqual(
            instance.personal_fastest_lap_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_fastest_lap_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_fastest_lap_time
        self.assertAlmostEqual(
            instance.world_fastest_lap_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_current_s1_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_current_s1_time
        self.assertAlmostEqual(
            instance.current_s1_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_current_s2_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_current_s2_time
        self.assertAlmostEqual(
            instance.current_s2_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_current_s3_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_current_s3_time
        self.assertAlmostEqual(
            instance.current_s3_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fastest_s1_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fastest_s1_time
        self.assertAlmostEqual(
            instance.fastest_s1_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fastest_s2_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fastest_s2_time
        self.assertAlmostEqual(
            instance.fastest_s2_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fastest_s3_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fastest_s3_time
        self.assertAlmostEqual(
            instance.fastest_s3_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_personal_fastest_s1_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_personal_fastest_s1_time
        self.assertAlmostEqual(
            instance.personal_fastest_s1_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_personal_fastest_s2_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_personal_fastest_s2_time
        self.assertAlmostEqual(
            instance.personal_fastest_s2_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_personal_fastest_s3_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_personal_fastest_s3_time
        self.assertAlmostEqual(
            instance.personal_fastest_s3_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_fastest_s1_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_fastest_s1_time
        self.assertAlmostEqual(
            instance.world_fastest_s1_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_fastest_s2_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_fastest_s2_time
        self.assertAlmostEqual(
            instance.world_fastest_s2_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_fastest_s3_time(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_fastest_s3_time
        self.assertAlmostEqual(
            instance.world_fastest_s3_time,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_joypad(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_joypad
        self.assertEqual(instance.joypad, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_highest_flag(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_highest_flag
        self.assertEqual(instance.highest_flag, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_pit_mode_schedule(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_pit_mode_schedule
        self.assertEqual(instance.pit_mode_schedule, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_oil_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_oil_temp
        self.assertEqual(instance.oil_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_oil_pressure(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_oil_pressure
        self.assertEqual(instance.oil_pressure, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_water_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_water_temp
        self.assertEqual(instance.water_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_water_pressure(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_water_pressure
        self.assertEqual(instance.water_pressure, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fuel_pressure(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fuel_pressure
        self.assertEqual(instance.fuel_pressure, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_car_flags(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_car_flags
        self.assertEqual(instance.car_flags, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fuel_capacity(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fuel_capacity
        self.assertEqual(instance.fuel_capacity, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_brake(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_brake
        self.assertEqual(instance.brake, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_throttle(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_throttle
        self.assertEqual(instance.throttle, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_clutch(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_clutch
        self.assertEqual(instance.clutch, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_steering(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_steering
        self.assertEqual(instance.steering, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_fuel_level(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_fuel_level
        self.assertAlmostEqual(instance.fuel_level, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_speed(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_speed
        self.assertAlmostEqual(instance.speed, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_rpm(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_rpm
        self.assertEqual(instance.rpm, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_max_rpm(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_max_rpm
        self.assertEqual(instance.max_rpm, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_gear_num_gears(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_gear_num_gears
        self.assertEqual(instance.gear_num_gears, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_boost_amount(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_boost_amount
        self.assertEqual(instance.boost_amount, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_enforced_pit_stop_lap(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_enforced_pit_stop_lap
        self.assertEqual(instance.enforced_pit_stop_lap, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_crash_state(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_crash_state
        self.assertEqual(instance.crash_state, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_odometer(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_odometer
        self.assertAlmostEqual(instance.odometer, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_orientation(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_orientation
        self.assertListAlmostEqual(
            instance.orientation,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_local_velocity(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_local_velocity
        self.assertListAlmostEqual(
            instance.local_velocity,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_velocity(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_velocity
        self.assertListAlmostEqual(
            instance.world_velocity,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_angular_velocity(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_angular_velocity
        self.assertListAlmostEqual(
            instance.angular_velocity,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_local_acceleration(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_local_acceleration
        self.assertListAlmostEqual(
            instance.local_acceleration,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_world_acceleration(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_world_acceleration
        self.assertListAlmostEqual(
            instance.world_acceleration,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_extents_centre(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_extents_centre
        self.assertListAlmostEqual(
            instance.extents_centre,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_flags(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_flags
        self.assertListEqual(instance.tyre_flags, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_terrain(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_terrain
        self.assertListEqual(instance.terrain, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_y(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_y
        self.assertListAlmostEqual(instance.tyre_y, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_rps(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_rps
        self.assertListAlmostEqual(instance.tyre_rps, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_slip_speed(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_slip_speed
        self.assertListAlmostEqual(
            instance.tyre_slip_speed,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_temp
        self.assertListEqual(instance.tyre_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_grip(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_grip
        self.assertListEqual(instance.tyre_grip, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_height_above_ground(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_height_above_ground
        self.assertListAlmostEqual(
            instance.tyre_height_above_ground,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_lateral_stiffness(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_lateral_stiffness
        self.assertListAlmostEqual(
            instance.tyre_lateral_stiffness,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_wear(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_wear
        self.assertListEqual(instance.tyre_wear, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_brake_damage(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_brake_damage
        self.assertListEqual(instance.brake_damage, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_suspension_damage(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_suspension_damage
        self.assertListEqual(instance.suspension_damage, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_brake_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_brake_temp
        self.assertListEqual(instance.brake_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_tread_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_tread_temp
        self.assertListEqual(instance.tyre_tread_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_layer_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_layer_temp
        self.assertListEqual(instance.tyre_layer_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_carcass_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_carcass_temp
        self.assertListEqual(instance.tyre_carcass_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_rim_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_rim_temp
        self.assertListEqual(instance.tyre_rim_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_tyre_internal_air_temp(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_tyre_internal_air_temp
        self.assertListEqual(instance.tyre_internal_air_temp, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_wheel_local_position_y(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_wheel_local_position_y
        self.assertListAlmostEqual(
            instance.wheel_local_position_y,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_ride_height(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_ride_height
        self.assertListAlmostEqual(
            instance.ride_height,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_suspension_travel(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_suspension_travel
        self.assertListAlmostEqual(
            instance.suspension_travel,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_suspension_velocity(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_suspension_velocity
        self.assertListAlmostEqual(
            instance.suspension_velocity,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_air_pressure(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_air_pressure
        self.assertListEqual(instance.air_pressure, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_engine_speed(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_engine_speed
        self.assertAlmostEqual(instance.engine_speed, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_engine_torque(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_engine_torque
        self.assertAlmostEqual(
            instance.engine_torque,
            expected_result,
            delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_aero_damage(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_aero_damage
        self.assertEqual(instance.aero_damage, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_engine_damage(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_engine_damage
        self.assertEqual(instance.engine_damage, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_ambient_temperature(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_ambient_temperature
        self.assertEqual(instance.ambient_temperature, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_track_temperature(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_track_temperature
        self.assertEqual(instance.track_temperature, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_rain_density(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_rain_density
        self.assertEqual(instance.rain_density, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_wind_speed(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_wind_speed
        self.assertEqual(instance.wind_speed, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_wind_direction_x(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_wind_direction_x
        self.assertEqual(instance.wind_direction_x, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_wind_direction_y(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_wind_direction_y
        self.assertEqual(instance.wind_direction_y, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_participant_info(self, _):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = list
        self.assertIsInstance(instance.participant_info, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_track_length(self, mock_participant_info):
        def remove_participant_info_data(*args):
            for _ in range(9):
                args[0].popleft()
        mock_participant_info.side_effect = remove_participant_info_data

        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_track_length
        self.assertAlmostEqual(instance.track_length, expected_result, delta=0.001)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_wings(self, mock_participant_info):
        def remove_participant_info_data(*args):
            for _ in range(9):
                args[0].popleft()
        mock_participant_info.side_effect = remove_participant_info_data

        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_wings
        self.assertListEqual(instance.wings, expected_result)

    @patch('replayenhancer.TelemetryDataPacket.ParticipantInfo', autospec=True)
    def test_property_d_pad(self, mock_participant_info):
        def remove_participant_info_data(*args):
            for _ in range(9):
                args[0].popleft()
        mock_participant_info.side_effect = remove_participant_info_data

        instance = TelemetryDataPacket(self.binary_data())
        expected_result = self.expected_d_pad
        self.assertEqual(instance.d_pad, expected_result)

    def test_method_repr(self):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = "TelemetryDataPacket"
        self.assertEqual(repr(instance), expected_result)

    def test_method_str(self):
        instance = TelemetryDataPacket(self.binary_data())
        expected_result = "TelemetryDataPacket"
        self.assertEqual(str(instance), expected_result)


class TestParticipantInfo(unittest.TestCase):
    """Unit tests against the ParticipantInfo object.

    """
    from random import choice, random, randrange
    expected_world_position = [
        randrange(100)+choice([0, 0.25, 0.50, 0.75]),
        randrange(100),
        randrange(100) + choice([0, 0.25, 0.50, 0.75])]
    expected_current_lap_distance = randrange(100)
    expected_is_active = 1
    expected_race_position = randrange(56)
    expected_invalid_lap = 0
    expected_laps_completed = randrange(50)
    expected_current_lap = expected_laps_completed + 1
    expected_sector = randrange(1, 4)
    expected_last_sector_time = random()

    @classmethod
    def binary_data(cls, **kwargs):
        test_data = list()

        try:
            world_position = kwargs['world_position']
        except KeyError:
            world_position = cls.expected_world_position

        test_data.extend([int(num) for num in world_position])

        try:
            test_data.append(kwargs['current_lap_distance'])
        except KeyError:
            test_data.append(cls.expected_current_lap_distance)

        try:
            is_active = kwargs['is_active']
        except KeyError:
            is_active = cls.expected_is_active

        try:
            race_position = kwargs['race_position']
        except KeyError:
            race_position = cls.expected_race_position

        test_data.append((is_active << 7) + race_position)

        try:
            invalid_lap = kwargs['invalid_lap']
        except KeyError:
            invalid_lap = cls.expected_invalid_lap

        try:
            laps_completed = kwargs['laps_completed']
        except KeyError:
            laps_completed = cls.expected_laps_completed

        test_data.append((invalid_lap << 7) + laps_completed)

        try:
            test_data.append(kwargs['current_lap'])
        except KeyError:
            test_data.append(cls.expected_current_lap)

        try:
            sector = kwargs['sector']
        except KeyError:
            sector = cls.expected_sector

        x_acc = int(((world_position[0] - int(world_position[0])) * 100) / 25)
        z_acc = int(((world_position[2] - int(world_position[2])) * 100) / 25)
        test_data.append((z_acc << 5) + (x_acc << 3) + sector)

        try:
            test_data.append(kwargs['last_sector_time'])
        except KeyError:
            test_data.append(cls.expected_last_sector_time)

        return deque(tuple(test_data))

    def test_init(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = ParticipantInfo
        self.assertIsInstance(instance, expected_result)

    def test_property_current_lap(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_current_lap
        self.assertEqual(instance.current_lap, expected_result)

    def test_property_current_lap_distance(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_current_lap_distance
        self.assertEqual(instance.current_lap_distance, expected_result)

    def test_property_invalid_lap_false(self):
        instance = ParticipantInfo(self.binary_data(invalid_lap=0))
        self.assertFalse(instance.invalid_lap)

    def test_property_invalid_lap_true(self):
        instance = ParticipantInfo(self.binary_data(invalid_lap=1))
        self.assertTrue(instance.invalid_lap)

    def test_property_invalid_lap_false_negative_at_race_start(self):
        instance = ParticipantInfo(self.binary_data(
            invalid_lap=1,
            sector=3,
            last_sector_time=-123))
        self.assertFalse(instance.invalid_lap)

    def test_property_is_active_false(self):
        instance = ParticipantInfo(self.binary_data(is_active=0))
        self.assertFalse(instance.is_active)

    def test_property_is_active_true(self):
        instance = ParticipantInfo(self.binary_data(is_active=1))
        self.assertTrue(instance.is_active)

    def test_property_laps_completed(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_laps_completed
        self.assertEqual(instance.laps_completed, expected_result)

    def test_property_last_sector_time(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_last_sector_time
        self.assertEqual(instance.last_sector_time, expected_result)

    def test_property_race_position(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_race_position
        self.assertEqual(instance.race_position, expected_result)

    def test_property_sector(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_sector
        self.assertEqual(instance.sector, expected_result)

    def test_property_world_position(self):
        instance = ParticipantInfo(self.binary_data())
        expected_result = self.expected_world_position
        self.assertListEqual(instance.world_position, expected_result)
