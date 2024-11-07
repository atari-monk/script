from base.base_command import BaseCommand
from .lib.watch_time import main

class WatchTimeCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Watch Time."