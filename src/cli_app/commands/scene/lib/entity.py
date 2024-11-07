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