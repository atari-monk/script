from base.base_command import BaseCommand
from .database_config import db_context

class CreateNewDBCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        file_name = input("Enter the new database file name (e.g., conversation_01.json): ")

        # Prepare the empty structure for the database
        conversation_data = {
            "conversations": [],
            "projects": [],
            "tags": []
        }

        # Set the file in the context
        try:
            db_context.set_file(file_name)  # Try to load the file
        except FileNotFoundError:
            # If the file doesn't exist, proceed with creating a new file
            db_context.data = conversation_data  # Assign empty data
            db_context.save_data()  # Save the new empty file

        print(f"New database '{file_name}' created in the folder '{db_context.file_path}'.")

    @property
    def description(self):
        return "Creates a new database file in a fixed folder with an empty structure for storing conversations, projects, and tags."
