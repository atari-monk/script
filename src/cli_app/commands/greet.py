# commands/greet.py

from base.base_command import BaseCommand

class GreetCommand(BaseCommand):
    def execute(self, name="World"):
        print(f"Hello, {name}!")

    @property
    def description(self):
        return "Greet a person by name."
