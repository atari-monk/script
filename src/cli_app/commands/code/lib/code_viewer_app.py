import tkinter as tk
from tkinter import messagebox, ttk
from .database_context import DatabaseContext

class CodeViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Viewer")

        self.db = DatabaseContext("../../data/code_descriptions.json")  # Use DatabaseContext

        # Load configuration and tags
        self.config = self.db.load_config("../../config/codeForm.json")
        self.font = (self.config.get("font_family", "Arial"), self.config.get("font_size", 12))
        self.tags = self.load_tags()

        # Setup Scrollable Frame
        self.setup_scrollable_frame()

        # Setup GUI controls and widgets
        self.setup_controls()

        # Load descriptions on initialization
        self.load_descriptions()

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

    def setup_controls(self):
        """Setup the controls like labels, dropdown, listbox, and buttons."""
        control_frame = tk.Frame(self.scrollable_content)
        control_frame.pack(pady=5, fill=tk.X)

        tk.Label(self.scrollable_content, text="Tag:", font=self.font).pack(anchor="w", padx=5)
        self.tag_var = tk.StringVar(value="None")
        self.tag_dropdown = ttk.Combobox(control_frame, textvariable=self.tag_var, values=self.tags, state="readonly", font=self.font)
        self.tag_dropdown.pack(side=tk.LEFT, padx=5)
        self.tag_dropdown.bind("<<ComboboxSelected>>", self.load_descriptions)

        self.name_listbox = tk.Listbox(self.scrollable_content, font=self.font)
        self.name_listbox.pack(fill=tk.X, padx=5, pady=5)
        self.name_listbox.bind("<<ListboxSelect>>", self.load_selected_description)

        tk.Label(self.scrollable_content, text="Name:", font=self.font).pack(anchor="w", padx=5)
        self.name_label = tk.Label(self.scrollable_content, text="", font=self.font)
        self.name_label.pack(fill=tk.X, padx=5)

        tk.Label(self.scrollable_content, text="Description:", font=self.font).pack(anchor="w", padx=5)
        self.description_text = tk.Text(self.scrollable_content, wrap="word", font=self.font, state="disabled")
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5)

    def bind_mouse_wheel(self):
        """Bind mouse wheel scrolling."""
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_tags(self):
        """Load tags from the database."""
        return self.db.get_all_tags()

    def load_descriptions(self, event=None):
        """Load descriptions from the database based on the selected tag."""
        try:
            descriptions = self.db.get_all_descriptions()
            self.name_listbox.delete(0, tk.END)

            selected_tag = self.tag_var.get()
            for desc in descriptions:
                if selected_tag == "None" or selected_tag in desc.tags:
                    self.name_listbox.insert(tk.END, desc.name)

            self.clear_form()

            # Set the tag_var to the selected tag if it's in the list
            if selected_tag in self.tags:
                self.tag_var.set(selected_tag)
            else:
                self.tag_var.set("None")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load descriptions: {e}")

    def load_selected_description(self, event=None):
        """Load the description of the selected item."""
        selection = self.name_listbox.curselection()
        if selection:
            index = selection[0]
            descriptions = self.db.get_all_descriptions()
            selected_description = descriptions[index]

            self.name_label.config(text=selected_description.name)  # Display name
            self.description_text.config(state="normal")  # Enable text widget
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, selected_description.description)
            self.description_text.config(state="disabled")  # Set back to read-only

    def clear_form(self):
        """Clear the form."""
        self.name_label.config(text="")
        self.description_text.config(state="normal")  # Enable text widget to clear
        self.description_text.delete("1.0", tk.END)
        self.description_text.config(state="disabled")  # Set back to read-only
