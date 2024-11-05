import os
import importlib
from base.base_command import BaseCommand
from base.base_module import BaseModule
#from commands.exit import ExitCommand
#from commands.help import HelpCommand

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them.
        """
        command_folder = 'commands'
        for filename in os.listdir(command_folder):
            if filename.endswith(".py") and filename not in ["__init__.py"]:
                module_name = f"{command_folder}.{filename[:-3]}"
                module = importlib.import_module(module_name)

                # Find command class in module
                for attr in dir(module):
                    command_class = getattr(module, attr)
                    if isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand:
                        command_instance = command_class(self.app)  # Pass the app instance
                        command_name = filename[:-3]
                        self.app.commands[command_name] = command_instance.execute
