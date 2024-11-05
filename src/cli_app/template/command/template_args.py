from base.base_command import BaseCommand

class TemplateArgsCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        if len(args) != 1:
            print("Error: One argument required - arg1.")
            return

        arg1 = args

        try:
            if not self.is_valid_arg1(arg1):
                print("Invalid arg1 format. Arg1 must be alphanumeric or contain underscores.")
                return
        except ValueError as e:
            print(f"Error: {e}.")

    @property
    def description(self):
        return "Command help."
