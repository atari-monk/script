# commands/print_tasks.py

import json
import os
from base.base_command import BaseCommand

class PrintTasksCommand(BaseCommand):
    def execute(self):
        tasks_file = '../../data/tasks.json'
        
        if not os.path.exists(tasks_file):
            print("No tasks file found.")
            return

        with open(tasks_file, 'r') as file:
            tasks = json.load(file)

        if not tasks:
            print("No tasks available.")
            return

        print("Tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. Description: {task['description']}, Priority: {task['priority']}, Duration: {task['duration']}")

    @property
    def description(self):
        return "Print all tasks from the tasks file."
