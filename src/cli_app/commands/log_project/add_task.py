from datetime import datetime
from pydantic import ValidationError
from base.base_command import BaseCommand
from commands.log_project.lib.crud.task_crud import TaskCRUD
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.task import Task

class TaskCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.task_crud = TaskCRUD()
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 2:
            print("Usage: task <action> <task_id (optional)> <project_id> <task_description> <status> [due_date]")
            return

        action = args[0].lower()

        if action == "add":
            self.add_task(args[1:])
        elif action == "edit":
            self.edit_task(args[1:])
        elif action == "delete":
            self.delete_task(args[1:])
        else:
            print("Error: Invalid action. Use 'add' to create, 'edit' to update, or 'delete' to remove a task.")

    def add_task(self, args):
        if len(args) < 3:
            print("Usage: task add <project_id> <task_description> <status> [due_date]")
            return

        project_id, task_description, status = args[0], args[1], args[2]
        due_date = args[3] if len(args) > 3 else None

        # Check if project exists
        project = self.project_crud.read(project_id)
        if not project:
            print(f"Project with ID {project_id} does not exist.")
            return

        # Prepare task data
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
            print(e.json())
            return

        # Attempt to add the task
        try:
            result = self.task_crud.create(**validated_task.model_dump())
            if result:
                print(f"Task '{result['description']}' created successfully with ID: {result['id']}")
            else:
                print("Failed to create task.")
        except Exception as e:
            print(f"Unexpected error during task creation: {e}")

    def edit_task(self, args):
        if len(args) < 4:
            print("Usage: task edit <task_id> <project_id> <task_description> <status> [due_date]")
            return

        task_id, project_id, task_description, status = args[0], args[1], args[2], args[3]
        due_date = args[4] if len(args) > 4 else None

        # Check if project exists
        project = self.project_crud.read(project_id)
        if not project:
            print(f"Project with ID {project_id} does not exist.")
            return

        # Fetch the existing task to validate ID
        existing_task = self.task_crud.read(task_id)
        if not existing_task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        # Update only the fields that are provided
        if task_description != "none":
            existing_task['description'] = task_description
        if status != "none":
            existing_task['status'] = status
        if due_date:
            try:
                existing_task['due_date'] = datetime.fromisoformat(due_date)
            except ValueError:
                print("Invalid due date format. Use YYYY-MM-DD.")
                return

        # Validate and update the task
        try:
            validated_task = Task(**existing_task)
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        # Attempt to update the task
        try:
            result = self.task_crud.update(task_id, **validated_task.model_dump())
            if result:
                print(f"Task '{task_id}' updated successfully.")
            else:
                print("Failed to update task.")
        except Exception as e:
            print(f"Unexpected error during task update: {e}")

    def delete_task(self, args):
        if len(args) < 1:
            print("Usage: task delete <task_id>")
            return

        task_id = args[0]

        # Fetch the task to ensure it exists
        existing_task = self.task_crud.read(task_id)
        if not existing_task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        # Attempt to delete the task
        try:
            result = self.task_crud.delete(task_id)
            if result:
                print(f"Task '{task_id}' deleted successfully.")
            else:
                print(f"Failed to delete task '{task_id}'.")
        except Exception as e:
            print(f"Unexpected error during task deletion: {e}")

    @property
    def description(self):
        return "Add, edit, or delete a task. Use 'add' to create, 'edit' to update, or 'delete' to remove a task."
