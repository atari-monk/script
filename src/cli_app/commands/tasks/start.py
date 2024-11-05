import json
import os
from datetime import datetime
from base.base_command import BaseCommand

class StartTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.task_log_file = '../../data/task_log.json'

    def execute(self):
        # Check if a task is currently selected
        if not hasattr(self.app.context, 'current_task'):
            print("No task is currently selected. Please select a task before starting it.")
            return

        selected_task = self.app.context.current_task

        # Create the log entry
        log_entry = {
            "task_id": selected_task['id'],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "log": None
        }

        # Load existing logs or initialize an empty list
        task_logs = self.load_task_logs()

        # Append the new log entry
        task_logs.append(log_entry)

        # Save the updated logs back to the JSON file
        with open(self.task_log_file, 'w') as file:
            json.dump(task_logs, file, indent=2)

        print(f"Started task: {selected_task['name']} (ID: {selected_task['id']})")

    @property
    def description(self):
        return "Start the currently selected task and log the start time."

    def load_task_logs(self):
        """Load existing task logs from the JSON file or return an empty list if the file is empty or invalid."""
        if os.path.exists(self.task_log_file):
            try:
                with open(self.task_log_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Warning: task_log.json is empty or contains invalid JSON. Starting with an empty log list.")
                return []
        return []
