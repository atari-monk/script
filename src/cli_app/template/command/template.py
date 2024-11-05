from base.base_command import BaseCommand

class TemplateCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        return

    @property
    def description(self):
        return "Command help."