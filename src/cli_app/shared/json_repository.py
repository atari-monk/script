import logging
from .jsonl_file_storage import JSONLFileStorage
from .i_storage import IStorage

logger = logging.getLogger(__name__)

class JSONRepository:
    def __init__(self, model, storage: IStorage):
        self.model = model
        self.storage = storage

    def add_item(self, item_data: dict) -> dict:
        if isinstance(self.storage, JSONLFileStorage):
            return self.jsonl_add_item(item_data)

        # Default flow for other storage types (like JSONFileStorage)
        items = self.storage.load_all(self.model)
        item_data['id'] = self._get_new_id(items)
        items.append(self.model.from_dict(item_data))
        self.storage.save_all(items)
        logger.info(f"Item with ID {item_data['id']} created successfully.")
        return item_data

    def jsonl_add_item(self, item_data: dict) -> dict:
        """Handles adding an item to JSONL storage."""
        item_data['id'] = self._get_new_id()
        self.storage.append(self.model.from_dict(item_data))  # Appending to JSONL storage
        logger.info(f"Item with ID {item_data['id']} appended successfully.")
        return item_data

    def _get_new_id(self, existing_items=None) -> int:
        """Helper method to get the next ID for a new item."""
        if existing_items is None:
            existing_items = self.storage.load_all(self.model)
        return max((item.id for item in existing_items), default=0) + 1

    def get_by_id(self, item_id: int) -> dict:
        """Reads a single item by its ID."""
        items = self.storage.load_all (self.model)
        item = next((item for item in items if item.id == item_id), None)
        
        if item:
            return item.to_dict()
        logger.error(f"Item with ID {item_id} not found.")
        return {}

    def update_by_id(self, item_id: int, **data) -> bool:
        items = self.storage.load_all(self.model)
        for index, item in enumerate(items):
            if item.id == item_id:
                updated_data = {**item.to_dict(), **data}  # Merge current and new data
                try:
                    # Reinitialize item with validated data
                    items[index] = self.model.from_dict(updated_data)
                    self.storage.save_all(items)
                    logger.info(f"Item {item_id} updated successfully.")
                    return True
                except Exception as e:
                    logger.error(f"Validation failed for item {item_id}: {e}")
                    return False
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
