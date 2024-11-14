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
        #self.project_jsonl_reposotory = ProjectCRUD3()

    def execute(self, *args):
        #pdb.set_trace()
        if len(args) < 2:
            self.print_usage()
            return
        
        name = args[0]
        description = args[1]
        repo_link =  args[2] if len(args) > 2 else None
        status = args[3] if len(args) > 3 else None
        start_date = args[4] if len(args) > 4 else None
        end_date = args[5] if len(args) > 5 else None
        
        project_dict = {
            'id': 0,
            'name': name,
            'description': description,
            'repo_link': repo_link,
            'status': status,
            'start_date': start_date,
            'end_date': end_date
        }

        try:
            result = self.project_json_reposotory.add_item(project_dict)
            result_jsonl = True #self.project_jsonl_reposotory.add_item(project_dict)
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
Usage: command <name> <description> [optional: <repo_link> <status> <start_date> <end_date>]

Examples:
- To add a new project: 
  command "New Project" "Project description" "https://repo.com" "Not Started" "2024-11-14" "2024-11-16"
"""
        logger.info(usage_message)

    @property
    def description(self):
        return "Add a new project."
