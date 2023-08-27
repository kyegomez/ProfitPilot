from typing import Dict, Any, Tuple, Union
from pydantic import BaseModel
from enum import Enum, EnumMeta
import loguru

logger = loguru.logger


class BaseSelector:
    def __init__(self, name=""):
        logger.info("Initializing BaseSelector")
        self.option_map: Dict[str, Dict[str, Any]] = {}
        self.option_index: Dict[int, str] = {}
        self.option_name = self.select(name)

    def initialize_maps(self, options: EnumMeta):
        logger.info("Initializing BaseSelector")

        init_options = {
            name: member.value for name, member in options.__members__.items()
        }

        for i, (option_name, option_value) in enumerate(init_options.items()):
            logger.info(f"Mapping Name: {option_name}, Value: {option_value}")
            self.option_map[option_name] = option_value
            self.option_index[i] = option_name

    def select(self, name: str):
        logger.info(f"Selecting {name}")
        self.option = self.option_map.get(name, None)
        return self.option

    def add(self, option: Dict[str, Any]):
        logger.info(f"Adding {option}")
        option_name = list(option.keys())[0]
        self.option_map[option_name] = option
        self.option_index[len(self.option_map)] = option_name

    def get_maps(self) -> Tuple[Dict[str, Any], Dict[int, str]]:
        """Return the current option map and option index."""
        return self.option_map, self.option_index
