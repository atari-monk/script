class AppContext:
    def __init__(self):
        self.current_task = None
        self.commands = {}
        self.last_menu = []  # To store the last printed menu items

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

    def set_last_menu(self, menu):
        """Store the last printed menu items."""
        self.last_menu = menu

    def get_last_menu(self):
        """Retrieve the last printed menu items."""
        return self.last_menu
