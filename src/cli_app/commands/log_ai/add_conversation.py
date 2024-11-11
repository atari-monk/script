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
        if len(args) < 2:
            print("Usage: add_conversation <action> <conversation_id (optional)> <name> <description>")
            return

        action = args[0].lower()

        if action == "add":
            self.add_conversation(args[1:])
        elif action == "edit":
            self.edit_conversation(args[1:])
        else:
            print("Error: Invalid action. Use 'add' to create or 'edit' to update a conversation.")

    def add_conversation(self, args):
        if len(args) < 2:
            print("Usage: add_conversation add <name> <description>")
            return

        name, description = args[0], args[1]

        try:
            validated_conversation = Conversation(
                name=name,
                description=description
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

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

    def edit_conversation(self, args):
        if len(args) < 3:
            print("Usage: add_conversation edit <conversation_id> <name or 'none'> <description or 'none'>")
            return

        conversation_id, name, description = args[0], args[1], args[2]

        # Fetch the current conversation to validate the ID and make sure it exists
        existing_conversation = self.conversation_crud.get_by_id(conversation_id)
        if not existing_conversation:
            print(f"Error: Conversation with ID '{conversation_id}' not found.")
            return

        # Update only the fields that are provided (not 'none')
        if name != "none":
            existing_conversation['name'] = name
        if description != "none":
            existing_conversation['description'] = description

        try:
            validated_conversation = Conversation(
                name=existing_conversation['name'],
                description=existing_conversation['description'],
                start_timestamp=existing_conversation['start_timestamp'],
                last_mod_timestamp=existing_conversation['last_mod_timestamp']
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        # Update the conversation in the database
        try:
            result = self.conversation_crud.update(
                conversation_id,
                validated_conversation.name,
                validated_conversation.description,
                validated_conversation.start_timestamp,
                validated_conversation.last_mod_timestamp
            )
            if result:
                print(f"Conversation '{conversation_id}' updated successfully.")
            else:
                print("Failed to update conversation.")
        except Exception as e:
            print(f"Unexpected error during conversation update: {e}")

    @property
    def description(self):
        return "Add or edit a conversation. Use 'add' to create or 'edit' to update a conversation."
