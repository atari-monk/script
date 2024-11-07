from base.base_command import BaseCommand
from .lib.wellness_tracker import main

class WellnessTrackerCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        main()

    @property
    def description(self):
        return "Wellness Tracker."
    