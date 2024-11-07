import json
from tkinter import messagebox

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
                tags.add("None")
                sorted_tags = sorted(tags)
                sorted_tags.remove("None")
                return ["None"] + sorted_tags
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tags: {e}")
            return ["None"]
        