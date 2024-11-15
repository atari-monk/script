import logging
import os
import importlib
import sys
from base.base_command import BaseCommand
from base.base_module import BaseModule

logger = logging.getLogger(__name__)

class CommandLoaderModule(BaseModule):
    def initialize(self):
        """
        Dynamically load command classes from the 'commands' folder and register them,
        including commands from subdirectories. Only files that contain a class subclassing
        'BaseCommand' will be treated as commands. Skips 'lib' and 'tests' folders.
        """
        command_folder = 'commands'
        
        # Log Python path and command folder for debugging
        self._log_paths(command_folder)
        
        # Walk through the command directory structure
        for dirpath, dirnames, filenames in os.walk(command_folder):
            # Skip 'lib' and 'tests' directories
            self._skip_folders(dirnames, dirpath)

            logger.debug("Checking directory: %s", dirpath)

            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":
                    self._load_and_register_command(dirpath, filename)

    def _log_paths(self, command_folder):
        """Log Python path and command folder for debugging."""
        logger.debug("Python Path: %s", sys.path)
        logger.debug("Command Folder: %s", os.path.abspath(command_folder))

    def _skip_folders(self, dirnames, dirpath):
        """Skip 'lib' and 'tests' folders."""
        if 'lib' in dirnames:
            dirnames.remove('lib')
            logger.debug("Skipping 'lib' folder in directory: %s", dirpath)
        if 'tests' in dirnames:
            dirnames.remove('tests')
            logger.debug("Skipping 'tests' folder in directory: %s", dirpath)

    def _load_and_register_command(self, dirpath, filename):
        """Load and register command class from the module."""
        try:
            module_name = self._get_module_name(dirpath, filename)
            module = importlib.import_module(module_name)

            for attr in dir(module):
                command_class = getattr(module, attr)
                if self._is_valid_command_class(command_class):
                    command_instance = command_class(self.app)
                    command_name = self._get_command_name(dirpath, filename)
                    self.app.context.register_command(command_name, command_instance.execute)
                    logger.debug("Command '%s' registered.", command_name)
                    break  # Command found, no need to check other attributes
        except ModuleNotFoundError as e:
            logger.error("Module not found: %s", e)
        except Exception as e:
            logger.error("Error loading module '%s': %s", filename, str(e))

    def _get_module_name(self, dirpath, filename):
        """Generate module name from directory and filename."""
        return f"{dirpath.replace(os.sep, '.')}.{filename[:-3]}"

    def _is_valid_command_class(self, command_class):
        """Check if the class is a valid subclass of BaseCommand."""
        return isinstance(command_class, type) and issubclass(command_class, BaseCommand) and command_class is not BaseCommand

    def _get_command_name(self, dirpath, filename):
        """Generate command name based on folder structure."""
        relative_path = os.path.relpath(dirpath, 'commands')
        if relative_path != '.':
            return f"{relative_path.replace(os.sep, '/')}/{filename[:-3]}"
        return filename[:-3]  # Command name without .py extension
