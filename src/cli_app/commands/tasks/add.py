import json
import os
from pydantic import BaseModel, Field, ValidationError
from base.base_command import BaseCommand

class Task(BaseModel):
    name: str
    description: str
    priority_id: int
    duration_estimate: int

    # You can add constraints for fields if needed, such as min and max values for duration_estimate

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
            # Parse and validate the input parameters using Pydantic
            task_data = Task(
                name=name,
                description=description,
                priority_id=int(priority_id),
                duration_estimate=int(duration_estimate)
            )

            # Load existing tasks to establish a new id
            tasks_file = '../../data/tasks.json'
            tasks = self.load_tasks(tasks_file)

            # Generate a unique id based on the number of existing tasks
            task_id = len(tasks) + 1

            # Load priorities and validate priority_id
            priorities = self.load_priorities()
            if not any(priority['id'] == task_data.priority_id for priority in priorities):
                valid_ids = [priority['id'] for priority in priorities]
                print(f"Invalid priority ID: {task_data.priority_id}. Valid priority IDs are: {valid_ids}.")
                return

            task = {
                "id": task_id,
                "name": task_data.name,
                "description": task_data.description,
                "priority_id": task_data.priority_id,
                "duration_estimate": task_data.duration_estimate
            }

            # Append the new task
            tasks.append(task)

            # Save tasks back to the JSON file
            with open(tasks_file, 'w') as file:
                json.dump(tasks, file, indent=2)

            print(f"Task added: {task}")

        except ValidationError as e:
            print(f"Error: Invalid input data. {e}")

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
