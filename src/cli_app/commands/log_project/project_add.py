import logging
from base.base_command import BaseCommand
from commands.log_project.lib.crud.project_crud import ProjectCRUD
from commands.log_project.lib.model.project import Project

logger = logging.getLogger(__name__)

class ProjectAddCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.project_crud = ProjectCRUD()

    def execute(self, *args):
        if len(args) < 2:
            self.print_usage()
            return
        
        name, description = args[0], args[1]
        repo_link = args[2] if len(args) > 2 else None
        status = args[3] if len(args) > 3 else None
        start_date = args[4] if len(args) > 4 else None
        end_date = args[5] if len(args) > 5 else None
        priority = args[6] if len(args) > 6 else None
        technologies = args[7].split(",") if len(args) > 7 else []
        milestones = args[8].split(",") if len(args) > 8 else []
        current_tasks = args[9].split(",") if len(args) > 9 else []

        logger.debug(f"Arguments received: {args}")
        logger.debug(f"Project name: {name}")
        logger.debug(f"Project description: {description}")

        try:
            validated_project = Project(name=name, description=description, repo_link=repo_link,
            status=status,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            technologies=technologies,
            milestones=milestones,
            current_tasks=current_tasks)
        except ValueError as e:
            print(f"Error: Invalid input data. {e}")
            return

        try:
            result = self.project_crud.create(validated_project)
            if result:
                print(f"Project '{result['name']}' created successfully with ID '{result['id']}'.")
            else:
                print("Failed to create project.")
        except Exception as e:
            print(f"Unexpected error during project creation: {e}")

    def print_usage(self):
        print("""
Usage: command <name> <description> [optional: <repo_link> <status> <start_date> <end_date> <priority> <technologies> <milestones> <current_tasks>]

Examples:
- To add a new project: 
  command "New Project" "This is a description" "https://repo.com" "Active" "2024-01-01" "2024-12-31" "High" "Tech1, Tech2" "Milestone1, Milestone2" "Task1, Task2"
""")
    
    @property
    def description(self):
        return "Add a new project."
