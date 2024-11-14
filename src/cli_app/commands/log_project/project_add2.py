import logging
#import pdb
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD2, ProjectCRUD3
from commands.log_project.lib.model.project2 import Project2

logger = logging.getLogger(__name__)

class ProjectAdd2Command(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_json_reposotory = ProjectCRUD2()
        self.project_jsonl_reposotory = ProjectCRUD3()

    def execute(self, *args):
        #pdb.set_trace()
        if len(args) < 2:
            self.print_usage()
            return
        
        name = args[0]
        description = args[1]
        repo_link =  args[2] if len(args) > 2 else None
        status = args[3] if len(args) > 3 else None
        data_valid = Project2.parse_data(0, name, description, repo_link, status)

        try:
            project_new = Project2.from_dict(data_valid)
        except ValueError as e:
            logger.error(f"Error: Invalid input data. {e}")
            return

        try:
            result = self.project_json_reposotory.add_item(project_new)
            result_jsonl = self.project_jsonl_reposotory.add_item(project_new)
            if result and result_jsonl:
                logger.info(f"Project '{result['name']}' created successfully with ID '{result['id']}' in both repositories (JSON and JSONL).")
            else:
                if not result:
                    logger.warning("Failed to create project in JSON repository.")
                if not result_jsonl:
                    logger.warning("Failed to create project in JSONL repository.")
        except Exception as e:
            logger.error(f"Unexpected error during project creation: {e}")

    def print_usage(self):
        usage_message = """
Usage: command <name> <description> [optional: <repo_link> <status>]

Examples:
- To add a new project: 
  command "New Project" "Project description" "https://repo.com" "Not Started"
"""
        logger.info(usage_message)

    @property
    def description(self):
        return "Add a new project."
