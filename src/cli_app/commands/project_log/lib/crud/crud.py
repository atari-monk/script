from typing import Type, TypeVar, Optional, List, Dict
from pydantic import BaseModel, ValidationError
from .json_storage import JSONStorage
import logging

T = TypeVar('T', bound=BaseModel)  # Generic type for Pydantic models

logger = logging.getLogger(__name__)

class CRUD:
    def __init__(self, model: Type[T], storage: JSONStorage):
        self.model = model
        self.storage = storage

    def create(self, **data) -> Optional[Dict]:
        """Creates a new entry and adds it to the storage."""
        try:
            # Validate and create model instance
            item = self.model(**data)
            item_data = item.model_dump()  # Pydantic v2.x, use .dict() for v1.x
            items = self.storage.read_data()
            
            # Assign a unique ID
            item_id = len(items) + 1
            item_data['id'] = item_id
            
            # Append the new item
            items.append(item_data)
            self.storage.write_data(items)
            
            return item_data

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return None

    def read(self, item_id: int) -> Optional[Dict]:
        """Reads a single item by its ID."""
        items = self.storage.read_data()
        item = next((item for item in items if item.get('id') == item_id), None)
        if item is None:
            logger.error(f"Item with ID {item_id} not found.")
        return item

    def update(self, item_id: int, **data) -> bool:
        """Updates an item by its ID with provided data."""
        items = self.storage.read_data()
        for item in items:
            if item.get('id') == item_id:
                # Update fields if they are valid attributes of the model
                for key, value in data.items():
                    if key in self.model.model_fields:
                        item[key] = value
                self.storage.write_data(items)
                logger.info(f"Item {item_id} updated successfully.")
                return True
        logger.error(f"Failed to update item with ID {item_id}.")
        return False

    def delete(self, item_id: int) -> bool:
        """Deletes an item by its ID."""
        items = self.storage.read_data()
        updated_items = [item for item in items if item.get('id') != item_id]
        
        if len(updated_items) == len(items):
            logger.error(f"Item with ID {item_id} not found.")
            return False
        
        self.storage.write_data(updated_items)
        logger.info(f"Item with ID {item_id} deleted.")
        return True

    def list_all(self) -> List[Dict]:
        """Lists all items."""
        return self.storage.read_data()
