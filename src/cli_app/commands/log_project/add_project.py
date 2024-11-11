from pydantic import ValidationError
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.project import Project

class ProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 2:
            self.print_usage()
            return

        action = args[0].lower()
        if action == "add":
            self.add_project(args[1:])
        elif action == "edit":
            self.edit_project(args[1:])
        elif action == "delete":
            self.delete_project(args[1:])
        else:
            print("Error: Invalid action. Use 'add' to create, 'edit' to update, or 'delete' to remove a project.")
            self.print_usage()

    def add_project(self, args):
        if len(args) < 2:
            print("Usage: project add <name> <description> [optional: <repo_link> <status> <start_date> <end_date> <priority> <technologies> <milestones> <current_tasks>]")
            return

        name, description = args[0], args[1]

        try:
            validated_project = Project(
                name=name,
                description=description
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        try:
            result = self.project_crud.create(
                name=validated_project.name,
                description=validated_project.description,
                repo_link=validated_project.repo_link,
                status=validated_project.status,
                start_date=validated_project.start_date,
                end_date=validated_project.end_date,
                priority=validated_project.priority,
                technologies=validated_project.technologies,
                milestones=validated_project.milestones,
                current_tasks=validated_project.current_tasks,
                last_updated=validated_project.last_updated
            )
            if result:
                print(f"Project '{result['name']}' created successfully with ID '{result['id']}'.")
            else:
                print("Failed to create project.")
        except Exception as e:
            print(f"Unexpected error during project creation: {e}")

    def edit_project(self, args):
        if len(args) < 3:
            print("Usage: project edit <project_id> <name or 'none'> <description or 'none'> [optional: <repo_link> <status> <start_date> <end_date> <priority> <technologies> <milestones> <current_tasks>]")
            return

        project_id, name, description = args[0], args[1], args[2]

        # Fetch the current project to validate the ID and make sure it exists
        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        # Update only the fields that are provided (not 'none')
        if name != "none":
            existing_project['name'] = name
        if description != "none":
            existing_project['description'] = description

        try:
            validated_project = Project(
                name=existing_project['name'],
                description=existing_project['description'],
                repo_link=existing_project['repo_link'],
                status=existing_project['status'],
                start_date=existing_project['start_date'],
                end_date=existing_project['end_date'],
                priority=existing_project['priority'],
                technologies=existing_project['technologies'],
                milestones=existing_project['milestones'],
                current_tasks=existing_project['current_tasks'],
                last_updated=existing_project['last_updated']
            )
        except ValidationError as e:
            print("Error: Invalid input data.")
            print(e.json())
            return

        try:
            result = self.project_crud.update(
                project_id,
                **validated_project.model_dump()
            )
            if result:
                print(f"Project '{project_id}' updated successfully.")
            else:
                print("Failed to update project.")
        except Exception as e:
            print(f"Unexpected error during project update: {e}")

    def delete_project(self, args):
        if len(args) < 1:
            print("Usage: project delete <project_id>")
            return

        project_id = args[0]

        # Fetch the project to ensure it exists
        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        try:
            # Perform the deletion
            result = self.project_crud.delete(project_id)
            if result:
                print(f"Project '{project_id}' deleted successfully.")
            else:
                print(f"Failed to delete project '{project_id}'.")
        except Exception as e:
            print(f"Unexpected error during project deletion: {e}")

    def print_usage(self):
        print("""
Usage: project <action> <project_id (optional)> <name> <description>
Actions:
- add: Create a new project. You must specify a name and description. Optional additional fields: <repo_link>, <status>, <start_date>, <end_date>, <priority>, <technologies>, <milestones>, <current_tasks>.
- edit: Update an existing project by specifying the project ID, and the fields you want to modify. Use 'none' for fields you don't want to update.
- delete: Remove a project by specifying its project ID.

Examples:
- To add a new project: 
  project add "New Project" "This is a description" "https://repo.com" "Active" "2024-01-01" "2024-12-31" "High" "Tech1, Tech2" "Milestone1, Milestone2" "Task1, Task2"

- To edit an existing project:
  project edit 123 "Updated Project Name" "Updated Description"

- To delete a project:
  project delete 123
""")
    
    @property
    def description(self):
        return "Add, edit, or delete a project. Use 'add' to create, 'edit' to update, or 'delete' to remove a project."
