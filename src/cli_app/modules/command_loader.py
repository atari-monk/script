import os
import importlib
from base.base_command import BaseCommand
from base.base_module import BaseModule

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them,
        including commands from subdirectories. Command names will include folder structure
        to avoid naming conflicts.
        """
        command_folder = 'commands'
        
        for dirpath, _, filenames in os.walk(command_folder):
            for filename in filenames:
                # Skip the init and template files
                if filename.endswith(".py") and filename not in ["__init__.py", "template.py"]:
                    # Create module name by replacing slashes with dots
                    module_name = f"{dirpath.replace(os.sep, '.')}.{filename[:-3]}"
                    module = importlib.import_module(module_name)

                    # Find and register command classes in the module
                    for attr in dir(module):
                        command_class = getattr(module, attr)
                        if isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand:
                            command_instance = command_class(self.app)  # Pass the app instance
                            
                            # Create a command name that includes the folder structure
                            relative_path = os.path.relpath(dirpath, command_folder)
                            if relative_path != '.':
                                command_name = f"{relative_path.replace(os.sep, '/')}/{filename[:-3]}"
                            else:
                                command_name = filename[:-3]  # Command name without .py extension
                            
                            # Register the command in the app's command registry
                            self.app.context.register_command(command_name, command_instance.execute)
