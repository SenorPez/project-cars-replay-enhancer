"""
Provides classes for the creation of a GT Sport style
Standings overlay.
"""

from PIL import Image, ImageDraw
from replayenhancer.DynamicBase import DynamicBase


class GTStandings(DynamicBase):
    """
    Creates a standings overlay that constantly updates with the
    following columns of information:
    Position | Driver

    Additional information is available in customizable flyouts.

    Up to 10 drivers are displayed.
    Race positions 1-5 are always displayed.
    Positions n-2 through n+2, where n is the viewed car are displayed
        if there is no overlap with positions 1-5.
    Additional positions are added to display 10 if needed.
    """

    _ups = 30

    @property
    def clip_t(self):
        # TODO: Determine if this is even needed.
        return self._clip_t

    @clip_t.setter
    def clip_t(self, value):
        self._clip_t = value

    @property
    def ups(self):
        # TODO: Determine if this is even needed.
        return self._ups

    @ups.setter
    def ups(self, value):
        self._ups = value

    def __init__(self, clip_t=0, *, ups=30):
        self._clip_t = clip_t
        self._ups = ups

    def make_mask(self):
        return super(GTStandings, self).make_mask()

    def to_frame(self):
        return super(GTStandings, self).to_frame()

    def update(self, force_process=False):
        pass

    def _make_material(self, material_only):
        return self._write_data()

    def _write_data(self):
        return Image.new('RGBA', (100, 100))


class StandingsLine():
    """
    Represents a single line in the standings display.
    """

    _position_color = (0, 0, 0, 200)
    _name_color = (51, 51, 51, 200)
    _viewed_position_color = (255, 215, 0, 200)
    _viewed_name_color = (255, 215, 0, 200)

    _position_text_color = (255, 255, 255, 255)
    _name_text_color = (255, 255, 255, 255)
    _viewed_position_text_color = (0, 0, 0, 255)
    _viewed_name_text_color = (0, 0, 0, 255)

    _ups = 30

    def __init__(self, driver, font, text_size, *, ups=30):
        """
        Creates a new Standings Line object.
        """
        self._ups = ups
        self._viewed = False

        self._driver = driver
        self._font = font
        self._text_size = text_size

    @property
    def name_color(self):
        """
        Gets the material color for the name, based on if it's the
        viewed car or not.
        """
        return self._viewed_name_color if self._viewed \
            else self._name_color

    @property
    def name_text_color(self):
        """
        Gets the text color for the name, based on if it's the
        viewed car or not.
        """
        return self._viewed_name_text_color if self._viewed \
            else self._name_text_color

    @property
    def position_color(self):
        """
        Gets the material color for the position, based on if it's the
        viewed car or not.
        """
        return self._viewed_position_color if self._viewed \
            else self._position_color

    @property
    def position_text_color(self):
        """
        Gets the text color for the position, based on if it's the
        viewed car or not.
        """
        return self._viewed_position_text_color if self._viewed \
            else self._position_text_color

    def _render(self):
        text_width, text_height = self._text_size
        block_height = self._font.getsize("A")[1]

        material_width = text_height*2+text_width+10*2
        material_height = text_height*2
        material = Image.new('RGBA', (material_width, material_height))

        draw = ImageDraw.Draw(material)

        draw.rectangle(
            (0, 0, material_height+1, material_height+1),
            fill=self.position_color)
        position_width = self._font.getsize(
            str(self._driver.race_position))[0]
        x_position = int((material_height-position_width)/2)
        y_position = int((material_height-block_height)/2)
        draw.text(
            (x_position, y_position),
            str(self._driver.race_position),
            fill=self.position_text_color,
            font=self._font)

        draw.rectangle(
            (material_height, 0, material_width+1, material_height+1),
            fill=self.name_color)
        x_position = material_height+10
        draw.text(
            (x_position, y_position),
            str(self._driver.name),
            fill=self.name_text_color,
            font=self._font)

        return material
