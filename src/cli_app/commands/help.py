# commands/help.py

from base.base_command import BaseCommand

class HelpCommand(BaseCommand):
    def __init__(self, commands):
        # Store reference to the commands dictionary for help display
        self.commands = commands

    def execute(self, *args):
        print("Available commands:")
        for cmd, func in self.commands.items():
            if hasattr(func, '__self__') and isinstance(func.__self__, BaseCommand):
                description = func.__self__.description
            else:
                description = "No description available"
            print(f"  {cmd}: {description}")

    @property
    def description(self):
        return "Display available commands."
