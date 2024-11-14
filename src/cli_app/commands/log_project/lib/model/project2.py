import logging
from shared.validator import Validator

logger = logging.getLogger(__name__)

class Project2:
    def __init__(
        self, id: int, name: str, description: str
    ):
        self.id = id
        self.name = name
        self.description = description
        
    @staticmethod
    def parse_data(id: int, name: str, description: str) -> dict:
        data = {'id': id}
        if name is not None:
            data['name'] = Validator.validate_name(name.strip())
        if description is not None:
            data['description'] = Validator.validate_description(description.strip())
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project2':
        # Assumes `data` contains all keys that match the __init__ parameters of `Project` with compatible value types.
        return cls(**data)
    
    def to_dict(self) -> dict:
        """
        Converts the Project object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def __repr__(self):
        return (f"Project(id={self.id}), name={self.name}, description={self.description}")
    