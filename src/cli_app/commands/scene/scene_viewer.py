import tkinter as tk
from base.base_command import BaseCommand
from .lib.scene_viewer_app import SceneViewerApp

class SceneViewerCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        root = tk.Tk()
        app = SceneViewerApp(root)
        root.mainloop()

    @property
    def description(self):
        return "Scene viewer."