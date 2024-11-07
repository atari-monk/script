import os
import json
from .constants import DATABASE_PATH

class DatabaseContext:
    def __init__(self, parsing_utils):
        self.file_name = None
        self.file_path = None
        self.data = None
        self.parsing_utils = parsing_utils

    def set_file(self, file_name):
        """Set the database file name and load its data."""
        self.file_name = file_name
        self.file_path = os.path.join(DATABASE_PATH, file_name)

        # Check if the file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Database file '{file_name}' not found in the folder '{DATABASE_PATH}'.")

        # Load the data from the file
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def get_data(self):
        """Retrieve the current data loaded from the database file."""
        if not self.data:
            raise ValueError("No database file loaded. Please load a file using set_file().")
        return self.data

    def save_data(self):
        """Save the current data back to the database file."""
        if not self.file_path or not self.data:
            raise ValueError("No data to save. Please load a file first.")
        
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def generate_new_id(self, key):
        """Generate the next available ID based on existing entries under a given key."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        items = self.data.get(key, [])
        if not items:
            return "1"  # If no items, start with ID "1"
        
        # Extract the highest existing ID (assuming all items have an integer 'id' field)
        max_id = max(int(item[f"{key[:-1]}_id"]) for item in items)  # Handles both "project_id" and "tag_id"
        return str(max_id + 1)

    def add_tag(self, tag_name):
        """Add a new tag to the loaded database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        new_tag_id = self.generate_new_id("tags")  # Use the new ID generation method for tags
        new_tag = {
            "tag_id": new_tag_id,
            "name": tag_name
        }

        # Add the tag to the database
        tags = self.data.get("tags", [])
        tags.append(new_tag)
        self.data["tags"] = tags

        # Save the data back to the file
        self.save_data()
        return new_tag

    def add_project(self, project_name):
        """Add a new project to the loaded database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        new_project_id = self.generate_new_id("projects")  # Use the new ID generation method
        new_project = {
            "project_id": new_project_id,
            "name": project_name
        }

        # Add the project to the database
        projects = self.data.get("projects", [])
        projects.append(new_project)
        self.data["projects"] = projects

        # Save the data back to the file
        self.save_data()
        return new_project  # Return the added project data

    def get_projects(self):
        """Retrieve all projects from the database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        return self.data.get("projects", [])

    def add_conversation(self, project_id, tags_id, name, description):
        """Add a new conversation to the loaded database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        new_conversation_id = self.generate_new_id("conversations")  # Generate a unique ID for the conversation
        new_conversation = {
            "conversation_id": new_conversation_id,
            "project_id": project_id,
            "tags_id": tags_id,
            "name": name,
            "description": description,
            "start_timestamp": self.parsing_utils.get_current_timestamp(),
            "last_mod_timestamp": self.parsing_utils.get_current_timestamp(),
            "dialogues": []  # Initialize as an empty list
        }

        # Add the conversation to the database
        conversations = self.data.get("conversations", [])
        conversations.append(new_conversation)
        self.data["conversations"] = conversations

        # Save the data back to the file
        self.save_data()
        return new_conversation
    
    def get_conversation(self, conversation_id):
        """Retrieve a conversation by its ID."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")

        # Find the conversation by its ID
        conversations = self.data.get("conversations", [])
        conversation = next((conv for conv in conversations if conv["conversation_id"] == conversation_id), None)

        if not conversation:
            raise ValueError(f"Conversation with ID '{conversation_id}' not found.")
        
        return conversation
    
    def add_dialog(self, conversation_id, message, response):
        """Add a dialog entry to a specific conversation with a unique dialog ID."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        # Find the conversation by its ID
        conversations = self.data.get("conversations", [])
        conversation = next((conv for conv in conversations if conv["conversation_id"] == conversation_id), None)

        if not conversation:
            raise ValueError(f"Conversation with ID '{conversation_id}' not found.")
        
        # Generate a new dialog ID for this entry
        new_dialog_id = self.generate_new_id("dialogues")  # Generate a new dialog ID

        # Create the new dialog entry
        new_dialog = {
            "dialog_id": new_dialog_id,
            "message": message,
            "response": response
        }

        # Add the new dialog to the conversation's dialogues
        conversation["dialogues"].append(new_dialog)
        conversation["last_mod_timestamp"] = self.parsing_utils.get_current_timestamp()  # Update timestamp

        # Save the updated data back to the file
        self.save_data()
        return new_dialog
