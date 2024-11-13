import pytest
from unittest.mock import MagicMock
from ..json_repository import JSONRepository  # Assuming CRUD is implemented for standard Python dicts

class ItemModel:
    def __init__(self, name: str, description: str):
        if not name or not description:
            raise ValueError("Both 'name' and 'description' are required.")
        self.name = name
        self.description = description
        self.id = None  # This will be set when the item is added to storage

    def to_dict(self):
        return {"name": self.name, "description": self.description, "id": self.id}


@pytest.fixture
def mock_storage():
    """Mock storage to simulate read and write."""
    mock = MagicMock()
    mock.read_data.return_value = []  # Start with an empty storage
    return mock

@pytest.fixture
def crud(mock_storage):
    """Provide CRUD instance with mocked storage."""
    return JSONRepository(dict, mock_storage)  # Use `dict` as model instead of Pydantic

def test_create(crud, mock_storage):
    """Test creating an item."""
    data = {"name": "Item 1", "description": "A test item"}
    
    # Call the create method
    result = crud.create(**data)
    
    # Verify the item was created with a unique ID
    assert result is not None
    assert result["name"] == "Item 1"
    assert result["description"] == "A test item"
    assert result["id"] == 1  # ID should be 1 since the storage is empty initially

    # Ensure storage was updated with the new item
    mock_storage.write_data.assert_called_once_with([result])

def test_read(crud, mock_storage):
    """Test reading an item by ID."""
    item_data = {"id": 1, "name": "Item 1", "description": "A test item"}
    mock_storage.read_data.return_value = [item_data]
    
    # Call the read method
    result = crud.read(1)
    
    # Verify the item was read correctly
    assert result is not None
    assert result["name"] == "Item 1"
    assert result["description"] == "A test item"

def test_update(crud, mock_storage):
    """Test updating an item."""
    item_data = {"id": 1, "name": "Item 1", "description": "A test item"}
    mock_storage.read_data.return_value = [item_data]
    
    # Call the update method
    updated_data = {"name": "Updated Item 1", "description": "Updated description"}
    result = crud.update(1, **updated_data)
    
    # Verify the item was updated
    assert result is True
    assert item_data["name"] == "Updated Item 1"
    assert item_data["description"] == "Updated description"
    
    # Ensure the storage was updated
    mock_storage.write_data.assert_called_once_with([item_data])

def test_delete(crud, mock_storage):
    """Test deleting an item."""
    item_data = {"id": 1, "name": "Item 1", "description": "A test item"}
    mock_storage.read_data.return_value = [item_data]
    
    # Call the delete method
    result = crud.delete(1)
    
    # Verify the item was deleted
    assert result is True
    mock_storage.write_data.assert_called_once_with([])  # Storage should be empty now

def test_list_all(crud, mock_storage):
    """Test listing all items."""
    item_data_1 = {"id": 1, "name": "Item 1", "description": "A test item"}
    item_data_2 = {"id": 2, "name": "Item 2", "description": "Another item"}
    mock_storage.read_data.return_value = [item_data_1, item_data_2]
    
    # Call the list_all method
    result = crud.list_all()
    
    # Verify all items are returned
    assert len(result) == 2
    assert result[0]["name"] == "Item 1"
    assert result[1]["name"] == "Item 2"

def test_update_item_not_found(crud, mock_storage):
    """Test updating an item that doesn't exist."""
    mock_storage.read_data.return_value = []  # No items in storage
    
    # Call the update method
    result = crud.update(999, name="Non-existent Item")
    
    # Verify that the result is False since the item was not found
    assert result is False
    mock_storage.write_data.assert_not_called()  # Storage should not be updated
