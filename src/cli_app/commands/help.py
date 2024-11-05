from base.base_command import BaseCommand

class HelpCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ignore_list = {}

    def execute(self, *args):
        """Display the available commands and their descriptions."""
        print("Available commands:")
        for cmd, func in self.app.context.commands.items():  # Accessing commands directly from app
            if cmd in self.ignore_list:
                continue
            
            # Check if the command has a description
            description = getattr(func.__self__, 'description', "No description available")
            print(f"  {cmd}: {description}")

    @property
    def description(self):
        return "Display available commands."
