# commands/add_task.py

import json
import os
from base.base_command import BaseCommand

class AddTaskCommand(BaseCommand):
    def execute(self, description, priority, duration):
        try:
            task = {
                "description": description,
                "priority": priority,
                "duration": float(duration)
            }

            tasks_file = '../../data/tasks.json'

            # Load existing tasks
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r') as file:
                    tasks = json.load(file)
            else:
                tasks = []

            # Append the new task
            tasks.append(task)

            # Save tasks back to the JSON file
            with open(tasks_file, 'w') as file:
                json.dump(tasks, file, indent=2)

            print(f"Task added: {task}")

        except ValueError:
            print("Invalid input for duration. Please provide a valid number.")

    @property
    def description(self):
        return "Add a new task with a description, priority, and duration."
