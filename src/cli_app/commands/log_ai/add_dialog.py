from pydantic import ValidationError
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.dialog_crud import DialogCRUD
from commands.log_ai.lib.model.dialog import Dialog
import pyperclip

class AddDialogCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.dialog_crud = DialogCRUD()

    def execute(self, *args):
        # Ensure the correct number of arguments
        if len(args) < 2:
            print("Usage: add_dialog <file_name> <conversation_id>")
            return

        file_name, conversation_id = args

        # Validate and prepare the file name
        file_name = self.validate_and_append_extension(file_name)

        # Load the specified database file
        if not self.load_file(file_name):
            return

        # Get the message content from clipboard
        print("Please copy the message content to your clipboard (in Markdown format), then press Enter.")
        input("Press Enter to continue...")
        try:
            message = self.get_clipboard_content("message")
        except Exception as e:
            print(f"Error: {e}")
            return

        # Get the response content from clipboard
        print("Please copy the response content to your clipboard (in Markdown format), then press Enter.")
        input("Press Enter to continue...")
        try:
            response = self.get_clipboard_content("response")
        except Exception as e:
            print(f"Error: {e}")
            return

        # Validate the dialog data
        try:
            validated_dialog = Dialog(
                message=message,
                response=response,
                conversation_id=conversation_id  # Added conversation_id to Dialog
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to add the new dialog
        try:
            result = self.dialog_crud.create(
                conversation_id=validated_dialog.conversation_id,
                message=validated_dialog.message,
                response=validated_dialog.response
            )
            if result:
                print(f"New dialog added to conversation '{conversation_id}'.")
            else:
                print("Failed to add dialog.")
        except Exception as e:
            print(f"Unexpected error during dialog creation: {e}")

    def validate_and_append_extension(self, file_name):
        """Validate the file name and append the correct extension if needed."""
        # Assuming you have a specific extension for your database files
        if not file_name.endswith(".db"):
            file_name += ".db"
        return file_name

    def load_file(self, file_name):
        """Load the specified database file."""
        # Add the logic to open and validate the database file here
        print(f"Loading database file: {file_name}")
        try:
            # Simulate loading the file (you can replace this with actual loading logic)
            # e.g., db.load(file_name)
            return True
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist.")
            return False

    def get_clipboard_content(self, content_type):
        """Retrieves and parses content from the clipboard."""
        try:
            content = pyperclip.paste().strip()
            return self.parse_markdown(content)
        except Exception:
            raise ValueError(f"Failed to retrieve {content_type} from clipboard.")

    def parse_markdown(self, md_text):
        """Cleans up Markdown content for JSON."""
        return '\n'.join(md_text.strip().splitlines())

    @property
    def description(self):
        return "Adds a new dialog to an existing conversation within a database file, linking it by conversation_id."
