from unittest import TestCase
from unittest.mock import MagicMock
from ..project_crud import ProjectCRUD  # Ensure correct import path

class ProjectCRUDTest(TestCase):
    def test_create_project(self):
        # Mock the storage
        mock_storage = MagicMock()
        mock_storage.read_data.return_value = []  # Empty list as the initial state
        project_crud = ProjectCRUD()

        # Inject the mock storage into the ProjectCRUD instance
        project_crud.storage = mock_storage

        # Valid project data
        project_data = {'name': 'Test Project', 'description': 'Test description'}
        result = project_crud.create(**project_data)

        # Assert that the storage.write_data method was called once
        mock_storage.write_data.assert_called_once()

        # Assert that the returned project matches the expected data
        self.assertEqual(result['name'], 'Test Project')
        self.assertEqual(result['description'], 'Test description')
        # Check that the ID was assigned correctly
        self.assertEqual(result['id'], 1)  # As we are adding to an empty list, ID should be 1
