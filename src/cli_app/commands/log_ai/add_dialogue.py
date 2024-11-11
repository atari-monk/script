from pydantic import ValidationError
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.dialogue_crud import DialogueCRUD
from commands.log_ai.lib.model.dialogue import Dialogue

class AddDialogCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.dialog_crud = DialogueCRUD()

    def execute(self, *args):
        if len(args) < 2:
            print("Usage: add_dialogue <action> <dialogue_id (optional)> <text>")
            return

        action = args[0].lower()

        if action == "add":
            self.add_dialogue(args[1:])
        elif action == "edit":
            self.edit_dialogue(args[1:])
        elif action == "delete":
            self.delete_dialogue(args[1:])
        else:
            print("Error: Invalid action. Use 'add' to create, 'edit' to update, or 'delete' to remove a dialogue.")

    def add_dialogue(self, args):
        if len(args) < 1:
            print("Usage: add_dialogue add <text>")
            return

        text = args[0]

        try:
            validated_dialogue = Dialogue(
                text=text
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        try:
            result = self.dialog_crud.create(
                text=validated_dialogue.text,
                timestamp=validated_dialogue.timestamp
            )
            if result:
                print(f"Dialogue added successfully with id '{result['id']}'.")
            else:
                print("Failed to add dialogue.")
        except Exception as e:
            print(f"Unexpected error during dialogue addition: {e}")

    def edit_dialogue(self, args):
        if len(args) < 2:
            print("Usage: add_dialogue edit <dialogue_id> <text>")
            return

        dialogue_id, new_text = args[0], args[1]

        # Fetch the current dialogue to validate the ID and make sure it exists
        existing_dialogue = self.dialog_crud.get_by_id(dialogue_id)
        if not existing_dialogue:
            print(f"Error: Dialogue with ID '{dialogue_id}' not found.")
            return

        # Update the dialogue's text
        existing_dialogue['text'] = new_text

        try:
            validated_dialogue = Dialogue(
                text=existing_dialogue['text'],
                timestamp=existing_dialogue['timestamp']
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        # Update the dialogue in the database
        try:
            result = self.dialog_crud.update(
                dialogue_id,
                validated_dialogue.text,
                validated_dialogue.timestamp
            )
            if result:
                print(f"Dialogue '{dialogue_id}' updated successfully.")
            else:
                print("Failed to update dialogue.")
        except Exception as e:
            print(f"Unexpected error during dialogue update: {e}")

    def delete_dialogue(self, args):
        if len(args) < 1:
            print("Usage: add_dialogue delete <dialogue_id>")
            return

        dialogue_id = args[0]

        # Check if the dialogue exists before attempting to delete
        existing_dialogue = self.dialog_crud.get_by_id(dialogue_id)
        if not existing_dialogue:
            print(f"Error: Dialogue with ID '{dialogue_id}' not found.")
            return

        # Attempt to delete the dialogue
        try:
            result = self.dialog_crud.delete(dialogue_id)
            if result:
                print(f"Dialogue '{dialogue_id}' deleted successfully.")
            else:
                print(f"Failed to delete dialogue '{dialogue_id}'.")
        except Exception as e:
            print(f"Unexpected error during dialogue deletion: {e}")

    @property
    def description(self):
        return "Add, edit, or delete a dialogue. Use 'add' to create, 'edit' to update, or 'delete' to remove a dialogue."
