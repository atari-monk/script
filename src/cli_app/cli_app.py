from app_context import AppContext
from modules.command_loader import CommandLoaderModule
from modules.run_module import RunModule
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

class CLIApp:
    def __init__(self):
        self.context = AppContext()
        self.command_loader = CommandLoaderModule(self)
        self.run_module = RunModule(self)
        self.running = False

    def start(self):
        """
        Start the application by initializing modules and running the main loop.
        """
        self.running = True
        self.command_loader.initialize()
        self.run_module.initialize()

if __name__ == "__main__":
    app = CLIApp()
    app.start()
