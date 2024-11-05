# commands/add.py

from base.base_command import BaseCommand

class AddCommand(BaseCommand):
    def execute(self, x, y):
        try:
            result = float(x) + float(y)
            print(f"The result of {x} + {y} is {result}")
        except ValueError:
            print("Please provide two valid numbers.")

    @property
    def description(self):
        return "Add two numbers together."
