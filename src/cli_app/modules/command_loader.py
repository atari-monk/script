# main.py or a separate file for better organization

import os
import importlib
from base.base_command import BaseCommand
from base.base_module import BaseModule
from commands.exit import ExitCommand
from commands.help import HelpCommand

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them.
        """
        command_folder = 'commands'
        for filename in os.listdir(command_folder):
            if filename.endswith(".py") and filename not in ["base_command.py", "__init__.py", "help.py", "exit.py"]:
                module_name = f"{command_folder}.{filename[:-3]}"
                module = importlib.import_module(module_name)

                # Find command class in module
                for attr in dir(module):
                    command_class = getattr(module, attr)
                    if isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand:
                        command_instance = command_class()
                        command_name = filename[:-3]
                        self.app.commands[command_name] = command_instance.execute

        # Register help and exit commands with access to the commands dictionary and app state
        self.app.commands["help"] = HelpCommand(self.app.commands).execute
        self.app.commands["exit"] = ExitCommand(self.app).execute
