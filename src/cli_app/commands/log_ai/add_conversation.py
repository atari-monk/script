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
            print("Usage: add_conversation <name> <description> [<project_id> <tags_id> <start_timestamp> <last_mod_timestamp>]")
            return

        # Extract required arguments
        name, description = args[0], args[1]
        
        # Extract optional arguments if provided
        project_id = args[2] if len(args) > 2 else None
        tags_id = args[3] if len(args) > 3 else None
        start_timestamp = args[4] if len(args) > 4 else None
        last_mod_timestamp = args[5] if len(args) > 5 else None

        # Validate the conversation data
        try:
            validated_conversation = Conversation(
                name=name,
                description=description,
                project_id=project_id,
                tags_id=tags_id,
                start_timestamp=start_timestamp,
                last_mod_timestamp=last_mod_timestamp
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
                project_id=validated_conversation.project_id,
                tags_id=validated_conversation.tags_id,
                start_timestamp=validated_conversation.start_timestamp,
                last_mod_timestamp=validated_conversation.last_mod_timestamp,
                dialogues=validated_conversation.dialogues
            )
            if result:
                print(f"Conversation '{result['name']}' created successfully.")
            else:
                print("Failed to create conversation.")
        except Exception as e:
            print(f"Unexpected error during conversation creation: {e}")

    @property
    def description(self):
        return "Add a new conversation to the database with a name, description, and optional project ID, tag ID, and timestamps."
