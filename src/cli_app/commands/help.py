from base.base_command import BaseCommand

class HelpCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ignore_list = {'template.py'}

    def execute(self, *args):
        print("Available commands:")
        for cmd, func in self.app.commands.items():
            if f"{cmd}" in self.ignore_list:
                continue
             
            if hasattr(func, '__self__') and isinstance(func.__self__, BaseCommand):
                description = func.__self__.description
            else:
                description = "No description available"
            print(f"  {cmd}: {description}")

    @property
    def description(self):
        return "Display available commands."
