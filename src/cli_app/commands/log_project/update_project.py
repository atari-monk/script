from base.base_command import BaseCommand
from .lib.crud.project_crud import ProjectCRUD
from pydantic import ValidationError
from .lib.model.project import Project

class UpdateProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        # Ensure minimum arguments (project_id and at least one field to update)
        if len(args) < 2:
            print("Usage: update_project <project_id> <field1=value1> <field2=value2> ...")
            return

        project_id = int(args[0])  # The first argument is the project ID

        # Prepare a dictionary to store the updated fields
        update_data = {}

        # Parse the remaining arguments to fill the update_data dictionary
        for arg in args[1:]:
            try:
                field, value = arg.split("=")
                update_data[field] = value
            except ValueError:
                print(f"Invalid argument format: '{arg}'. Use 'field=value'.")
                return

        # Retrieve the existing project by ID
        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Project with ID {project_id} not found.")
            return

        # Create a validated project instance using the existing data and the update data
        try:
            # Pass existing data as defaults, overriding with the update data
            updated_project = Project(**{**existing_project, **update_data})
        except ValidationError as e:
            print("Error: Invalid input data for update.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to update the project
        try:
            # Use the CRUD's update method to apply the changes
            result = self.project_crud.update(project_id, **update_data)
            if result:
                print(f"Project '{updated_project.name}' updated successfully.")
            else:
                print("Failed to update project.")
        except Exception as e:
            print(f"Unexpected error during project update: {e}")

    @property
    def description(self):
        return "Update an existing project in the database. Only specify the fields you want to update."
