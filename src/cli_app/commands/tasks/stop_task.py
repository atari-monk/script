import json
import os
from datetime import datetime
from base.base_command import BaseCommand

class StopTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.task_log_file = '../../data/task_log.json'

    def execute(self, add_log=True):
        # Check if a task is currently selected
        if not hasattr(self.app.context, 'current_task'):
            print("No task is currently selected. Please select a task before stopping it.")
            return

        selected_task = self.app.context.current_task

        # Load existing logs to find the latest entry for this task
        task_logs = self.load_task_logs()
        current_log_entry = next(
            (log for log in task_logs if log['task_id'] == selected_task['id'] and log['end_time'] is None), 
            None
        )

        if current_log_entry:
            # Update the log entry with the end time
            current_log_entry['end_time'] = datetime.now().isoformat()
            print(f"Stopped task: {selected_task['name']} (ID: {selected_task['id']})")
            
            if add_log:
                log_details = input("Enter log details (optional): ")
                current_log_entry['log'] = log_details

            # Debug information
            print(f"Log Entry Updated: {current_log_entry}")
        else:
            print(f"No running task found for task ID: {selected_task['id']}.")

        # Save the updated logs back to the JSON file
        with open(self.task_log_file, 'w') as file:
            json.dump(task_logs, file, indent=2)
            print("Task logs saved successfully.")

    @property
    def description(self):
        return "Stop the currently selected task and optionally log the end time and details."

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
