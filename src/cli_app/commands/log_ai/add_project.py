from base.base_command import BaseCommand
from .lib.config import db_context
from .lib.config import parsing_utils

class AddProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate the arguments
        if not parsing_utils.validate_args(args, 2, ['file_name', 'project_name']):
            return

        # Extract file name and project name from args
        file_name, project_name = args

        # Ensure the file name has a '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

        # Set the file in the database context
        try:
            db_context.set_file(file_name)  # Try to load the file
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist in the database.")
            return

        # Add the new project
        new_project = db_context.add_project(project_name)

        print(f"New project '{project_name}' with ID '{new_project['project_id']}' has been added to '{file_name}'.")

    @property
    def description(self):
        return "Adds a new project to an existing database file with an automatically assigned unique project ID."
