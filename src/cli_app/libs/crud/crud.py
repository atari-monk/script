from typing import Type, Optional, List, Dict
import logging
from .json_storage import JSONStorage

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CRUD:
    def __init__(self, model: Type[dict], storage: JSONStorage):
        self.model = model  # model is now a dictionary type
        self.storage = storage

    def create(self, **data) -> Optional[Dict]:
        """Creates a new entry and adds it to the storage."""
        try:
            # Assuming `data` is a dictionary or is already validated
            item_data = data
            
            items = self.storage.read_data()
            
            # Assign a unique ID based on the highest existing ID + 1
            item_id = max([item.get('id', 0) for item in items], default=0) + 1
            item_data['id'] = item_id
            
            # Append the new item
            items.append(item_data)
            self.storage.write_data(items)
            
            logger.info(f"Item with ID {item_id} created successfully.")
            return item_data

        except Exception as e:
            logger.error(f"Unexpected error during creation: {e}")
            return None

    def read(self, item_id: int) -> Optional[Dict]:
        """Reads a single item by its ID."""
        try:
            item_id = int(item_id)  # Ensure item_id is an integer
            items = self.storage.read_data()
            item = next((item for item in items if item.get('id') == item_id), None)
            
            if item is None:
                logger.error(f"Item with ID {item_id} not found.")
            return item
        except ValueError:
            logger.error(f"Invalid item_id: {item_id} is not an integer.")
            return None
        except Exception as e:
            logger.error(f"Error reading data: {e}")
            return None

    def update(self, item_id: int, **data) -> bool:
        """Updates an item by its ID with provided data."""
        try:
            item_id = int(item_id)
            items = self.storage.read_data()
            for item in items:
                if item.get('id') == item_id:
                    # Update the item fields with the provided data
                    item.update(data)  # Directly update the dictionary
                    self.storage.write_data(items)
                    logger.info(f"Item {item_id} updated successfully.")
                    return True
            
            logger.error(f"Failed to update item with ID {item_id}. Item not found.")
            return False

        except Exception as e:
            logger.error(f"Unexpected error during update: {e}")
            return False

    def delete(self, item_id: int) -> bool:
        """Deletes an item by its ID."""
        try:
            item_id = int(item_id)
            items = self.storage.read_data()
            updated_items = [item for item in items if item.get('id') != item_id]
            
            if len(updated_items) == len(items):
                logger.error(f"Item with ID {item_id} not found.")
                return False
            
            self.storage.write_data(updated_items)
            logger.info(f"Item with ID {item_id} deleted.")
            return True

        except Exception as e:
            logger.error(f"Unexpected error during deletion: {e}")
            return False

    def list_all(self) -> List[Dict]:
        """Lists all items."""
        try:
            return self.storage.read_data()
        except Exception as e:
            logger.error(f"Error listing data: {e}")
            return []
