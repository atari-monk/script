import tkinter as tk
from base.base_command import BaseCommand
from .lib.scene_form_app import SceneFormApp

class SceneFormCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        root = tk.Tk()
        app = SceneFormApp(root)
        root.mainloop()

    @property
    def description(self):
        return "Scene form."