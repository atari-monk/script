import os
from base.base_command import BaseCommand
from .lib.config import DB_DIR
from ...libs.crud.project_crud import ProjectCRUD  # Assuming ProjectCRUD is imported from its module
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DeleteProjectCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        """Executes the delete command using the project ID provided in *args."""
        if len(args) < 1:
            logger.error("Project ID is required to delete a project.")
            return "Error: Project ID is required."

        # Extract the project ID from *args
        project_id = args[0]

        # Ensure the project ID is an integer
        try:
            project_id = int(project_id)
        except ValueError:
            logger.error("Invalid Project ID format. Project ID must be an integer.")
            return "Error: Project ID must be an integer."

        # Perform the delete operation
        self.project_crud.delete(project_id)

    @property
    def description(self):
        return "Delete Project."
