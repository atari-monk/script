from base.base_command import BaseCommand
from .lib.crud.project_crud import ProjectCRUD  # Import ProjectCRUD
from pydantic import BaseModel, Field, field_validator, ValidationError

class AddProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()  # Initialize ProjectCRUD

    def execute(self, *args):
        # Ensure the user provided both project name and description
        if len(args) < 2:
            print("Usage: add_project <project_name> <project_description>")
            return

        project_name = args[0]
        project_description = args[1]

        # Validate input using Pydantic
        try:
            validated_project = ProjectInput(name=project_name, description=project_description)
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e)  # Print the validation error details
            return

        # Use ProjectCRUD to create the project if input is valid
        result = self.project_crud.create_project(validated_project.name, validated_project.description)

        # Print result of the creation
        if result:
            print(f"Project '{result['name']}' created successfully with ID: {result['id']}")
        else:
            print("Failed to create project.")

    @property
    def description(self):
        return "Add Project"

# Pydantic Model to validate project input using @field_validator
class ProjectInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=255)

    @field_validator('name')
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Project name must not be empty.")
        if not value.isalnum() and not all(c.isspace() for c in value):  # Allow spaces, alphanumeric characters only
            raise ValueError("Project name must only contain alphanumeric characters and spaces.")
        return value

    @field_validator('description')
    def validate_description(cls, value):
        if len(value) > 255:
            raise ValueError("Project description cannot exceed 255 characters.")
        return value
