from typing import Dict, List, Any, Tuple
import loguru

logger = loguru.logger


class BaseSelector:
    def __init__(self):
        logger.info("Initializing BaseSelector")
        self.embedding: Any
        self.option_map: Dict[str, Any] = {}
        self.option_index: Dict[int, str] = {}

    def initialize_maps(self, options: List[Any]):
        """Initialize option maps."""
        logger.info("Initializing BaseSelector")
        for i, option in enumerate(options):
            self.option_map[option.name] = option
            self.option_index[i] = option.name

    def select(self, name: str):
        """Select an option by its name."""
        logger.info(f"Selecting {name}")
        self.embedding = self.option_map.get(name, None)
        return self.embedding

    def add(self, option: Any):
        """Add a new option."""
        logger.info(f"Adding {option.name}")
        self.option_map[option.name] = option
        self.option_index[len(self.option_map) - 1] = option.name

    def get_maps(self) -> Tuple[Dict[str, Any], Dict[int, str]]:
        """Return the current option map and option index."""
        return self.option_map, self.option_index
