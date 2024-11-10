from base.base_command import BaseCommand
from .lib.singletons import db_context
from .lib.singletons import parsing_utils

class AddConversationCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate that all required arguments are provided
        if not parsing_utils.validate_args(args, 5, ['file_name', 'project_id', 'tags_id', 'name', 'description']):
            return

        # Extract arguments
        file_name, project_id, tags_id, name, description = args

        # Ensure file name has '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

        # Load the specified database file
        try:
            db_context.set_file(file_name)
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist in the database.")
            return

        # Convert tags_id if it is not already in list format
        if isinstance(tags_id, str):
            tags_id = tags_id.split(",")  # Split comma-separated string into list

        # Add the new conversation
        new_conversation = db_context.add_conversation(
            project_id=project_id,
            tags_id=tags_id,
            name=name,
            description=description
        )

        print(f"New conversation '{name}' has been added to '{file_name}' with ID '{new_conversation['conversation_id']}'.")

    @property
    def description(self):
        return "Adds a new conversation to an existing database file with specified project, tags, name, and description."
