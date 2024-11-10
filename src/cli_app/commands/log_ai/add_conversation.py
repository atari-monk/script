from pydantic import ValidationError
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.conversation_crud import ConversationCRUD
from commands.log_ai.lib.model.conversation import Conversation

class AddConversationCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.conversation_crud = ConversationCRUD()

    def execute(self, *args):
        # Check for minimum required arguments
        if len(args) < 2:
            print("Usage: add_conversation <name> <description>")
            return

        # Extract required arguments
        name, description = args[0], args[1]

        # Validate the conversation data
        try:
            # No need to manually set the timestamps here; they'll be automatically handled by the model
            validated_conversation = Conversation(
                name=name,
                description=description
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to create the conversation with validated data
        try:
            result = self.conversation_crud.create(
                name=validated_conversation.name,
                description=validated_conversation.description,
                start_timestamp=validated_conversation.start_timestamp,
                last_mod_timestamp=validated_conversation.last_mod_timestamp
            )
            if result:
                print(f"Conversation '{result['name']}' created successfully with id '{result['id']}'.")
            else:
                print("Failed to create conversation.")
        except Exception as e:
            print(f"Unexpected error during conversation creation: {e}")

    @property
    def description(self):
        return "Add a new conversation to the database, requiring a name and description."
