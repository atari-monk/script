import shutil
import tkinter as tk
from tkinter import messagebox, ttk
from .code_description import CodeDescription
from .database_context import DatabaseContext

class CodeDescriptionApp:
    def __init__(self, root, db_path):
        self.root = root
        self.root.title("Code Description Form")
        
        # Initialize the database context (now with JSON file as the "database")
        self.db = DatabaseContext(db_path)
        
        # Load configuration settings (unchanged)
        self.load_config()

        # Load tags from database
        self.tags = self.load_tags_from_db()

        # Setup GUI components
        self.setup_scrollable_frame()
        self.setup_control_frame()
        self.setup_name_listbox()

        # Load descriptions initially (unchanged)
        self.load_descriptions()

    def load_config(self):
        """Load configuration settings from the database."""
        self.config = self.db.load_config("../../config/codeForm.json")
        self.font_config = self.config.get("font", {})
        self.path_config = self.config.get("paths", {})
        self.file_path_storage1 = self.path_config.get("storage1", "../data/code_descriptions.json")
        self.file_path_storage2 = self.path_config.get("storage2", "")
        self.font = (self.font_config.get("font_family", "Arial"), self.font_config.get("font_size", 12))

    def setup_scrollable_frame(self):
        """Setup the scrollable frame and canvas."""
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_content = tk.Frame(self.canvas)
        self.scrollable_content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.bind_mouse_wheel()

    def setup_control_frame(self):
        """Setup the control frame with input elements."""
        control_frame = tk.Frame(self.scrollable_content)
        control_frame.pack(pady=5, fill=tk.X)

        # Tag dropdown
        tk.Label(self.scrollable_content, text="Tag:", font=self.font).pack(anchor="w", padx=5)
        self.tag_var = tk.StringVar(value="None")
        self.tag_dropdown = ttk.Combobox(control_frame, textvariable=self.tag_var, values=self.tags, state="readonly", font=self.font)
        self.tag_dropdown.pack(side=tk.LEFT, padx=5)
        self.tag_dropdown.bind("<<ComboboxSelected>>", self.load_descriptions)

        # Save and clear buttons
        tk.Button(control_frame, text="Save Description", command=self.save_description).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(control_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def setup_name_listbox(self):
        """Setup the name listbox and text fields."""
        self.name_var = tk.StringVar()
        self.description_text = tk.Text(self.scrollable_content, wrap="word", font=self.font)
        self.tags_var = tk.StringVar()

        # Name listbox
        self.name_listbox = tk.Listbox(self.scrollable_content, font=self.font)
        self.name_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.name_listbox.bind("<<ListboxSelect>>", self.load_selected_description)

        # Name input
        tk.Label(self.scrollable_content, text="Name:", font=self.font).pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.name_var, font=self.font).pack(fill=tk.X, padx=5)

        # Description input
        tk.Label(self.scrollable_content, text="Description:", font=self.font).pack(anchor="w", padx=5)
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5)

        # Tags input
        tk.Label(self.scrollable_content, text="Tags (comma-separated):", font=self.font).pack(anchor="w", padx=5)
        tk.Entry(self.scrollable_content, textvariable=self.tags_var, font=self.font).pack(fill=tk.X, padx=5)

    def bind_mouse_wheel(self):
        """Bind mouse wheel to scroll canvas."""
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        """Scroll canvas on mouse wheel movement."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def save_description(self):
        """Save the description to the database."""
        description_data = self.get_description_data()
        existing_description = self.db.get_description_by_name(description_data.name)

        if existing_description:
            self.db.update_description(description_data)
        else:
            self.db.insert_description(description_data)

        # Optionally, copy to another storage path
        if self.file_path_storage2:
            shutil.copy(self.file_path_storage1, self.file_path_storage2)

        messagebox.showinfo("Success", "Description saved successfully!")
        self.load_descriptions()

    def get_description_data(self):
        """Retrieve description data from the form."""
        tags_input = self.tags_var.get()
        tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        return CodeDescription(
            name=self.name_var.get(),
            description=self.description_text.get("1.0", tk.END).strip(),
            tags=tags_list if tags_list else ["None"]
        )

    def load_descriptions(self, event=None):
        """Load all descriptions and filter by selected tag."""
        try:
            descriptions = self.db.get_all_descriptions()
            self.name_listbox.delete(0, tk.END)

            selected_tag = self.tag_var.get()
            for desc in descriptions:
                if selected_tag == "None" or selected_tag in desc.tags:
                    self.name_listbox.insert(tk.END, desc.name)

            self.clear_form()

            if selected_tag in self.tags:
                self.tag_var.set(selected_tag)
            else:
                self.tag_var.set("None")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load descriptions: {e}")

    def load_selected_description(self, event=None):
        """Load the selected description into the form."""
        selection = self.name_listbox.curselection()
        if selection:
            index = selection[0]
            descriptions = self.db.get_all_descriptions()
            selected_description = descriptions[index]

            self.name_var.set(selected_description.name)
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_description.description)
            self.tags_var.set(", ".join(selected_description.tags))

    def load_tags_from_db(self):
        """Retrieve all unique tags from descriptions in the database."""
        descriptions = self.db.get_all_descriptions()
        tags = set()
        for desc in descriptions:
            tags.update(desc.tags)
        tags.add("None")
        return sorted(tags)

    def clear_form(self):
        """Clear all input fields in the form."""
        self.name_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.tags_var.set("")
        self.tag_var.set("None")
