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
        except ValueError as e:
            print(f"Error: Invalid input data. {e}")
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
        if len(args) < 2:
            print("Usage: project edit <project_id> <field1=value1> <field2=value2> ...")
            return

        project_id = args[0]
        field_value_pairs = args[1:]

        # Fetch the current project to validate the ID and make sure it exists
        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        # Prepare the data to update
        update_data = {}

        for field_value in field_value_pairs:
            try:
                field, value = field_value.split('=')
                field = field.strip().lower()
                value = value.strip()

                # Validate and assign the fields
                if field == "name":
                    if not Project._contains_only_valid_characters(value):
                        raise ValueError("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
                    update_data["name"] = value
                elif field == "description":
                    if len(value.split()) < 5:
                        raise ValueError("Description should contain at least 5 words.")
                    update_data["description"] = value
                elif field == "repo_link":
                    update_data["repo_link"] = value
                elif field == "status":
                    if value not in ["Not Started", "In Progress", "Completed", "On Hold"]:
                        raise ValueError("Invalid status value. Must be one of: 'Not Started', 'In Progress', 'Completed', 'On Hold'.")
                    update_data["status"] = value
                elif field == "start_date":
                    update_data["start_date"] = value
                elif field == "end_date":
                    update_data["end_date"] = value
                elif field == "priority":
                    if value not in ["Low", "Medium", "High"]:
                        raise ValueError("Invalid priority value. Must be one of: 'Low', 'Medium', 'High'.")
                    update_data["priority"] = value
                elif field == "technologies":
                    update_data["technologies"] = value.split(',')
                elif field == "milestones":
                    update_data["milestones"] = value.split(',')
                elif field == "current_tasks":
                    update_data["current_tasks"] = value.split(',')
                else:
                    print(f"Warning: Unknown field '{field}', skipping.")
                    continue  # Skip unknown fields

            except ValueError as e:
                print(f"Error: Invalid format for '{field_value}', {e}")
                return

        # Update the project with the validated data
        try:
            # Assuming that ProjectCRUD is implemented to update fields correctly
            updated_project = self.project_crud.update(project_id, **update_data)
            if updated_project:
                print(f"Project '{project_id}' updated successfully.")
            else:
                print(f"Failed to update project '{project_id}'.")
        except Exception as e:
            print(f"Unexpected error during project update: {e}")

            if len(args) < 2:
                print("Usage: project edit <project_id> <field1=value1> <field2=value2> ...")
                return

            project_id = args[0]
            field_value_pairs = args[1:]

            # Fetch the current project to validate the ID and make sure it exists
            existing_project = self.project_crud.read(project_id)
            if not existing_project:
                print(f"Error: Project with ID '{project_id}' not found.")
                return

            # Prepare the data to update
            update_data = {}

            for field_value in field_value_pairs:
                try:
                    field, value = field_value.split('=')
                    field = field.strip().lower()
                    value = value.strip()

                    # Validate and assign the fields
                    if field == "name":
                        if not Project._contains_only_valid_characters(value):
                            raise ValueError("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
                        update_data["name"] = value
                    elif field == "description":
                        if len(value.split()) < 5:
                            raise ValueError("Description should contain at least 5 words.")
                        update_data["description"] = value
                    elif field == "repo_link":
                        update_data["repo_link"] = value
                    elif field == "status":
                        if value not in ["Not Started", "In Progress", "Completed", "On Hold"]:
                            raise ValueError("Invalid status value. Must be one of: 'Not Started', 'In Progress', 'Completed', 'On Hold'.")
                        update_data["status"] = value
                    elif field == "start_date":
                        update_data["start_date"] = value
                    elif field == "end_date":
                        update_data["end_date"] = value
                    elif field == "priority":
                        if value not in ["Low", "Medium", "High"]:
                            raise ValueError("Invalid priority value. Must be one of: 'Low', 'Medium', 'High'.")
                        update_data["priority"] = value
                    elif field == "technologies":
                        update_data["technologies"] = value.split(',')
                    elif field == "milestones":
                        update_data["milestones"] = value.split(',')
                    elif field == "current_tasks":
                        update_data["current_tasks"] = value.split(',')
                    else:
                        print(f"Warning: Unknown field '{field}', skipping.")
                        continue  # Skip unknown fields

                except ValueError as e:
                    print(f"Error: Invalid format for '{field_value}', {e}")
                    return

            # Update the project with the validated data
            try:
                updated_project = self.project_crud.update(project_id, **update_data)
                if updated_project:
                    print(f"Project '{project_id}' updated successfully.")
                else:
                    print(f"Failed to update project '{project_id}'.")
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
Usage: project <action> <project_id (optional)> <field1=value1> <field2=value2> ...
Actions:
- add: Create a new project. You must specify a name and description. Optional additional fields: <repo_link>, <status>, <start_date>, <end_date>, <priority>, <technologies>, <milestones>, <current_tasks>.
- edit: Update an existing project by specifying the project ID, and the fields you want to modify in the format 'field=value'. At least one field must be provided.
- delete: Remove a project by specifying its project ID.

Examples:
- To add a new project: 
  project add "New Project" "This is a description" "https://repo.com" "Active" "2024-01-01" "2024-12-31" "High" "Tech1, Tech2" "Milestone1, Milestone2" "Task1, Task2"

- To edit an existing project:
  project edit 123 name="Updated Project" description="Updated Description" status="In Progress"

- To delete a project:
  project delete 123
""")
    
    @property
    def description(self):
        return "Add, edit, or delete a project. Use 'add' to create, 'edit' to update, or 'delete' to remove a project."
