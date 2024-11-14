import logging
from typing import Optional
from urllib.parse import urlparse, ParseResult
from shared.validator import Validator

logger = logging.getLogger(__name__)

class Project2:
    def __init__(
        self, id: int, name: str, description: str, repo_link: Optional[ParseResult] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.repo_link = repo_link
        
    @staticmethod
    def parse_data(id: int, name: str, description: str, repo_link: str) -> dict:
        data = {'id': id}
        if name is not None:
            data['name'] = Validator.validate_name(name.strip())
        if description is not None:
            data['description'] = Validator.validate_description(description.strip())
        if repo_link is not None:
            data['repo_link'] = urlparse(repo_link.strip())
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project2':
        # Assumes `data` contains all keys that match the __init__ parameters of `Project` with compatible value types.
        # Check if 'repo_link' is already a URL instance or needs to be converted
        if 'repo_link' in data and isinstance(data['repo_link'], str):
            data['repo_link'] = urlparse(data['repo_link'])  # Convert string to ParseResult object
        return cls(**data)
    
    def to_dict(self) -> dict:
        """
        Converts the Project object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'repo_link': self.repo_link.geturl() if self.repo_link else None
        }
    
    def __repr__(self):
        return (f"Project(id={self.id}), name={self.name}, description={self.description}, repo_link={self.repo_link.geturl() if self.repo_link else None})")
