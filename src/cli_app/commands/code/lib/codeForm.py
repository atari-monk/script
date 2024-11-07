import json
import tkinter as tk
from tkinter import messagebox
from cli_app.commands.code.lib.CodeDescriptionApp import CodeDescriptionApp

# Load configuration settings from JSON
def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load config: {e}")
        return {
            "font": {"font_family": "Arial", "font_size": 12},
            "paths": {"data_file": {"storage1": "data/code_descriptions.json", "storage2": ""}}
        }  # Default values

# GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeDescriptionApp(root)
    root.mainloop()
