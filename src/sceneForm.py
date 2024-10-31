import json
import tkinter as tk
from tkinter import messagebox, ttk

# Define the Scene, Entity, Component, and System data structures
class Scene:
    def __init__(self, path='', name='', description='', image='', entities=None):
        self.path = path
        self.name = name
        self.description = description
        self.image = image
        self.entities = entities if entities is not None else []

    def to_dict(self):
        return {
            "path": self.path,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "entities": [entity.to_dict() for entity in self.entities]
        }

    @staticmethod
    def from_dict(data):
        scene = Scene(
            path=data.get("path", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            image=data.get("image", ""),
            entities=[Entity.from_dict(e) for e in data.get("entities", [])]
        )
        return scene

class Entity:
    def __init__(self, name='', components=None, systems=None):
        self.name = name
        self.components = components if components is not None else []
        self.systems = systems if systems is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "components": self.components,
            "systems": self.systems
        }

    @staticmethod
    def from_dict(data):
        return Entity(
            name=data.get("name", ""),
            components=data.get("components", []),
            systems=data.get("systems", [])
        )

# GUI Application
class SceneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scene Form")
        self.file_path = "data/scenes.json"
        self.config_path = "config/sceneForm.json"

        # Load font size from config
        self.font_size = self.load_font_size()

        # Apply font size to the root
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

        # Bind mouse wheel scroll to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Main scene attributes
        self.path_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.image_var = tk.StringVar()
        self.description_text = tk.Text(self.scrollable_content, height=3, wrap="word")

        # Entities storage
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
                return config.get("font_size", 12)  # Default font size
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return 12  # Default font size
        
    def on_mouse_wheel(self, event):
        # Scroll the canvas based on mouse wheel movement
        self.canvas.yview_scroll(int(-1*(event.delta // 120)), "units")

    def add_entity_form(self):
        # New frame for each entity
        entity = Entity(name="")
        entity_frame = tk.Frame(self.entity_frame, bd=1, relief="sunken", padx=5, pady=5)
        entity_frame.pack(fill="x", pady=5)

        # Entity name entry
        name_var = tk.StringVar()
        entity.name = name_var
        tk.Label(entity_frame, text="Entity Name:").grid(row=0, column=0, sticky="w")
        tk.Entry(entity_frame, textvariable=name_var).grid(row=0, column=1, sticky="ew", padx=5)

        # Components and Systems input for the entity
        components_var = tk.StringVar()
        systems_var = tk.StringVar()

        tk.Label(entity_frame, text="Components (comma-separated):").grid(row=1, column=0, sticky="w")
        tk.Entry(entity_frame, textvariable=components_var).grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(entity_frame, text="Systems (comma-separated):").grid(row=2, column=0, sticky="w")
        tk.Entry(entity_frame, textvariable=systems_var).grid(row=2, column=1, sticky="ew", padx=5)

        # Remove button
        remove_button = tk.Button(entity_frame, text="Remove Entity", command=lambda: self.remove_entity_form(entity, entity_frame))
        remove_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Store the entity
        entity.components = components_var
        entity.systems = systems_var
        self.entities.append((entity, entity_frame))

    def remove_entity_form(self, entity, entity_frame):
        # Remove the entity form
        entity_frame.destroy()
        self.entities = [(e, f) for e, f in self.entities if f != entity_frame]

    def get_scene_data(self):
        # Build scene data from form
        scene = Scene(
            path=self.path_var.get(),
            name=self.name_var.get(),
            description=self.description_text.get("1.0", tk.END).strip(),
            image=self.image_var.get(),
            entities=[Entity(
                name=e[0].name.get(),
                components=[c.strip() for c in e[0].components.get().split(",") if c.strip()],
                systems=[s.strip() for s in e[0].systems.get().split(",") if s.strip()]
            ) for e in self.entities]
        )
        return scene

    def save_scene(self):
        scenes = self.load_all_scenes()  # Load existing scenes
        scene_data = self.get_scene_data()

        # Check if the scene path already exists
        existing_scene = next((s for s in scenes if s.path == scene_data.path), None)
        if existing_scene:
            scenes.remove(existing_scene)  # Remove the old scene

        scenes.append(scene_data)  # Add the updated scene

        try:
            with open(self.file_path, "w") as f:
                json.dump([scene.to_dict() for scene in scenes], f, indent=2)
            messagebox.showinfo("Success", "Scene saved successfully!")
            self.load_scenes()  # Reload the scenes after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scene: {e}")

    def load_scenes(self):
        # Load all scenes from the JSON file and populate the listbox
        try:
            scenes = self.load_all_scenes()
            self.scene_listbox.delete(0, tk.END)  # Clear the listbox
            for scene in scenes:
                self.scene_listbox.insert(tk.END, scene.path)  # Add scene paths to listbox
            if scenes:  # Load the first scene by default
                self.load_selected_scene()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scenes: {e}")

    def load_selected_scene(self, event=None):
        # Load the selected scene from the listbox
        selection = self.scene_listbox.curselection()
        if selection:
            scene_index = selection[0]
            scenes = self.load_all_scenes()
            selected_scene = scenes[scene_index]
            self.path_var.set(selected_scene.path)
            self.name_var.set(selected_scene.name)
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_scene.description)
            self.image_var.set(selected_scene.image)
            self.entities.clear()  # Clear current entities
            for entity_data in selected_scene.entities:
                self.add_entity_form()
                entity, entity_frame = self.entities[-1]
                entity.name.set(entity_data.name)
                entity.components.set(", ".join(entity_data.components))
                entity.systems.set(", ".join(entity_data.systems))

    def load_all_scenes(self):
        # Load scenes from JSON file
        with open(self.file_path, "r") as f:
            data = json.load(f)
            return [Scene.from_dict(item) for item in data]

    def clear_form(self):
        # Clear all fields in the form except the scene listbox
        self.path_var.set("")
        self.name_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.image_var.set("")

        # Clear all entity forms
        for entity, entity_frame in self.entities:
            entity_frame.destroy()  # Destroy each entity frame
        self.entities.clear()  # Clear the entities list


if __name__ == "__main__":
    root = tk.Tk()
    app = SceneApp(root)
    root.mainloop()
