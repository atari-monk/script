from base.base_command import BaseCommand
from .lib.singletons import db_context
from .lib.singletons import parsing_utils

class AddTagCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate the arguments
        if not parsing_utils.validate_args(args, 2, ['file_name', 'tag_name']):
            return

        # Extract file name and tag name from args
        file_name, tag_name = args

        # Ensure the file name has a '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

        # Set the file in the database context
        try:
            db_context.set_file(file_name)  # Try to load the file
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist in the database.")
            return

        # Add the new tag
        new_tag = db_context.add_tag(tag_name)

        print(f"New tag '{tag_name}' with ID '{new_tag['tag_id']}' has been added to '{file_name}'.")

    @property
    def description(self):
        return "Adds a new tag to an existing database file with an automatically assigned unique tag ID."
