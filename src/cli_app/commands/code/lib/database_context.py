import json
import os
from tkinter import messagebox
from .code_description import CodeDescription

class DatabaseContext:
    def __init__(self, db_path):
        self.db_path = db_path
        # Load the database from file (or initialize an empty one if not exists)
        self.load_db()

    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                self.db_data = json.load(f)
        else:
            # Initialize an empty database structure if file doesn't exist
            self.db_data = []
            self.save_db()

    def save_db(self):
        with open(self.db_path, "w") as f:
            json.dump(self.db_data, f, indent=2)

    def insert_description(self, description):
        # Insert a new description into the database
        self.db_data.append({
            "name": description.name,
            "description": description.description,
            "tags": description.tags
        })
        self.save_db()

    def update_description(self, description):
        # Update an existing description by its name
        for entry in self.db_data:
            if entry["name"] == description.name:
                entry["description"] = description.description
                entry["tags"] = description.tags
                self.save_db()
                return
        # If no existing description found, add it as a new entry
        self.insert_description(description)

    def get_all_descriptions(self):
        # Return all descriptions in the database
        return [CodeDescription(name=entry["name"], description=entry["description"], tags=entry["tags"]) for entry in self.db_data]

    def get_description_by_name(self, name):
        # Return a description by its name
        for entry in self.db_data:
            if entry["name"] == name:
                return CodeDescription(name=entry["name"], description=entry["description"], tags=entry["tags"])
        return None

    def get_all_tags(self):
        try:
            # Use a set to avoid duplicates
            tags = set()

            # Collect all tags from the descriptions already loaded in db_data
            for entry in self.db_data:
                tags.update(entry.get("tags", []))  # Add tags for each entry, if any

            tags.add("None")  # Ensure "None" is included in the tags

            # Return sorted tags
            return sorted(tags)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tags: {e}")
            return ["None"]  # Default value in case of error

    # Load configuration settings from JSON
    def load_config(self, file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")
            return {
                "font": {"font_family": "Arial", "font_size": 12},
                "paths": {"data_file": {"storage1": "data/code_descriptions.json", "storage2": ""}}
            }  # Default values
    