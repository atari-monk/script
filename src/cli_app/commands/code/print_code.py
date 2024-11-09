from base.base_command import BaseCommand
from .lib.print_code import main

class PrintCodeCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Print Code."
    