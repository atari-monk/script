import logging
from .json_file_storage import JSONFileStorage

logger = logging.getLogger(__name__)

class JSONRepository:
    def __init__(self, model, storage: JSONFileStorage):
        self.model = model
        self.storage = storage

    def add_item(self, instance) -> dict:
        """Creates a new entry and adds it to the storage."""
        item_data = {key: value for key, value in vars(instance).items() if not key.startswith('_')}
        items = self.storage.load_all (self.model)
        
        item_data['id'] = max((item.id for item in items), default=0) + 1
        items.append(self.model.from_dict(item_data))
        
        self.storage.save_all(items)
        logger.info(f"Item with ID {item_data['id']} created successfully.")
        return item_data

    def get_by_id(self, item_id: int) -> dict:
        """Reads a single item by its ID."""
        items = self.storage.load_all (self.model)
        item = next((item for item in items if item.id == item_id), None)
        
        if item:
            return item.to_dict()
        logger.error(f"Item with ID {item_id} not found.")
        return {}

    def update_by_id(self, item_id: int, **data) -> bool:
        """Updates an item by its ID with provided data."""
        items = self.storage.load_all (self.model)
        for item in items:
            if item.id == item_id:
                for key, value in data.items():
                    setattr(item, key, value)
                self.storage.save_all(items)
                logger.info(f"Item {item_id} updated successfully.")
                return True
        logger.error(f"Item with ID {item_id} not found.")
        return False

    def delete_by_id(self, item_id: int) -> bool:
        """Deletes an item by its ID."""
        items = self.storage.load_all (self.model)
        updated_items = [item for item in items if item.id != item_id]
        
        if len(updated_items) < len(items):
            self.storage.save_all(updated_items)
            logger.info(f"Item with ID {item_id} deleted.")
            return True
        logger.error(f"Item with ID {item_id} not found.")
        return False

    def fetch_all(self) -> list:
        """Lists all items."""
        items = self.storage.load_all (self.model)
        return [item.to_dict() for item in items]
