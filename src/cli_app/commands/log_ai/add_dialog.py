from base.base_command import BaseCommand
from .lib.singletons import db_context
from .lib.singletons import parsing_utils
import pyperclip  # Import pyperclip to interact with the clipboard

class AddDialogCommand(BaseCommand):
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

        # Ask the user to copy the message to clipboard and then paste it
        print("Please copy the message content to your clipboard (in Markdown format), and then press Enter when ready.")
        input("Press Enter to continue...")  # Wait for user input to confirm they have copied the message

        try:
            message = pyperclip.paste()  # Get clipboard content for the message
        except Exception as e:
            print(f"Error: Failed to read clipboard. {e}")
            return

        # Optionally, parse and clean the Markdown content, e.g., removing unnecessary whitespace or formatting
        message = self.parse_markdown(message)

        # Ask the user to copy the response to clipboard and then paste it
        print("Please copy the response content to your clipboard (in Markdown format), and then press Enter when ready.")
        input("Press Enter to continue...")  # Wait for user input to confirm they have copied the response

        try:
            response = pyperclip.paste()  # Get clipboard content for the response
        except Exception as e:
            print(f"Error: Failed to read clipboard. {e}")
            return

        # Optionally, parse and clean the Markdown content
        response = self.parse_markdown(response)

        # Add the new dialog
        new_dialog = db_context.add_dialog(
            conversation_id=conversation_id,
            message=message,
            response=response
        )

        print(f"New dialog has been added to conversation '{conversation_id}' in '{file_name}'.")
        #print(f"Message: {new_dialog['message']}")
        #print(f"Response: {new_dialog['response']}")

    @property
    def description(self):
        return "Adds a new dialog to an existing conversation within a database file."

    def parse_markdown(self, md_text):
        """Parses Markdown text and returns a formatted string for JSON"""
        # Here, we'll strip unnecessary whitespace, and if you want to keep Markdown formatting,
        # we can replace multiple newlines with a single one, or handle specific Markdown parsing.
        
        # Strip leading and trailing whitespace
        md_text = md_text.strip()

        # Optionally, you can handle Markdown in more advanced ways if needed, like converting links, 
        # bold/italic text, etc., but for simplicity, we're just cleaning up whitespace.

        # Replace multiple newlines with a single newline (for better formatting in JSON)
        md_text = '\n'.join(md_text.splitlines())

        return md_text
