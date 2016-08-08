"""
Provides base class for dynamic objects. Dynamic objects are those
objects that update continuously based on the telemetry feed.
"""

import abc
from moviepy.video.io.bindings import PIL_to_npimage

from StaticBase import StaticBase

class DynamicBase(StaticBase, metaclass=abc.ABCMeta):
    """
    Defines base class for dynamic objects, including default object
    return methods. Methods are named to be compatible with MoviePy's
    UpdatedVideoClip object. Typically, they will be called from
    that object.

    To update the object state, `update` is called.

    To get the representation of the dynamic object at the current
    world state, `to_frame` is called. Execution chain is `to_frame` ->
    `update` -> `_make_material` -> `_write_data`.

    To get the mask of the dynamic oject, `make_mask` is called.
    Exectuion chain is `make_mask` -> `update` -> `_make_material`.
    """
    @property
    @abc.abstractmethod
    def ups(self):
        """Updates per second of the simulation."""

    @ups.setter
    @abc.abstractmethod
    def ups(self, value):
        return

    @property
    @abc.abstractmethod
    def clip_t(self):
        """Current time in simulation."""

    @clip_t.setter
    @abc.abstractmethod
    def clip_t(self, value):
        return

    @abc.abstractmethod
    def update(self, force_process=False):
        """
        If force_process is False, only clip_t is updated. Use this to
        advance through time without the overhead of rendering the
        intervening frames. Note that this may cause errors in data
        display, however, for data that rely on historical information.

        If force_process is True, the data is read and clip_t
        is updated.
        """

    @abc.abstractmethod
    def to_frame(self):
        """Render the card with data. Override to customize."""
        return PIL_to_npimage(
            self._make_material(False).convert('RGB'))
