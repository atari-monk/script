import json
import os
import logging
from typing import List, Type, TypeVar, Generic

logger = logging.getLogger(__name__)

T = TypeVar('T')

class JSONStorage(Generic[T]):
    def __init__(self, file_path: str, indent: int = 2):
        self.file_path = file_path
        self.indent = indent
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f, indent=self.indent)

    def read_data(self, model: Type[T]) -> List[T]:
        """Reads the current data from the JSON file and converts it to model instances."""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                
                return [model.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            logger.error(f"Error reading JSON from {self.file_path}: {e}")
            return []
        except IOError as e:
            logger.error(f"Error opening file {self.file_path}: {e}")
            return []

    def write_data(self, instances: List[T]):
        """Writes a list of model instances back to the JSON file."""
        try:
            instances_dicts = [instance.to_dict() for instance in instances]
            with open(self.file_path, 'w') as f:
                json.dump(instances_dicts, f, indent=self.indent)
            logger.info(f"Successfully wrote data to {self.file_path}")
        except IOError as e:
            logger.error(f"Error writing to file {self.file_path}: {e}")
