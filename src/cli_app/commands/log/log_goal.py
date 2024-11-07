from base.base_command import BaseCommand
from .lib.log_goal import main

class LogGoalCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Log goal."