import logging
from typing import List
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD2

logger = logging.getLogger(__name__)

class ProjectDelete2Command(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD2()

    def execute(self, *args: List[str]) -> None:
        if len(args) < 1:
            self.print_usage()
            return

        project_id = int(args[0])

        logger.debug(f"Attempting to delete project with ID: {project_id}")

        try:
            existing_project = self.project_crud.get_by_id(project_id)
            if not existing_project:
                logger.error(f"Project with ID '{project_id}' not found.")
                return

            result = self.project_crud.delete_by_id(project_id)
            if result:
                logger.info(f"Project '{project_id}' deleted successfully.")
            else:
                logger.warning(f"Failed to delete project '{project_id}'.")
        except ValueError:
            logger.error("Invalid project ID. Please provide a numeric ID.")
        except Exception as e:
            logger.error(f"Unexpected error during project deletion: {e}")

    def print_usage(self):
        usage_message = """
Usage: command <project_id>

Example:
- To delete a project:
  command 123
"""
        logger.info(usage_message)

    @property
    def description(self):
        return "Delete a project by its ID."
