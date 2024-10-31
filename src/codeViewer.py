import json
import tkinter as tk
from tkinter import messagebox, ttk

# Define the CodeDescription data structure
class CodeDescription:
    def __init__(self, name='', description='', tags=None):
        self.name = name
        self.description = description
        self.tags = tags if tags is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags
        }

    @staticmethod
    def from_dict(data):
        return CodeDescription(
            name=data.get("name", ""),
            description=data.get("description", ""),
            tags=data.get("tags", [])
        )

    @staticmethod
    def load_tags(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                tags = set()
                for item in data:
                    tags.update(item.get("tags", []))
                tags.add("None")  # Ensure "None" is included
                sorted_tags = sorted(tags)  # Sort tags
                # Ensure "None" is the first element
                sorted_tags.remove("None")
                return ["None"] + sorted_tags  # Return list with "None" first
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tags: {e}")
            return ["None"]  # Default to ["None"]

# Load configuration settings from JSON
def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load config: {e}")
        return {"font_family": "Arial", "font_size": 12}  # Default values

# GUI Application
class CodeViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Viewer")
        self.file_path = "data/code_descriptions.json"
        self.config = load_config("config/codeForm.json")  # Load font configuration
        self.font = (self.config.get("font_family", "Arial"), self.config.get("font_size", 12))

        # Load tags from JSON
        self.tags = CodeDescription.load_tags(self.file_path)

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

        # Bind mouse wheel for scrolling
        self.bind_mouse_wheel()

        # Control variables
        self.tag_var = tk.StringVar(value="None")  # Default value for tags

        # Control buttons
        control_frame = tk.Frame(self.scrollable_content)
        control_frame.pack(pady=5, fill=tk.X)

        tk.Label(self.scrollable_content, text="Tag:", font=self.font).pack(anchor="w", padx=5)
        self.tag_dropdown = ttk.Combobox(control_frame, textvariable=self.tag_var, values=self.tags, state="readonly", font=self.font)
        self.tag_dropdown.pack(side=tk.LEFT, padx=5)
        self.tag_dropdown.bind("<<ComboboxSelected>>", self.load_descriptions)

        # Listbox for names
        self.name_listbox = tk.Listbox(self.scrollable_content, font=self.font)
        self.name_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.name_listbox.bind("<<ListboxSelect>>", self.load_selected_description)

        tk.Label(self.scrollable_content, text="Name:", font=self.font).pack(anchor="w", padx=5)
        self.name_label = tk.Label(self.scrollable_content, text="", font=self.font)
        self.name_label.pack(fill=tk.X, padx=5)

        tk.Label(self.scrollable_content, text="Description:", font=self.font).pack(anchor="w", padx=5)
        self.description_text = tk.Text(self.scrollable_content, wrap="word", font=self.font, state="disabled")  # Read-only
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5)  # Make description expand

        # Load descriptions on initialization
        self.load_descriptions()

    def bind_mouse_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_descriptions(self, event=None):
        try:
            descriptions = self.load_all_descriptions()
            self.name_listbox.delete(0, tk.END)  # Clear the listbox

            # Filter descriptions based on selected tag
            selected_tag = self.tag_var.get()
            for desc in descriptions:
                if selected_tag == "None" or selected_tag in desc.tags:
                    self.name_listbox.insert(tk.END, desc.name)

            # Clear the form after loading
            self.clear_form()

            # Set the tag_var to the selected tag if it's in the list
            if selected_tag in self.tags:
                self.tag_var.set(selected_tag)
            else:
                self.tag_var.set("None")  # Default to None if not in list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load descriptions: {e}")

    def load_selected_description(self, event=None):
        selection = self.name_listbox.curselection()
        if selection:
            index = selection[0]
            descriptions = self.load_all_descriptions()
            selected_description = descriptions[index]

            self.name_label.config(text=selected_description.name)  # Display name
            self.description_text.config(state="normal")  # Enable text widget
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_description.description)
            self.description_text.config(state="disabled")  # Set back to read-only

    def load_all_descriptions(self):
        # Load descriptions from JSON file
        with open(self.file_path, "r") as f:
            data = json.load(f)
            return [CodeDescription.from_dict(item) for item in data]

    def clear_form(self):
        # Clear all fields in the form
        self.name_label.config(text="")
        self.description_text.config(state="normal")  # Enable text widget to clear
        self.description_text.delete("1.0", tk.END)
        self.description_text.config(state="disabled")  # Set back to read-only

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeViewerApp(root)
    root.mainloop()
