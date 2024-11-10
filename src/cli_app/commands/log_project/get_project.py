from base.base_command import BaseCommand
from .lib.crud.project_crud import ProjectCRUD

class GetProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        # Check if project ID is provided
        if len(args) < 1:
            print("Usage: get_project <project_id>")
            return

        # Parse and validate project ID
        try:
            project_id = int(args[0])
        except ValueError:
            print("Error: Project ID must be an integer.")
            return

        # Retrieve and display the project
        project = self.project_crud.read(project_id)
        if project:
            print("Project Details:")
            for key, value in project.items():
                print(f"{key}: {value}")
        else:
            print(f"Project with ID {project_id} not found.")

    @property
    def description(self):
        return "Retrieve and display a project by its ID."
