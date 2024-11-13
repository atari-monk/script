import logging
from typing import List
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD, ProjectCRUD3
from commands.log_project.lib.model.project import Project

logger = logging.getLogger(__name__)

class ProjectEditCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_json_reposotory = ProjectCRUD()
        self.project_jsonl_reposotory = ProjectCRUD3()

    def execute(self, *args: List[str]) -> None:
        if len(args) < 2:
            self.print_usage()
            return

        project_id = int(args[0])
        field_value_pairs = args[1:]
        update_data = {}

        logger.debug(f"Attempting to edit project with ID: {project_id}")

        existing_project = self.project_json_reposotory.get_by_id(project_id)
        if not existing_project:
            logger.error(f"Project with ID '{project_id}' not found.")
            return

        for field_value in field_value_pairs:
            if "=" not in field_value:
                logger.error(f"Invalid format for '{field_value}', expected 'field=value'.")
                return

            field, value = map(str.strip, field_value.split("=", 1))
            field = field.lower()

            try:
                parsed_value = Project.parse_fields(field, value)
                update_data[field] = parsed_value
            except ValueError as e:
                logger.error(f"Invalid value for '{field}': {e}")
                return

        try:
            result = self.project_json_reposotory.update_by_id(project_id, **update_data)
            result_jsonl = self.project_jsonl_reposotory.update_by_id(project_id, **update_data)
            if result and result_jsonl:
                logger.info(f"Project '{project_id}' updated successfully in both repositories (JSON and JSONL).")
            else:
                if not result:
                    logger.warning(f"Failed to update project '{project_id}' in JSON repository.")
                if not result_jsonl:
                    logger.warning(f"Failed to update project '{project_id}' in JSONL repository.")
        except Exception as e:
            logger.error(f"Unexpected error during project update: {e}")

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
