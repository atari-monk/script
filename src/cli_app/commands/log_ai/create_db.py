from base.base_command import BaseCommand
from .lib.singletons import db_context
from .lib.singletons import parsing_utils

class CreateNewDBCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate the arguments
        if not parsing_utils.validate_args(args, 1, ['file_name']):
            return

        # Extract the file name from args
        file_name = args[0]

        # Ensure the file name has a '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

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
