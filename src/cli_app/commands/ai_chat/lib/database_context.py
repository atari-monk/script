import os
import json
from .config import DATABASE_PATH  # Assuming DATABASE_PATH is imported from config.py

class DatabaseContext:
    def __init__(self):
        self.file_name = None  # To store the current database file name
        self.file_path = None  # To store the full path of the database file
        self.data = None  # The current loaded database data (dictionary)
    
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

    def add_project(self, project_name):
        """Add a new project to the loaded database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        
        # Generate new project_id (next available ID based on existing projects)
        projects = self.data.get("projects", [])
        new_project_id = str(len(projects) + 1)  # Simple approach, can be adjusted for more complex ID generation

        new_project = {
            "project_id": new_project_id,
            "name": project_name
        }

        projects.append(new_project)
        self.data["projects"] = projects
        self.save_data()
        return new_project  # Return the added project data

    def get_projects(self):
        """Retrieve all projects from the database."""
        if not self.data:
            raise ValueError("No database loaded. Please load a database file first.")
        return self.data.get("projects", [])
