from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.project import Project

class ProjectEditCommand(BaseCommand):
    VALID_STATUSES = {"Not Started", "In Progress", "Completed", "On Hold"}
    VALID_PRIORITIES = {"Low", "Medium", "High"}

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 2:
            self.print_usage()
            return

        project_id, *field_value_pairs = args
        update_data = {}

        if not (existing_project := self.project_crud.read(project_id)):
            print(f"Error: Project with ID '{project_id}' not found.")
            return

        for field_value in field_value_pairs:
            if "=" not in field_value:
                print(f"Error: Invalid format for '{field_value}', expected 'field=value'.")
                return

            field, value = map(str.strip, field_value.split("=", 1))
            field = field.lower()

            if not self._validate_and_add_field(field, value, update_data):
                return

        try:
            updated_project = self.project_crud.update(project_id, **update_data)
            message = f"Project '{project_id}' updated successfully." if updated_project else f"Failed to update project '{project_id}'."
            print(message)
        except Exception as e:
            print(f"Unexpected error during project update: {e}")

    def _validate_and_add_field(self, field, value, update_data):
        if field == "name" and not Project._contains_only_valid_characters(value):
            print("Error: Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
            return False
        elif field == "description" and len(value.split()) < 5:
            print("Error: Description should contain at least 5 words.")
            return False
        elif field == "status" and value not in self.VALID_STATUSES:
            print(f"Error: Invalid status value. Must be one of: {', '.join(self.VALID_STATUSES)}.")
            return False
        elif field == "priority" and value not in self.VALID_PRIORITIES:
            print(f"Error: Invalid priority value. Must be one of: {', '.join(self.VALID_PRIORITIES)}.")
            return False

        if field in {"technologies", "milestones", "current_tasks"}:
            update_data[field] = value.split(",")
        else:
            update_data[field] = value
        return True

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
