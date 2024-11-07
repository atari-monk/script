import tkinter as tk
from base.base_command import BaseCommand
from .lib.code_viewer_app import CodeViewerApp

class CodeViewerCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        root = tk.Tk()
        app = CodeViewerApp(root)
        root.mainloop()

    @property
    def description(self):
        return "Code Viewer."