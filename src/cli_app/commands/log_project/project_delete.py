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

        action = args[0].lower()
        if action == "delete":
            self.delete_project(args[1:])
        else:
            print("Error: Invalid action. Use 'delete' to remove a project.")
            self.print_usage()

    def delete_project(self, args):
        if len(args) < 1:
            print("Usage: project delete <project_id>")
            return

        project_id = args[0]

        # Fetch the project to ensure it exists
        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        try:
            # Perform the deletion
            result = self.project_crud.delete(project_id)
            if result:
                print(f"Project '{project_id}' deleted successfully.")
            else:
                print(f"Failed to delete project '{project_id}'.")
        except Exception as e:
            print(f"Unexpected error during project deletion: {e}")

    def print_usage(self):
        print("""
Usage: project delete <project_id>
Actions:
- delete: Remove a project by specifying its project ID.

Example:
- To delete a project:
  project delete 123
""")
    
    @property
    def description(self):
        return "Delete a project by its ID."
