# base_module.py

class BaseModule:
    def __init__(self, app):
        self.app = app  # Reference to the main CLI application

    def initialize(self):
        """
        Placeholder method to initialize the module.
        This method should be implemented by derived classes.
        """
        raise NotImplementedError("Initialize method must be implemented by subclasses.")
