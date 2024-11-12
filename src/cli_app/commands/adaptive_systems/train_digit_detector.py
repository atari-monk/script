from base.base_command import BaseCommand
from commands.adaptive_systems.lib.digit_classification import train_and_save_mnist_model

class TrainDigitDetectorCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        train_and_save_mnist_model()

    @property
    def description(self):
        return "Digit Classification Neural Network."
    