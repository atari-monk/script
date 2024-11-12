from typing import Type, Optional, List, Dict
import logging
from .json_storage import JSONStorage

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CRUD:
    def __init__(self, model: Type[dict], storage: JSONStorage):
        self.model = model  # model is now a dictionary type
        self.storage = storage

    def create(self, instance: object) -> Optional[Dict]:
        """Creates a new entry and adds it to the storage using a model instance."""
        try:
            # Convert the instance's attributes to a dictionary
            item_data = instance.__dict__

            # Ensure the dictionary is valid, e.g., removing any private or unwanted attributes
            item_data = {key: value for key, value in item_data.items() if not key.startswith('_')}
            
            # Read existing data from storage
            items = self.storage.read_data(model=self.model)  # Pass the model class for deserialization

            # Assign a unique ID based on the highest existing ID + 1
            item_id = max([item.id for item in items], default=0) + 1
            item_data['id'] = item_id
            
            # Append the new item to the list
            items.append(self.model.from_dict(item_data))  # Use model's `from_dict` for consistency
            
            # Write updated data back to storage
            self.storage.write_data(items)

            logging.info(f"Item with ID {item_id} created successfully.")
            return item_data

        except Exception as e:
            logging.error(f"Error creating item: {e}")
            return None

    def read(self, item_id: int) -> Optional[Dict]:
        """Reads a single item by its ID."""
        try:
            items = self.storage.read_data(model=self.model)
            item = next((item for item in items if item.get('id') == item_id), None)
            
            if item is None:
                logger.error(f"Item with ID {item_id} not found.")
            return item.to_dict() if item else None  # Convert to dictionary for output

        except Exception as e:
            logger.error(f"Error reading data: {e}")
            return None

    def update(self, item_id: int, **data) -> bool:
        """Updates an item by its ID with provided data."""
        try:
            items = self.storage.read_data(model=self.model)
            updated = False
            for item in items:
                if item.get('id') == item_id:
                    for key, value in data.items():
                        setattr(item, key, value)
                    updated = True
                    break
            
            if updated:
                self.storage.write_data(items)
                logger.info(f"Item {item_id} updated successfully.")
                return True
            else:
                logger.error(f"Failed to update item with ID {item_id}. Item not found.")
                return False

        except Exception as e:
            logger.error(f"Unexpected error during update: {e}")
            return False

    def delete(self, item_id: int) -> bool:
        """Deletes an item by its ID."""
        try:
            items = self.storage.read_data(model=self.model)
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
            items = self.storage.read_data(model=self.model)
            return [item.to_dict() for item in items]  # Convert each item to dictionary

        except Exception as e:
            logger.error(f"Error listing data: {e}")
            return []
