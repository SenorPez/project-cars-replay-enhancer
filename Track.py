"""
Provides track data for the Project CARS Replay Enhancer.
Way too many thanks to mrbelowski, who made much of the data publically
available through his CrewChief app, preventing me from having to
reinvent the wheel.
https://github.com/mrbelowski/CrewChiefV4/
"""

import json
import os

class Track():
    """
    Defines a Track object with the following properties:

    - Name: string
    - Length: float
    - Pit: bool
    - Pit Entry Coordinates: [float, float]
    - Pit Exit Coordinates: [float, float]
    - Pit Detection Radius: float
    """
    def __init__(self, track_length, reverse=False):
        with open(os.path.realpath("track_data.json"), 'r') \
                as json_file:
            try:
                json_data = json.load(json_file)
            except ValueError as json_error:
                raise json_error

        integer, _, decimal = str(track_length).partition('.')
        track_length = ".".join([integer, (decimal+'0'*3)[:3]])
        track = [y for x in json_data['tracks'] \
            for y in x.values() \
            if y['length'] == float(track_length)]

        if len(track) == 0:
            raise ValueError("ValueError: No matching track found \
                in data.")
        if len(track) > 1:
            raise ValueError("ValueError: Multiple matching tracks \
                found in data.")
        else:
            track = track[0]
            self.name = str(track['display_name'])
            if reverse:
                self.name += " Reverse"
            self.length = float(track['length'])

            try:
                #If all of the pit keys are present, we populate the
                #pit information.
                self.pit = True
                self.pit_entry = [float(track['pit_entry'][0]),
                                  float(track['pit_entry'][1])]
                self.pit_exit = [float(track['pit_exit'][0]),
                                 float(track['pit_exit'][1])]
                self.pit_radius = float(track['pit_radius'])
            except KeyError:
                #If any of the pit keys aren't present, we treat it
                #like there's no pit on the track.
                self.pit = False

    def at_pit_entry(self, coordinates):
        """
        Returns if a car is at the pit entry. Parameters:

        - coordinates: List consisting of x and z coordinates
        """
        return self.pit and \
            abs(self.pit_entry[0]-coordinates[0]) < \
                self.pit_radius and \
            abs(self.pit_entry[1]-coordinates[1]) < \
                self.pit_radius

    def at_pit_exit(self, coordinates):
        """
        Returns if a car is at the pit exit. Parameters:

        - coordinates: List consisting of x and z coordinates
        """
        return self.pit and \
            abs(self.pit_exit[0]-coordinates[0]) < \
                self.pit_radius and \
            abs(self.pit_exit[1]-coordinates[1]) < \
                self.pit_radius
