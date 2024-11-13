import pytest
import json
import os
from cli_app.shared.json_file_storage import JSONFileStorage  # Replace with the actual path to your library

@pytest.fixture
def setup_and_teardown():
    """Fixture to set up the test environment and clean up after each test."""
    test_file = 'test_data.json'
    # Ensure the test file is removed before each test to avoid conflicts
    if os.path.exists(test_file):
        os.remove(test_file)
    
    yield test_file
    
    # Clean up after each test
    if os.path.exists(test_file):
        os.remove(test_file)

def test_initial_file_creation(setup_and_teardown):
    """Test that the file is created with an empty list if it doesn't exist."""
    test_file = setup_and_teardown
    storage = JSONFileStorage(test_file)
    
    # Check that the file exists
    assert os.path.exists(test_file)

    # Check that the file contains an empty list
    with open(test_file, 'r') as f:
        data = json.load(f)
        assert data == []

def test_read_data_empty(setup_and_teardown):
    """Test reading from a newly created empty file."""
    test_file = setup_and_teardown
    storage = JSONFileStorage(test_file)
    data = storage.load_all ()
    assert data == []

def test_write_data(setup_and_teardown):
    """Test writing data to the JSON file."""
    test_file = setup_and_teardown
    storage = JSONFileStorage(test_file)
    data_to_write = [{"key": "value"}]

    # Write data to the file
    storage.save_all(data_to_write)

    # Read the data back from the file
    with open(test_file, 'r') as f:
        data = json.load(f)
        assert data == data_to_write

def test_write_and_read_multiple_entries(setup_and_teardown):
    """Test writing and reading multiple entries."""
    test_file = setup_and_teardown
    storage = JSONFileStorage(test_file)
    data_to_write = [{"key": "value1"}, {"key": "value2"}]

    # Write data to the file
    storage.save_all(data_to_write)

    # Read the data back from the file
    data = storage.load_all ()
    assert data == data_to_write

def test_read_data_with_invalid_json(setup_and_teardown):
    """Test reading from a file with invalid JSON."""
    test_file = setup_and_teardown
    # Manually corrupt the JSON file for this test
    with open(test_file, 'w') as f:
        f.write("{invalid json}")

    storage = JSONFileStorage(test_file)
    data = storage.load_all ()
    
    # Assert that the data returned is an empty list (error handling should ensure this)
    assert data == []

def test_write_data_error_handling(setup_and_teardown):
    """Test handling errors when writing to a file (e.g., permission issues)."""
    test_file = setup_and_teardown
    storage = JSONFileStorage(test_file)
    data_to_write = [{"key": "value"}]
    storage.save_all(data_to_write)

    # Set the file to read-only to simulate a write error
    os.chmod(test_file, 0o444)  # Read-only permission

    # Try writing data and expect a logged error (logging itself cannot be easily tested, but we check file contents)
    storage.save_all(data_to_write)

    # Read the data and ensure it hasn't changed
    with open(test_file, 'r') as f:
        data = json.load(f)
        assert data == data_to_write  # Check that data remains unchanged

    # Reset the file permission for further tests
    os.chmod(test_file, 0o666)
