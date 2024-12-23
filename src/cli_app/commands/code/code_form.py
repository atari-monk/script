import tkinter as tk
from base.base_command import BaseCommand
from .lib.code_form_app import CodeFormApp

class CodeFormCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        root = tk.Tk()
        app = CodeFormApp(root, '../../data/code_descriptions.json')
        root.mainloop()

    @property
    def description(self):
        return "Code form."