# commands/exit.py

from base.base_command import BaseCommand

class ExitCommand(BaseCommand):
    def __init__(self, app):
        # Store reference to the app to modify its running state
        self.app = app

    def execute(self, *args):
        print("Exiting CLI App.")
        self.app.running = False

    @property
    def description(self):
        return "Exit the application."
