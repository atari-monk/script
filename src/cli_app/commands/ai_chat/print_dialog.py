from base.base_command import BaseCommand
from .lib.config import db_context
from .lib.config import parsing_utils

class PrintDialogCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Validate arguments: file_name, conversation_id
        if not parsing_utils.validate_args(args, 2, ['file_name', 'conversation_id']):
            return

        # Extract arguments
        file_name, conversation_id = args

        # Ensure file name has '.json' extension
        file_name = parsing_utils.validate_and_append_extension(file_name)

        # Load the specified database file
        try:
            db_context.set_file(file_name)
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist in the database.")
            return

        # Retrieve the conversation and its dialogs
        conversation = db_context.get_conversation(conversation_id)
        if not conversation:
            print(f"Error: Conversation with ID '{conversation_id}' not found.")
            return

        # Print all dialogs in the format: id - message:
        print("Dialogs in the conversation:")
        for dialog in conversation["dialogues"]:
            print(f"{dialog['dialog_id']} - {dialog['message']}")

        # Ask the user to select a dialog ID to view the details
        dialog_id_to_print = input("Enter dialog ID to view its message and response: ")
        dialog = next((d for d in conversation["dialogues"] if str(d["dialog_id"]) == dialog_id_to_print), None)

        if dialog:
            # Print the selected dialog's message and response
            print(f"\nDialog ID {dialog_id_to_print}:")
            print(f"Message: {dialog['message']}")
            print(f"Response: {dialog['response']}")
        else:
            print(f"Error: No dialog found with ID '{dialog_id_to_print}'.")

    @property
    def description(self):
        return "Prints all dialogs in a conversation and allows selection of a dialog ID to view its details."
