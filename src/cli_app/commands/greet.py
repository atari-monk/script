# commands/greet.py

from base.base_command import BaseCommand

class GreetCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, name="World"):
        print(f"Hello, {name}!")

    @property
    def description(self):
        return "Greet a person by name."
