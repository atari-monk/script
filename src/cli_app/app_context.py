# app_context.py

class AppContext:
    def __init__(self):
        self.current_task = None
        self.commands = {}

    def register_command(self, name, command):
        """Register a command in the context."""
        self.commands[name] = command

    def get_command(self, name):
        """Retrieve a command by name."""
        return self.commands.get(name)

    def execute_command(self, name, *args, **kwargs):
        """Execute a registered command."""
        command = self.get_command(name)
        if command:
            return command(*args, **kwargs)
        else:
            raise ValueError(f"Command '{name}' not found.")
