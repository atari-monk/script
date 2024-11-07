import json
import tkinter as tk
from tkinter import messagebox, ttk
from .entity import Entity
from .scene import Scene

class SceneFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scene Form")
        self.file_path = "../../data/scenes.json"
        self.config_path = "../../config/sceneForm.json"

        # Load font size from config
        self.font_size = self.load_font_size()
        self.root.option_add("*Font", f"{self.font_size}pt")

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
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Main scene attributes
        self.path_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.image_var = tk.StringVar()
        self.description_text = tk.Text(self.scrollable_content, height=3, wrap="word")
        self.entities = []

        # Scene selection listbox
        self.scene_listbox = tk.Listbox(self.scrollable_content)
        self.scene_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.scene_listbox.bind("<<ListboxSelect>>", self.load_selected_scene)

        # Main scene form
        tk.Label(self.scrollable_content, text="Path:").pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.path_var).pack(fill=tk.X, padx=5)
        tk.Label(self.scrollable_content, text="Name:").pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.name_var).pack(fill=tk.X, padx=5)
        tk.Label(self.scrollable_content, text="Description:").pack(anchor="w", padx=5)
        self.description_text.pack(fill=tk.X, padx=5)
        tk.Label(self.scrollable_content, text="Image:").pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.image_var).pack(fill=tk.X, padx=5)

        # Entity section with Add/Remove buttons
        self.entity_frame = tk.Frame(self.scrollable_content)
        self.entity_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(self.entity_frame, text="Entities").pack(anchor="w")
        self.add_entity_button = tk.Button(self.entity_frame, text="Add Entity", command=self.add_entity_form)
        self.add_entity_button.pack(anchor="w", pady=5)

        # Control buttons
        control_frame = tk.Frame(self.scrollable_content)
        control_frame.pack(pady=5)
        tk.Button(control_frame, text="Save Scene", command=self.save_scene).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # Load scenes on initialization
        self.load_scenes()

    def load_font_size(self):
        """Load font size from JSON configuration."""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                return config.get("font_size", 12)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return 12

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta // 120)), "units")

    def add_entity_form(self):
        # Create a new frame for each entity
        entity_frame = tk.Frame(self.entity_frame, bd=1, relief="sunken", padx=5, pady=5)
        entity_frame.pack(fill="x", pady=5)

        # Entity name entry
        name_var = tk.StringVar()
        components_var = tk.StringVar()
        systems_var = tk.Text(entity_frame, height=3, wrap="word")

        # Add widgets for name, components, and systems with proper layout
        tk.Label(entity_frame, text="Entity Name:").grid(row=0, column=0, sticky="w")
        tk.Entry(entity_frame, textvariable=name_var).grid(row=0, column=1, sticky="ew", padx=5)
        tk.Label(entity_frame, text="Components (comma-separated):").grid(row=1, column=0, sticky="w")
        tk.Entry(entity_frame, textvariable=components_var).grid(row=1, column=1, sticky="ew", padx=5)
        tk.Label(entity_frame, text="Systems (comma-separated):").grid(row=2, column=0, sticky="nw")
        systems_var.grid(row=2, column=1, sticky="ew", padx=5)

        # Add the remove button
        remove_button = tk.Button(entity_frame, text="Remove Entity", command=lambda: self.remove_entity_form(entity_frame))
        remove_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Store references to the new entity's data in self.entities list
        self.entities.append({"name": name_var, "components": components_var, "systems": systems_var})
        self.entity_frame.update_idletasks()

    def remove_entity_form(self, entity_frame):
        # Find the entity in self.entities that corresponds to this frame and remove it
        entity_to_remove = next((e for e in self.entities if e["systems"].master == entity_frame), None)
        if entity_to_remove:
            self.entities.remove(entity_to_remove)
        entity_frame.destroy()


    def get_scene_data(self):
        scene = Scene(
            path=self.path_var.get(),
            name=self.name_var.get(),
            description=self.description_text.get("1.0", tk.END).strip(),
            image=self.image_var.get(),
            entities=[
                Entity(
                    name=e["name"].get(),
                    components=[c.strip() for c in e["components"].get().split(",") if c.strip()],
                    systems=[s.strip() for s in e["systems"].get("1.0", tk.END).split(",") if s.strip()]
                ) for e in self.entities
            ]
        )
        return scene

    def save_scene(self):
        scenes = self.load_all_scenes()
        scene_data = self.get_scene_data()
        existing_scene = next((s for s in scenes if s.path == scene_data.path), None)
        if existing_scene:
            scenes.remove(existing_scene)
        scenes.append(scene_data)
        try:
            with open(self.file_path, "w") as f:
                json.dump([scene.to_dict() for scene in scenes], f, indent=2)
            messagebox.showinfo("Success", "Scene saved successfully!")
            self.load_scenes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scene: {e}")

    def load_scenes(self):
        try:
            scenes = self.load_all_scenes()
            self.scene_listbox.delete(0, tk.END)
            for scene in scenes:
                self.scene_listbox.insert(tk.END, scene.path)
            if scenes:
                self.load_selected_scene()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scenes: {e}")

    def load_selected_scene(self, event=None):
        selection = self.scene_listbox.curselection()
        if not selection:
            return
        selected_scene_path = self.scene_listbox.get(selection[0])
        scenes = self.load_all_scenes()
        selected_scene = next((s for s in scenes if s.path == selected_scene_path), None)
        if selected_scene:
            self.clear_form()
            self.path_var.set(selected_scene.path)
            self.name_var.set(selected_scene.name)
            self.image_var.set(selected_scene.image)
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_scene.description)
            for entity in selected_scene.entities:
                self.add_entity_form()
                entity_entry = self.entities[-1]
                entity_entry["name"].set(entity.name)
                entity_entry["components"].set(", ".join(entity.components))
                entity_entry["systems"].delete("1.0", tk.END)
                entity_entry["systems"].insert("1.0", ", ".join(entity.systems))

    def clear_form(self):
        self.path_var.set("")
        self.name_var.set("")
        self.image_var.set("")
        self.description_text.delete("1.0", tk.END)

        # Remove all dynamically created entity frames (excluding the "Add Entity" button)
        for entity_frame in self.entity_frame.winfo_children():
            if entity_frame != self.add_entity_button:
                entity_frame.destroy()
                
        # Clear the entities list to reset the form
        self.entities.clear()

    def load_all_scenes(self):
        try:
            with open(self.file_path, "r") as f:
                scenes_data = json.load(f)
                return [Scene.from_dict(s) for s in scenes_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
