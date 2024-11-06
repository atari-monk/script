import os
import importlib
import sys
import logging
from base.base_command import BaseCommand
from base.base_module import BaseModule

# Configure logging
log_level = logging.WARNING  # Change to WARNING or ERROR to suppress lower-level logs
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them,
        including commands from subdirectories. Only files that contain a class subclassing
        'BaseCommand' will be treated as commands. Skips 'lib' folders.
        """
        command_folder = 'commands'
        
        # Log the current Python path to ensure the correct directories are included
        logger.debug("Python Path: %s", sys.path)  # This won't show up if log_level is WARNING or higher

        # Log where the command folder is located
        logger.debug("Command Folder: %s", os.path.abspath(command_folder))  # This won't show up either

        for dirpath, dirnames, filenames in os.walk(command_folder):
            # Skip the 'lib' directory if it is found
            if 'lib' in dirnames:
                dirnames.remove('lib')
                logger.debug("Skipping 'lib' folder in directory: %s", dirpath)  # This won't show up either

            logger.debug("Checking directory: %s", dirpath)  # This will also be suppressed

            for filename in filenames:
                # Skip the init and template files
                if filename.endswith(".py") and filename not in ["__init__.py"]:
                    # Log the module that will be loaded
                    logger.debug("Attempting to load module: %s", filename)  # This will be suppressed

                    try:
                        # Create module name by replacing slashes with dots
                        module_name = f"{dirpath.replace(os.sep, '.')}.{filename[:-3]}"
                        logger.debug("Module Name: %s", module_name)  # This won't show up

                        module = importlib.import_module(module_name)

                        for attr in dir(module):
                            command_class = getattr(module, attr)
                            if isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand:
                                logger.debug("Found BaseCommand subclass: %s", command_class)  # This will be suppressed

                                command_instance = command_class(self.app)  # Pass the app instance
                                
                                # Create a command name that includes the folder structure
                                relative_path = os.path.relpath(dirpath, command_folder)
                                if relative_path != '.':
                                    command_name = f"{relative_path.replace(os.sep, '/')}/{filename[:-3]}"
                                else:
                                    command_name = filename[:-3]  # Command name without .py extension
                                
                                # Register the command in the app's command registry
                                self.app.context.register_command(command_name, command_instance.execute)
                                logger.debug("Command '%s' registered.", command_name)  # This will also be suppressed
                                break  # We found a valid command, no need to continue checking other attributes
                    except ModuleNotFoundError as e:
                        logger.error("Module not found: %s", e)
                    except Exception as e:
                        logger.error("Error loading module '%s': %s", filename, str(e))
