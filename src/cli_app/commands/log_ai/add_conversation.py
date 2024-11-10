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
        if len(args) < 5:
            print("Usage: add_conversation <conversation_id> <project_id> <tags_id> <name> <description> <start_timestamp> <last_mod_timestamp>")
            return

        conversation_id, project_id, tags_id, name, description, start_timestamp, last_mod_timestamp = args[:7]

        # Validate the conversation data
        try:
            validated_conversation = Conversation(
                conversation_id=conversation_id,
                project_id=project_id,
                tags_id=tags_id,
                name=name,
                description=description,
                start_timestamp=start_timestamp,
                last_mod_timestamp=last_mod_timestamp,
                dialogues=[]
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to create the conversation with validated data
        try:
            result = self.conversation_crud.create(
                conversation_id=validated_conversation.conversation_id,
                project_id=validated_conversation.project_id,
                tags_id=validated_conversation.tags_id,
                name=validated_conversation.name,
                description=validated_conversation.description,
                start_timestamp=validated_conversation.start_timestamp,
                last_mod_timestamp=validated_conversation.last_mod_timestamp,
                dialogues=validated_conversation.dialogues
            )
            if result:
                print(f"Conversation '{result['name']}' created successfully with ID: {result['conversation_id']}")
            else:
                print("Failed to create conversation.")
        except Exception as e:
            print(f"Unexpected error during conversation creation: {e}")

    @property
    def description(self):
        return "Add a new conversation to the database with a project ID, tag ID, name, description, timestamps, and dialogues."
