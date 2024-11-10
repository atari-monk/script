from base.base_command import BaseCommand
from ...libs.crud.project_crud import ProjectCRUD
from pydantic import ValidationError
from ...libs.model.project import Project

class AddProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        # Check for minimum required arguments
        if len(args) < 2:
            print("Usage: add_project <project_name> <project_description>")
            return

        project_name, project_description = args[0], args[1]

        # Validate the project data
        try:
            validated_project = Project(name=project_name, description=project_description)
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to create the project with validated data
        try:
            result = self.project_crud.create(name=validated_project.name, description=validated_project.description)
            if result:
                print(f"Project '{result['name']}' created successfully with ID: {result['id']}")
            else:
                print("Failed to create project.")
        except Exception as e:
            print(f"Unexpected error during project creation: {e}")

    @property
    def description(self):
        return "Add a new project to the database with a name and description."