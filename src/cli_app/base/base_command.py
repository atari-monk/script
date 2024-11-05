# commands/base_command.py

from abc import ABC, abstractmethod

class BaseCommand(ABC):
    @abstractmethod
    def execute(self, *args):
        """
        Execute the command. This method must be implemented by all command subclasses.
        """
        pass

    @property
    def description(self):
        """
        Return a brief description of the command.
        """
        return "No description provided"
