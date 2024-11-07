from base.base_command import BaseCommand
from .lib.config import db_context
from .lib.config import parsing_utils

class AddDialogCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate arguments: file_name, conversation_id, message, response
        if not parsing_utils.validate_args(args, 4, ['file_name', 'conversation_id', 'message', 'response']):
            return

        # Extract arguments
        file_name, conversation_id, message, response = args

        # Ensure file name has '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

        # Load the specified database file
        try:
            db_context.set_file(file_name)
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist in the database.")
            return

        # Add the new dialog
        new_dialog = db_context.add_dialog(
            conversation_id=conversation_id,
            message=message,
            response=response
        )

        print(f"New dialog has been added to conversation '{conversation_id}' in '{file_name}'.")
        print(f"Message: {new_dialog['message']}")
        print(f"Response: {new_dialog['response']}")

    @property
    def description(self):
        return "Adds a new dialog to an existing conversation within a database file."
