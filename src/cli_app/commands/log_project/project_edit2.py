import logging
from typing import List
from base.base_command import BaseCommand
from shared.input_validator import InputValidator
from commands.log_project.lib.crud.project_crud import ProjectCRUD2
from commands.log_project.lib.model.project2 import Project2

logger = logging.getLogger(__name__)

class ProjectEdit2Command(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD2()

    def execute(self, *args: List[str]) -> None:
        if len(args) < 2:
            self.print_usage()
            return

        project_id = int(args[0])
        field_value_pairs = args[1:]

        existing_project = self.project_crud.get_by_id(project_id)
        if not existing_project:
            logger.error(f"Project with ID '{project_id}' not found.")
            return

        validated_data = InputValidator.validate_and_parse(field_value_pairs)
        if not validated_data: return

        try:
            updated_project = self.project_crud.update_by_id(project_id, **validated_data)
            if updated_project:
                logger.info(f"Project '{project_id}' updated successfully.")
            else:
                logger.warning(f"Failed to update project '{project_id}'.")
        except Exception as e:
            logger.error(f"Unexpected error during project update: {e}")

    def print_usage(self):
        logger.info("Usage: command <project_id> <field=value> ...")

    @property
    def description(self):
        return "Edit an existing project. Specify the project ID and fields to update."
