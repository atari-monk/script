import logging
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD2
from commands.log_project.lib.model.project2 import Project2

logger = logging.getLogger(__name__)

class ProjectAdd2Command(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD2()

    def execute(self, *args):
        if len(args) < 1:
            self.print_usage()
            return
        
        name = args[0]
        data = Project2.parse_data(0, name)

        try:
            validated_project = Project2.from_dict(data)
        except ValueError as e:
            logger.error(f"Error: Invalid input data. {e}")
            return

        try:
            result = self.project_crud.create(validated_project)
            if result:
                logger.info(f"Project '{result['name']}' created successfully with ID '{result['id']}'.")
            else:
                logger.warning("Failed to create project.")
        except Exception as e:
            logger.error(f"Unexpected error during project creation: {e}")

    def print_usage(self):
        usage_message = """
Usage: command <name>

Examples:
- To add a new project: 
  command "New Project"
"""
        logger.info(usage_message)

    @property
    def description(self):
        return "Add a new project."
