from datetime import date
import logging
from typing import Optional
from urllib.parse import urlparse, ParseResult
from shared.validator_enum import ValidatorEnum
from commands.log_project.lib.model.status import Status
from commands.log_project.lib.model.priority import Priority
from shared.validator import Validator
from shared.validator_date import ValidatorDate

logger = logging.getLogger(__name__)

class Project2:
    def __init__(
        self, id: int, name: str, description: str, repo_link: Optional[ParseResult] = None,
        status: Optional[Status] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
        #priority: Optional[Priority] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.repo_link = repo_link
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        
    @staticmethod
    def _parse_and_validate_data(id: int, name: str, description: str, repo_link: str, status: str, start_date: str, end_date: str) -> dict:
        if id < 0:
            raise ValueError("Project id must be greater than or equal to 0")
         
        data = {'id': id}

        if not name:
            raise ValueError("Project name cannot be None or empty")
        if not description:
            raise ValueError("Project description cannot be None or empty")
    
        data['name'] = Validator.validate_name(name.strip())
        data['description'] = Validator.validate_description(description.strip())

        if repo_link is not None:
            parsed_url = urlparse(repo_link.strip())
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError(f"Invalid repository link: {repo_link}")
            data['repo_link'] = parsed_url

        # Handling the 'status' field
        if status is not None:
            data['status'] = ValidatorEnum.validate_enum_by_class(status.strip(), Status)

        # Handle start_date and end_date based on their types
        if start_date is not None:
            if isinstance(start_date, str):
                data['start_date'] = ValidatorDate.validate_date(start_date.strip())
            elif isinstance(start_date, date):
                data['start_date'] = start_date  # Just keep the date if it's already a datetime.date object

        if end_date is not None:
            if isinstance(end_date, str):
                data['end_date'] = ValidatorDate.validate_date(end_date.strip())
            elif isinstance(end_date, date):
                data['end_date'] = end_date  # Just keep the date if it's already a datetime.date object

        # Ensure the start_date and end_date are valid and related
        if data.get('start_date') is not None and data.get('end_date') is not None:
            ValidatorDate.validate_relation(data['start_date'], data['end_date'])

        return data

    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project2':
        # Prepare data, converting strings to appropriate types if needed.
        parsed_data = cls._parse_and_validate_data(
            id=data['id'],
            name=data.get('name', None),
            description=data.get('description', None),
            repo_link=data.get('repo_link', None),
            status=data.get('status', None),
            start_date=data.get('start_date', None),
            end_date=data.get('end_date', None)
        )
        return cls(**parsed_data)

    
    def to_dict(self) -> dict:
        """
        Converts the Project object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'repo_link': self.repo_link.geturl() if self.repo_link else None,
            'status': self.status if self.status else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None    
        }
    
    def __repr__(self):
        return (f"Project(id={self.id}), name={self.name}, description={self.description}, repo_link={self.repo_link.geturl() if self.repo_link else None}, status={self.status}, start_date={self.start_date}, end_date={self.end_date})")
