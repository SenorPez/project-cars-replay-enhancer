class StartingGridEntry:
    """
    Represents an entry on the starting grid.
    """
    def __init__(self, position, driver_index, driver_name):
        self._position = position
        self._driver_index = driver_index
        self._driver_name = driver_name

    @property
    def driver_index(self):
        """
        Index position of driver.
        """
        return self._driver_index

    @property
    def driver_name(self):
        """
        Telemetry-read name of driver.
        """
        return self._driver_name

    @property
    def position(self):
        """
        Starting position of driver.
        """
        return self._position
