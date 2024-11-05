from base.base_command import BaseCommand

class PrintContextCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        """Print the current state of the app context."""
        print("Current App Context:")
        print(f"  Current Task: {self.app.context.current_task}")
        print("  Registered Commands:")
        for cmd in self.app.context.commands:
            print(f"    - {cmd}")
        print("  Last Menu Items:")
        print(f"    {self.app.context.get_last_menu() or 'No menu items available.'}")

    @property
    def description(self):
        return "Print the current state of the app context."
