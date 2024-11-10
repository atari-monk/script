from base.base_command import BaseCommand
from .lib.model.task import Task
from .lib.crud.task_crud import TaskCRUD
from ...libs.json_crud.project_crud import ProjectCRUD
from pydantic import ValidationError
from datetime import datetime

class AddTaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.task_crud = TaskCRUD()
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        # Check for minimum required arguments
        if len(args) < 3:
            print("Usage: add_task <project_id> <task_description> <status> [due_date]")
            return

        project_id = int(args[0])
        task_description = args[1]
        status = args[2]
        due_date = args[3] if len(args) > 3 else None

        # Check if project exists
        project = self.project_crud.read(project_id)
        if not project:
            print(f"Project with ID {project_id} does not exist.")
            return

        # Prepare the task data
        task_data = {
            "project_id": project_id,
            "description": task_description,
            "status": status,
        }

        # Parse and add the due date if provided
        if due_date:
            try:
                task_data["due_date"] = datetime.fromisoformat(due_date)
            except ValueError:
                print("Invalid due date format. Use YYYY-MM-DD.")
                return

        # Validate and create the task
        try:
            validated_task = Task(**task_data)
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())  # Detailed error info in JSON format
            return

        # Attempt to add the task to storage
        try:
            result = self.task_crud.create(**validated_task.model_dump())
            if result:
                print(f"Task '{result['description']}' created successfully with ID: {result['id']}")
            else:
                print("Failed to create task.")
        except Exception as e:
            print(f"Unexpected error during task creation: {e}")

    @property
    def description(self):
        return "Add a new task to a specific project."
