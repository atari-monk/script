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

        # Retrieve the current data from the database
        data = db_context.get_data()

        # Determine the highest existing project ID and increment it for the new project
        if data.get("projects"):
            max_project_id = max(int(project["project_id"]) for project in data["projects"])
            new_project_id = str(max_project_id + 1)
        else:
            # If no projects exist, start with ID "1"
            new_project_id = "1"

        # Create the new project
        new_project = {
            "project_id": new_project_id,
            "name": project_name
        }

        # Add the new project to the list of projects
        data["projects"].append(new_project)

        # Save the updated data back to the file through the database context
        db_context.save_data()

        print(f"New project '{project_name}' with ID '{new_project_id}' has been added to '{file_name}'.")

    @property
    def description(self):
        return "Adds a new project to an existing database file with an automatically assigned unique project ID."
