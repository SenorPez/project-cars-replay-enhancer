"""
Tests StartingGridEntry.py
"""
from unittest import TestCase
from unittest.mock import sentinel

from replayenhancer.StartingGridEntry import StartingGridEntry


class TestStartingGridEntry(TestCase):
    """
    Tests StartingGridEntry object.
    """

    def test_init(self):
        instance = StartingGridEntry(sentinel.position,
                                     sentinel.driver_index,
                                     sentinel.driver_name)
        expected_result = StartingGridEntry
        self.assertIsInstance(instance, expected_result)

    def test_property_driver_index(self):
        instance = StartingGridEntry(sentinel.position,
                                     sentinel.driver_index,
                                     sentinel.driver_name)
        expected_result = sentinel.driver_index
        self.assertEqual(instance.driver_index, expected_result)

    def test_property_driver_name(self):
        instance = StartingGridEntry(sentinel.position,
                                     sentinel.driver_index,
                                     sentinel.driver_name)
        expected_result = sentinel.driver_name
        self.assertEqual(instance.driver_name, expected_result)

    def test_property_position(self):
        instance = StartingGridEntry(sentinel.position,
                                     sentinel.driver_index,
                                     sentinel.driver_name)
        expected_result = sentinel.position
        self.assertEqual(instance.position, expected_result)
