# main.py

from modules.command_loader import CommandLoaderModule
from modules.run_module import RunModule

class CLIApp:
    def __init__(self):
        self.commands = {}
        self.running = True
        self.command_loader = CommandLoaderModule(self)
        self.run_module = RunModule(self)

    def start(self):
        """
        Start the application by initializing modules and running the main loop.
        """
        self.command_loader.initialize()
        self.run_module.initialize()

if __name__ == "__main__":
    app = CLIApp()
    app.start()
