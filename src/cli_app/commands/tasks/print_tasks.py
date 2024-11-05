import json
import os
from base.base_command import BaseCommand

class PrintTasksCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self):
        tasks_file = '../../data/tasks.json'
        
        if not os.path.exists(tasks_file):
            print("No tasks file found.")
            return

        try:
            with open(tasks_file, 'r') as file:
                tasks = json.load(file)
        except json.JSONDecodeError:
            print("Error reading tasks file: Invalid JSON format.")
            return

        if not tasks:
            print("No tasks available.")
            return

        print("Tasks:")
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Priority ID: {task['priority_id']}, Duration Estimate: {task['duration_estimate']} minutes")

    @property
    def description(self):
        return "Print all tasks from the tasks file."
