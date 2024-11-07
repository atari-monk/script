from base.base_command import BaseCommand
from .lib.time import main

class ProjectTimeCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Project time logger."
    