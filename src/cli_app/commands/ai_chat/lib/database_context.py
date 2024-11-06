import os
import json
from .constants import DATABASE_PATH  # Assuming DATABASE_PATH is imported from config.py

class DatabaseContext:
    def __init__(self):
        self.file_name = None
        self.file_path = None
        self.data = None
    
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
        max_id = max(int(item["project_id"]) for item in items)
        return str(max_id + 1)

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
