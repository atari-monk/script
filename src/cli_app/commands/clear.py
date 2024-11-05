import os
from base.base_command import BaseCommand

class ClearCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        """Clear the console screen."""
        # Check the OS and clear the screen accordingly
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For Unix-based systems (Linux/macOS)
            os.system('clear')

    @property
    def description(self):
        return "Clear the console screen."
