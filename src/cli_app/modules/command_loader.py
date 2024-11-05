import os
import importlib
from base.base_command import BaseCommand
from base.base_module import BaseModule

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them,
        including commands from subdirectories.
        """
        command_folder = 'commands'
        
        for dirpath, _, filenames in os.walk(command_folder):
            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":
                    # Create module name by replacing slashes with dots
                    module_name = f"{dirpath.replace(os.sep, '.')}.{filename[:-3]}"
                    module = importlib.import_module(module_name)

                    # Find command class in module
                    for attr in dir(module):
                        command_class = getattr(module, attr)
                        if isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand:
                            command_instance = command_class(self.app)  # Pass the app instance
                            command_name = filename[:-3]  # Command name without .py extension
                            self.app.commands[command_name] = command_instance.execute
