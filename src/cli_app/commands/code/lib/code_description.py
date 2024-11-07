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
        