import json
import os
from base.base_command import BaseCommand

class SelectTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, task_id):
        try:
            # Convert task_id to an integer
            task_id = int(task_id)

            tasks_file = '../../data/tasks.json'

            # Load existing tasks
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r') as file:
                    tasks = json.load(file)
            else:
                print("No tasks found.")
                return

            # Find the task by ID
            selected_task = next((task for task in tasks if task['id'] == task_id), None)

            if selected_task:
                self.app.context.current_task = selected_task
                print(f"Task selected: {selected_task}")
            else:
                print(f"Invalid task ID: {task_id}. Please provide a valid task ID.")

        except ValueError:
            print("Invalid input for task ID. Please provide a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @property
    def description(self):
        return "Select a task by ID and store it in the application context."
