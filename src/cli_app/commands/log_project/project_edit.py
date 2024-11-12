import logging
from typing import List
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.project import Project

logger = logging.getLogger(__name__)

class ProjectEditCommand(BaseCommand):
    VALID_STATUSES = {"Not Started", "In Progress", "Completed", "On Hold"}
    VALID_PRIORITIES = {"Low", "Medium", "High"}

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args: List[str]) -> None:
        if len(args) < 2:
            self.print_usage()
            return

        project_id = int(args[0])
        field_value_pairs = args[1:]
        update_data = {}

        logger.debug(f"Attempting to edit project with ID: {project_id}")

        existing_project = self.project_crud.read(project_id)
        if not existing_project:
            logger.error(f"Project with ID '{project_id}' not found.")
            return

        for field_value in field_value_pairs:
            if "=" not in field_value:
                logger.error(f"Invalid format for '{field_value}', expected 'field=value'.")
                return

            field, value = map(str.strip, field_value.split("=", 1))
            field = field.lower()

            if not self._validate_and_add_field(field, value, update_data):
                return

        try:
            updated_project = self.project_crud.update(project_id, **update_data)
            if updated_project:
                logger.info(f"Project '{project_id}' updated successfully.")
            else:
                logger.warning(f"Failed to update project '{project_id}'.")
        except Exception as e:
            logger.error(f"Unexpected error during project update: {e}")

    def _validate_and_add_field(self, field: str, value: str, update_data: dict) -> bool:
        if field == "name" and not Project._contains_only_valid_characters(value):
            logger.error("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
            return False
        elif field == "description" and len(value.split()) < 1:
            logger.error("Description should contain at least 1 word.")
            return False
        elif field == "status" and value not in self.VALID_STATUSES:
            logger.error(f"Invalid status value. Must be one of: {', '.join(self.VALID_STATUSES)}.")
            return False
        elif field == "priority" and value not in self.VALID_PRIORITIES:
            logger.error(f"Invalid priority value. Must be one of: {', '.join(self.VALID_PRIORITIES)}.")
            return False

        update_data[field] = value.split(",") if field in {"technologies", "milestones", "current_tasks"} else value
        return True

    def print_usage(self):
        usage_message = """
Usage: command <project_id> <field1=value1> <field2=value2> ...

Example:
- To edit an existing project:
  command 123 name="Updated Project" description="Updated Description" status="In Progress"
"""
        logger.info(usage_message)

    @property
    def description(self):
        return "Edit an existing project. Specify the project ID and fields to update."
