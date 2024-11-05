import json
import os
from base.base_command import BaseCommand

class AddTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.priorities_file = '../../data/priorities.json'

    def execute(self, *args):
        if len(args) != 4:
            print("Error: Four arguments required - name, description, priority ID, and duration estimate.")
            return

        name, description, priority_id, duration_estimate = args

        try:
            # Convert priority_id to an integer for validation
            priority_id = int(priority_id)

            # Validate name format (only letters, numbers, and underscores)
            if not self.is_valid_name(name):
                print("Invalid name format. Name must be alphanumeric or contain underscores.")
                return

            # Validate description (should be a non-empty string)
            if not self.is_valid_description(description):
                print("Invalid description. Description cannot be empty and should be a string.")
                return

            # Validate duration (should be an integer)
            duration_estimate_int = self.validate_duration(duration_estimate)

            # Load existing tasks to establish a new id
            tasks_file = '../../data/tasks.json'
            tasks = self.load_tasks(tasks_file)

            # Generate a unique id based on the number of existing tasks
            task_id = len(tasks) + 1

            # Load priorities and validate priority_id
            priorities = self.load_priorities()
            if not any(priority['id'] == priority_id for priority in priorities):
                valid_ids = [priority['id'] for priority in priorities]
                print(f"Invalid priority ID: {priority_id}. Valid priority IDs are: {valid_ids}.")
                return

            task = {
                "id": task_id,
                "name": name,
                "description": description,
                "priority_id": priority_id,
                "duration_estimate": duration_estimate_int
            }

            # Append the new task
            tasks.append(task)

            # Save tasks back to the JSON file
            with open(tasks_file, 'w') as file:
                json.dump(tasks, file, indent=2)

            print(f"Task added: {task}")

        except ValueError as e:
            print(f"Error: {e}. Please ensure that duration is an integer.")

    @property
    def description(self):
        return "Add a new task with a valid name, description, priority ID, and duration estimate in minutes."

    def load_tasks(self, tasks_file):
        """Load existing tasks from the JSON file, or return an empty list if file is empty or invalid."""
        if os.path.exists(tasks_file):
            try:
                with open(tasks_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Warning: tasks.json is empty or contains invalid JSON. Starting with an empty task list.")
                return []
        return []

    def load_priorities(self):
        """Load priorities from the JSON file."""
        if os.path.exists(self.priorities_file):
            try:
                with open(self.priorities_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Warning: priorities.json is empty or contains invalid JSON. Returning an empty priority list.")
                return []
        return []

    def is_valid_name(self, name):
        """Check if the name is valid (alphanumeric and underscores)."""
        return isinstance(name, str) and bool(name) and all(c.isalnum() or c == '_' for c in name)

    def is_valid_description(self, description):
        """Check if the description is valid (non-empty string)."""
        return isinstance(description, str) and bool(description.strip())

    def validate_duration(self, duration_estimate):
        """Validate that duration_estimate is an integer."""
        try:
            duration_int = int(duration_estimate)
        except ValueError:
            raise ValueError("Duration estimate must be an integer.")
        
        if duration_int < 0:
            raise ValueError("Duration estimate cannot be negative.")
        return duration_int
