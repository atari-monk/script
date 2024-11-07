from base.base_command import BaseCommand
from .lib.selection import main

class ProjectTimeInputCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Project time input."
    