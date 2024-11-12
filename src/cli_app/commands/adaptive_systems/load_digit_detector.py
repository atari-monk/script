from base.base_command import BaseCommand
from commands.adaptive_systems.lib.digit_classification import load_and_predict_mnist_model

class LoadDigitDetectorCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        load_and_predict_mnist_model()

    @property
    def description(self):
        return "Digit Classification Neural Network."
    