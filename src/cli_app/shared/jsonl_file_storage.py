import json
import os
import logging
from .i_storage import IStorage

logger = logging.getLogger(__name__)

class JSONLFileStorage(IStorage):
    """Handles reading and writing line-delimited JSON (JSONL) format."""
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.save_all([])  # Create an empty file if it doesn't exist

    def load_all(self, model):
        """Reads each line in a JSONL file and converts it to model instances."""
        instances = []
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    instances.append(model.from_dict(data))
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error reading from {self.file_path}: {e}")
        return instances

    def save_all(self, instances):
        """Writes each model instance as a separate line in the JSONL file."""
        try:
            with open(self.file_path, 'w') as f:
                for instance in instances:
                    json_line = json.dumps(instance.to_dict())
                    f.write(json_line + '\n')
            logger.info(f"Data successfully written to {self.file_path}")
        except IOError as e:
            logger.error(f"Error writing to {self.file_path}: {e}")

    def append(self, instance):
        """Appends a model instance to the JSONL file."""
        try:
            with open(self.file_path, 'a') as f:  # Open file in append mode
                f.write(json.dumps(instance.to_dict()) + "\n")
            logger.info(f"Appended data to {self.file_path}")
        except IOError as e:
            logger.error(f"Error appending to {self.file_path}: {e}")
            