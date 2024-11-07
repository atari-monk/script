from cli_app.commands.code.lib.CodeDescription import CodeDescription
from cli_app.commands.code.lib.codeForm import load_config
import json
import shutil
import tkinter as tk
from tkinter import messagebox, ttk

class CodeDescriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Description Form")

        # Load configuration
        self.config = load_config("../config/codeForm.json")
        self.font_config = self.config.get("font", {})
        self.path_config = self.config.get("paths", {})
        self.file_path_storage1 = self.path_config.get("storage1", "../data/code_descriptions.json")
        self.file_path_storage2 = self.path_config.get("storage2", "")

        self.font = (self.font_config.get("font_family", "Arial"), self.font_config.get("font_size", 12))

        # Load tags from JSON
        self.tags = CodeDescription.load_tags(self.file_path_storage1)

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

        # Main attributes
        self.name_var = tk.StringVar()
        self.description_text = tk.Text(self.scrollable_content, wrap="word", font=self.font)
        self.tag_var = tk.StringVar(value="None")  # Default value for tags
        self.tags_var = tk.StringVar()  # For comma-separated tags input

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
        tk.Entry(self.scrollable_content, textvariable=self.name_var, font=self.font).pack(fill=tk.X, padx=5)

        tk.Label(self.scrollable_content, text="Description:", font=self.font).pack(anchor="w", padx=5)
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5)  # Make description expand

        tk.Label(self.scrollable_content, text="Tags (comma-separated):", font=self.font).pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.tags_var, font=self.font).pack(fill=tk.X, padx=5)

        tk.Button(control_frame, text="Save Description", command=self.save_description).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(control_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Load descriptions on initialization
        self.load_descriptions()

    def bind_mouse_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def save_description(self):
        description_data = self.get_description_data()

        # Load existing descriptions
        descriptions = self.load_all_descriptions()

        # Add the new description or update existing one
        existing_description = next((d for d in descriptions if d.name == description_data.name), None)
        if existing_description:
            descriptions.remove(existing_description)

        descriptions.append(description_data)

        # Save to storage1 and copy to storage2 if specified
        try:
            # Save to storage1
            with open(self.file_path_storage1, "w") as f:
                json.dump([desc.to_dict() for desc in descriptions], f, indent=2)

            # Copy to storage2 if path is specified
            if self.file_path_storage2:
                shutil.copy(self.file_path_storage1, self.file_path_storage2)

            messagebox.showinfo("Success", "Description saved and copied successfully!")
            self.load_descriptions()  # Reload the descriptions after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save and copy description: {e}")

    def get_description_data(self):
        tags_input = self.tags_var.get()
        tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]  # Split and clean tags
        return CodeDescription(
            name=self.name_var.get(),
            description=self.description_text.get("1.0", tk.END).strip(),
            tags=tags_list if tags_list else ["None"]
        )

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

            self.name_var.set(selected_description.name)
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_description.description)
            self.tags_var.set(", ".join(selected_description.tags))  # Populate tags entry

    def load_all_descriptions(self):
        # Load descriptions from JSON file
        with open(self.file_path_storage1, "r") as f:
            data = json.load(f)
            return [CodeDescription.from_dict(item) for item in data]

    def clear_form(self):
        # Clear all fields in the form
        self.name_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.tags_var.set("")  # Clear tags input
        self.tag_var.set("None")  # Reset tag to default
        