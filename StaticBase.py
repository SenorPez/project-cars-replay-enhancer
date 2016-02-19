"""
Provides base class for static objects. Static objects are those
objects that do not update continuously based on the telemetry
feed.
"""

import abc
from moviepy.video.io.bindings import PIL_to_npimage

class StaticBase(metaclass=abc.ABCMeta):
    """
    Defines base class for static objects, including default object
    return methods.

    To get the representation of the static object, `to_frame` is
    called. Execution chain is `to_frame` -> `_make_material` ->
    `_write_data`.

    To get the mask of the static object, `make_mask` is called.
    Execution chain is `make_mask` -> `_make_material`.
    """
    @abc.abstractmethod
    def to_frame(self):
        """Render the card with data. Override to customize."""
        return PIL_to_npimage(
            self._make_material(False).convert('RGB'))

    @abc.abstractmethod
    def make_mask(self):
        """Default mask creation. Override to customize."""
        return PIL_to_npimage(
            self._make_material(True).split()[-1].convert('RGB'))

    @abc.abstractmethod
    def _write_data(self):
        """Write data to the canvas."""

    @abc.abstractmethod
    def _make_material(self, material_only):
        """Create material used as a canvas."""

    @staticmethod
    def format_time(seconds):
        """
        Converts seconds into seconds, minutes:seconds, or
        hours:minutes.seconds as appropriate.
        """
        minutes, seconds = divmod(float(seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return_value = (int(hours), int(minutes), float(seconds))

        if hours:
            return "{0:d}:{1:0>2d}:{2:0>5.2f}".format(*return_value)
        elif minutes:
            return "{1:d}:{2:0>5.2f}".format(*return_value)
        else:
            return "{2:.2f}".format(*return_value)
