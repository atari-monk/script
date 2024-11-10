from base.base_command import BaseCommand
from ...libs.crud.project_crud import ProjectCRUD

class ListProjectsCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        # Retrieve all projects
        projects = self.project_crud.list_all()
        if projects:
            print("All Projects:")
            for project in projects:
                print("------------")
                for key, value in project.items():
                    print(f"{key}: {value}")
                print("------------")
        else:
            print("No projects found.")

    @property
    def description(self):
        return "List all projects in the database."
