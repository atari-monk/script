from base.base_command import BaseCommand
from commands.adaptive_systems.lib.digit_drawer import DigitDrawer

class DigitDrawerCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        digit_drawer = DigitDrawer()  # Initialize the class
        digit_drawer.start_gui()

    @property
    def description(self):
        return "Digit Classification Neural Network, drawing digit and classifying it."
    