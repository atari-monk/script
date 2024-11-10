import json
import os
import logging
from typing import List

class JSONStorage:
    def __init__(self, file_path: str, indent: int = 2):
        self.file_path = file_path
        self.indent = indent
        # Ensure the file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f, indent=self.indent)
        # Set up logging
        logging.basicConfig(level=logging.INFO)

    def read_data(self) -> List[dict]:
        """Reads the current data from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error reading JSON from {self.file_path}: {e}")
            return []
        except IOError as e:
            logging.error(f"Error opening file {self.file_path}: {e}")
            return []

    def write_data(self, data: List[dict]):
        """Writes the data back to the JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=self.indent)
            logging.info(f"Successfully wrote data to {self.file_path}")
        except IOError as e:
            logging.error(f"Error writing to file {self.file_path}: {e}")
