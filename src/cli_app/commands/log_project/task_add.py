from base.base_command import BaseCommand
from commands.log_project.lib.crud.task_crud import TaskCRUD
from commands.log_project.lib.model.task import Task
from datetime import datetime

class TaskAddCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.task_crud = TaskCRUD()

    def execute(self, *args):
        if len(args) < 2:
            self.print_usage()
            return
        
        # Required fields
        project_id, title = args[0], args[1]
        
        # Optional fields
        status = args[2] if len(args) > 2 else 'pending'
        description = args[3] if len(args) > 3 else None
        priority = args[4] if len(args) > 4 else 'medium'
        due_date_str = args[5] if len(args) > 5 else None

        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return

        # Create and validate task model using required fields and optional fields
        try:
            validated_task = Task(
                project_id=int(project_id),
                title=title,
                status=status,
                description=description,
                priority=priority,
                due_date=due_date,
                created_at=datetime.now()  # Automatically set created_at
            )
        except ValueError as e:
            print(f"Error: Invalid input data. {e}")
            return

        # Attempt to save the task
        try:
            result = self.task_crud.add_item(validated_task)
            if result:
                print(f"Task '{result['description']}' created successfully with ID '{result['id']}'.")
            else:
                print("Failed to create task.")
        except Exception as e:
            print(f"Unexpected error during task creation: {e}")

    def print_usage(self):
        print("""
Usage: command <project_id> <title> [optional: <status>] [optional: <description>] [optional: <priority>] [optional: <due_date>]

Examples:
- To add a new task:
  command 123 "Task title" "Pending" "Task description" "High" "2024-12-31"
- To add a new task with minimal fields:
  command 123 "Task title" "In Progress"
""")

    @property
    def description(self):
        return "Add a new task."
