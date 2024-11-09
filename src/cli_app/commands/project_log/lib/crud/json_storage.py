import json
import os
from typing import List

class JSONStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Ensure the file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def read_data(self) -> List[dict]:
        """Reads the current data from the JSON file."""
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write_data(self, data: List[dict]):
        """Writes the data back to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
