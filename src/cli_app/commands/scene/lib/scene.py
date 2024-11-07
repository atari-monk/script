# Define the Scene, Entity, Component, and System data structures
from .entity import Entity

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
    