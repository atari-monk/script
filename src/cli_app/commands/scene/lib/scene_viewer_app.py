import json
import tkinter as tk
from tkinter import messagebox, ttk
from .scene import Scene

class SceneViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scene Viewer")
        self.file_path = "../../data/scenes.json"
        self.config_path = "../../config/sceneViewer.json"  # Path to the configuration file
        self.font_config = self.load_font_config()  # Load font configuration

        # Scrollable Frame
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame)
        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_content = tk.Frame(self.canvas)

        self.scrollable_content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Scene selection listbox
        self.scene_listbox = tk.Listbox(self.scrollable_content, font=(self.font_config["family"], self.font_config["size"]))
        self.scene_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.scene_listbox.bind("<<ListboxSelect>>", self.load_selected_scene)

        # Load scenes on initialization
        self.load_scenes()

        # Display area for scene details
        self.details_text = tk.Text(self.scrollable_content, height=15, wrap="word", font=(self.font_config["family"], self.font_config["size"]))
        self.details_text.pack(fill=tk.BOTH, padx=5, pady=5)

    def load_font_config(self):
        """Load font configuration from a separate JSON file."""
        with open(self.config_path, "r") as f:
            data = json.load(f)
            return data.get("font", {"family": "Arial", "size": 10})

    def load_scenes(self):
        """Load all scenes from the JSON file and populate the listbox."""
        try:
            scenes = self.load_all_scenes()
            self.scene_listbox.delete(0, tk.END)  # Clear the listbox
            for scene in scenes:
                self.scene_listbox.insert(tk.END, scene.path)  # Add scene paths to listbox
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scenes: {e}")

    def load_selected_scene(self, event=None):
        """Load the selected scene from the listbox."""
        selection = self.scene_listbox.curselection()
        if selection:
            scene_index = selection[0]
            scenes = self.load_all_scenes()
            selected_scene = scenes[scene_index]
            self.display_scene_details(selected_scene)

    def load_all_scenes(self):
        """Load scenes from JSON file."""
        with open(self.file_path, "r") as f:
            data = json.load(f)
            return [Scene.from_dict(item) for item in data]

    def display_scene_details(self, scene):
        """Display details of the selected scene."""
        details = (
            f"Path: {scene.path}\n"
            f"Name: {scene.name}\n"
            f"Description: {scene.description}\n"
            f"Image: {scene.image}\n"
            f"Entities:\n"
        )
        for entity in scene.entities:
            details += f"  - Name: {entity.name}, Components: {', '.join(entity.components)}, Systems: {', '.join(entity.systems)}\n"
        
        self.details_text.delete("1.0", tk.END)  # Clear previous details
        self.details_text.insert(tk.END, details)  # Insert new details
