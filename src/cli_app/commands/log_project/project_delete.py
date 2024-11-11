from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD

class ProjectDeleteCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 1:
            self.print_usage()
            return

        project_id = args[0]

        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        try:
            result = self.project_crud.delete(project_id)
            if result:
                print(f"Project '{project_id}' deleted successfully.")
            else:
                print(f"Failed to delete project '{project_id}'.")
        except Exception as e:
            print(f"Unexpected error during project deletion: {e}")

    def print_usage(self):
        print("""
Usage: command <project_id>

Example:
- To delete a project:
  command 123
""")
    
    @property
    def description(self):
        return "Delete a project by its ID."
