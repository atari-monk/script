from base.base_command import BaseCommand
from .lib.log_step import main

class LogStepCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Log step."