import unittest
from vectordb.selector import (
    BaseSelector,
)
from enum import Enum
import loguru

logger = loguru.logger


class InitialOptions(Enum):
    Option1 = {"data": "some_data1"}
    Option2 = {"data": "some_data2"}


class TestBaseSelector(unittest.TestCase):
    def setUp(self):
        self.selector = BaseSelector()
        initial_options = InitialOptions
        self.selector.initialize_maps(initial_options)

    def test_initialize_maps(self):
        expected_option_map = {
            "Option1": {"data": "some_data1"},
            "Option2": {"data": "some_data2"},
        }
        expected_option_index = {0: "Option1", 1: "Option2"}
        self.assertEqual(self.selector.option_map, expected_option_map)
        self.assertEqual(self.selector.option_index, expected_option_index)

    def test_select(self):
        selected = self.selector.select("Option1")
        self.assertEqual(selected, {"data": "some_data1"})
        self.assertEqual(self.selector.embedding, {"data": "some_data1"})

    def test_add(self):
        new_option = {"new_option": {"new_data": "some_new_data"}}
        self.selector.add(new_option)
        self.assertEqual(self.selector.option_map["new_option"], new_option)
        self.assertEqual(self.selector.option_index[3], "new_option")

    def test_get_maps(self):
        option_map, option_index = self.selector.get_maps()
        self.assertEqual(
            option_map,
            {"Option1": {"data": "some_data1"}, "Option2": {"data": "some_data2"}},
        )
        self.assertEqual(option_index, {0: "Option1", 1: "Option2"})


if __name__ == "__main__":
    unittest.main()
