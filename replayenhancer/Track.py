"""Provides a Track class for the Project CARS Replay Enhancer.

Notes
-----
Way too many thanks to mrbelowski, who made much of the data publicly
available through his CrewChief app, preventing me from having to
reinvent the wheel.
https://github.com/mrbelowski/CrewChiefV4/
"""

import os
from json import load


class Track:
    """Represents a Project CARS track.

    Notes
    -----
    Track detection requires the existence of `lib/track_data.json` that
    contains the track data.

    Parameters
    ----------
    track_length : float
        Length of the track, as found in the telemetry data.
    """
    def __init__(self, track_length):
        try:
            with open (os.path.join(
                    os.path.dirname(__file__),
                    'lib/track_data.json')) as json_file:
                json_data = load(json_file)

            matching_tracks = sorted(
                json_data.values(),
                key=lambda x: abs(x['length'] - float(track_length))
            )
            track = matching_tracks[0]

            try:
                # If all the pit keys are present, we populate the pit
                # information.
                self._pit_entry = (
                    float(track['pit_entry'][0]),
                    float(track['pit_entry'][1])
                )
                self._pit_exit = (
                    float(track['pit_exit'][0]),
                    float(track['pit_exit'][1])
                )
                self._pit_radius = float(track['pit_radius'])
            except KeyError:
                self._pit = False
            else:
                self._pit = True
        except FileNotFoundError:
            self._pit = False
        except ValueError as json_error:
            raise json_error

    def at_pit_entry(self, coordinates):
        """Determines if a car is at the pit entry.

        Parameters
        ----------
        coordinates : [float, float, float]
            Car coordinates.

        Returns
        -------
        bool
            True if car is at the pit entry
        """
        return self._pit \
            and abs(self._pit_entry[0]-coordinates[0]) < self._pit_radius \
            and abs(self._pit_entry[1]-coordinates[2]) < self._pit_radius

    def at_pit_exit(self, coordinates):
        """Determines if a car is at the pit exit.

        Parameters
        ----------
        coordinates : [float, float, float]
            Car coordinates.

        Returns
        -------
        bool
            True if car is at the pit exit
        """
        return self._pit \
            and abs(self._pit_exit[0]-coordinates[0]) < self._pit_radius \
            and abs(self._pit_exit[1]-coordinates[2]) < self._pit_radius
