# commands/select_task.py

import json
import os
from base.base_command import BaseCommand

class SelectTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, task_index):
        try:
            # Convert task_index to an integer
            task_index = int(task_index)

            tasks_file = '../../data/tasks.json'

            # Load existing tasks
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r') as file:
                    tasks = json.load(file)
            else:
                print("No tasks found.")
                return

            # Check if the index is valid
            if 0 <= task_index < len(tasks):
                selected_task = tasks[task_index]
                self.app.context.current_task = selected_task
                print(f"Task selected: {selected_task}")
            else:
                print(f"Invalid task index. Please select a number between 0 and {len(tasks) - 1}.")

        except ValueError:
            print("Invalid input for task index. Please provide a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @property
    def description(self):
        return "Select a task by index and store it in the application context."
