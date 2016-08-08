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
    def __init__(self, track_length, reverse=False, error=2):
        with open(os.path.realpath("track_data.json"), 'r') \
                as json_file:
            try:
                json_data = json.load(json_file)
            except ValueError as json_error:
                raise json_error

        #integer, _, decimal = str(track_length).partition('.')
        #track_length = ".".join([integer, (decimal+'0'*3)[:3]])
        track = sorted(
            [y \
                for x in json_data['tracks'] \
                for y in x.values() \
                if abs(y['length']-float(track_length)) < error],
            key=lambda y: abs(y['length']-float(track_length)))

        if len(track) == 0:
            print(
                "Error. No matching track length found",
                "in data. Supplied track length was {}".format(
                    track_length))
            print(
                "Press any key to continue. Pit stop detection",
                "will be disabled.")
            input("--> ")

            self.pit = False
        else:
            use_track = "1"
            if len(track) > 1:
                print(
                    "Error. Multiple matching track lengths found",
                    "in data. Supplied track length was {}".format(
                        track_length))
                for i, matching_track in enumerate(track, 1):
                    print("Enter {} to use {}".format(
                        i, matching_track['display_name']))
                print(
                    "Enter any other value, or press Enter to",
                    "continue. Pit stop detection will be disabled.")
                use_track = input("--> ")

            if len(use_track):
                try:
                    use_track = int(use_track)-1
                    if use_track < 0:
                        raise ValueError
                    track = track[use_track]
                except (IndexError, ValueError):
                    self.pit = False
                else:
                    self.name = str(track['display_name'])
                    print("Using Track: {}".format(self.name))
                    if reverse:
                        self.name += " Reverse"
                    self.length = float(track['length'])

                    try:
                        #If all of the pit keys are present, we populate
                        #the pit information.
                        self.pit = True
                        self.pit_entry = [float(track['pit_entry'][0]),
                                          float(track['pit_entry'][1])]
                        self.pit_exit = [float(track['pit_exit'][0]),
                                         float(track['pit_exit'][1])]
                        self.pit_radius = float(track['pit_radius'])
                    except KeyError:
                        #If any of the pit keys aren't present, we treat
                        #it like there's no pit on the track.
                        self.pit = False
            else:
                self.pit = False

    def at_pit_entry(self, coordinates):
        """
        Returns if a car is at the pit entry. Parameters:

        - coordinates: List consisting of x and z coordinates
        """
        return self.pit and \
            abs(self.pit_entry[0]-coordinates[0]) < \
                self.pit_radius and \
            abs(self.pit_entry[1]-coordinates[2]) < \
                self.pit_radius

    def at_pit_exit(self, coordinates):
        """
        Returns if a car is at the pit exit. Parameters:

        - coordinates: List consisting of x and z coordinates
        """
        return self.pit and \
            abs(self.pit_exit[0]-coordinates[0]) < \
                self.pit_radius and \
            abs(self.pit_exit[1]-coordinates[2]) < \
                self.pit_radius
