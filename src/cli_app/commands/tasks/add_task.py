import json
import os
from base.base_command import BaseCommand

class AddTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, name, description, priority, duration_estimate):
        try:
            # Debugging output to check input values
            print(f"Received input: name={name}, description={description}, priority={priority}, duration_estimate={duration_estimate}")

            # Attempt to convert duration_estimate to float
            duration_estimate_float = float(duration_estimate)

            # Load existing tasks to establish a new id
            tasks_file = '../../data/tasks.json'
            tasks = self.load_tasks(tasks_file)

            # Generate a unique id based on the number of existing tasks
            task_id = len(tasks) + 1

            task = {
                "id": task_id,
                "name": name,
                "description": description,
                "priority": priority,
                "duration_estimate": duration_estimate_float
            }

            # Append the new task
            tasks.append(task)

            # Save tasks back to the JSON file
            with open(tasks_file, 'w') as file:
                json.dump(tasks, file, indent=2)

            print(f"Task added: {task}")

        except ValueError as e:
            print(f"Invalid input for duration: {duration_estimate}. Error: {e}. Please provide a valid number.")


    @property
    def description(self):
        return "Add a new task with a name, description, priority, and duration estimate."

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
