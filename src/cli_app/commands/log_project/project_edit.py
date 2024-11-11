from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.project import Project

class ProjectEditCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 2:
            self.print_usage()
            return

        project_id = args[0]
        field_value_pairs = args[1:]
        update_data = {}

        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        for field_value in field_value_pairs:
            try:
                field, value = field_value.split('=')
                field = field.strip().lower()
                value = value.strip()

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
                    continue

            except ValueError as e:
                print(f"Error: Invalid format for '{field_value}', {e}")
                return

        try:
            updated_project = self.project_crud.update(project_id, **update_data)
            if updated_project:
                print(f"Project '{project_id}' updated successfully.")
            else:
                print(f"Failed to update project '{project_id}'.")
        except Exception as e:
            print(f"Unexpected error during project update: {e}")

    def print_usage(self):
        print("""
Usage: command <project_id> <field1=value1> <field2=value2> ...
Example:
- To edit an existing project:
  command 123 name="Updated Project" description="Updated Description" status="In Progress"
""")
    
    @property
    def description(self):
        return "Edit an existing project. Specify the project ID and fields to update."
