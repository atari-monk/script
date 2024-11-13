import logging
from typing import List, Optional, Literal
from datetime import date, datetime

logger = logging.getLogger(__name__)

class Project:
    STATUS_CHOICES = ['Not Started', 'In Progress', 'Completed', 'On Hold']
    PRIORITY_CHOICES = ['Low', 'Medium', 'High']

    def __init__(
        self,
        name: str,
        description: str,
        repo_link: Optional[str] = None,
        status: Optional[Literal['Not Started', 'In Progress', 'Completed', 'On Hold']] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        priority: Optional[Literal['Low', 'Medium', 'High']] = None,
        technologies: Optional[List[str]] = None,
        milestones: Optional[List[str]] = None,
        current_tasks: Optional[List[str]] = None,
        last_updated: Optional[date] = None,
        id: Optional[int] = None
    ):
        # Validate dates first for tests to pass
        self.start_date = self._validate_start_date(start_date)
        self.end_date = self._validate_end_date(end_date, self.start_date)
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.repo_link = repo_link
        self.status = status
        self.priority = priority
        self.technologies = technologies or []
        self.milestones = milestones or []
        self.current_tasks = current_tasks or []
        self.last_updated = last_updated or date.today()
        self.id = id
    
    @staticmethod
    def parse_add(name: str) -> dict:
        #converts cli input to dict for add command  
        
        return { 'name': name.strip(), }

    def _validate_name(self, name: str) -> str:
        if not 3 <= len(name) <= 50:
            raise ValueError("Project name must be between 3 and 50 characters.")
        if not all(c.isalnum() or c.isspace() or c in "-_" for c in name.strip()):
            raise ValueError("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
        return name.strip()
    
    def _validate_description(self, description: str) -> str:
        if len(description.split()) < 1:
            raise ValueError("Description should contain at least 1 word.")
        if len(description) < 10:  # Minimum length of description
            raise ValueError("Description should be at least 10 characters long.")
        return description.strip()

    def _validate_start_date(self, start_date: Optional[date]) -> Optional[date]:
        if start_date and not isinstance(start_date, date):
            raise ValueError("Start date must be a valid date.")
        return start_date
    
    def _validate_end_date(self, end_date: Optional[date], start_date: Optional[date]) -> Optional[date]:
        if end_date and not isinstance(end_date, date):
            raise ValueError("End date must be a valid date.")
        if start_date and end_date and end_date < start_date:
            raise ValueError("End date must be after the start date.")
        return end_date
    
    @staticmethod
    def parse_date(date_str: str) -> Optional[date]:
        try:
            return datetime.fromisoformat(date_str).date()
        except ValueError:
            logger.error(f"Invalid date format: {date_str}")
            return None
        
    @staticmethod
    def parse_comma_separated_list(input_str: str) -> List[str]:
        if input_str:
            items = [item.strip() for item in input_str.split(",")]
            if any(not item for item in items):
                raise ValueError("Comma-separated list contains empty values.")
            return items
        return []
    
    @staticmethod
    def parse_fields(field: str, value: str) -> any:
        if field == "technologies" or field == "milestones" or field == "current_tasks":
            return Project.parse_comma_separated_list(value)
        elif field == "status":
            return value if value in Project.STATUS_CHOICES else None
        elif field == "priority":
            return value if value in Project.PRIORITY_CHOICES else None
        return value
    
    def __repr__(self):
        return (f"Project(name={self.name}, description={self.description}, repo_link={self.repo_link}, "
            f"status={self.status}, start_date={self.start_date}, end_date={self.end_date}, "
            f"priority={self.priority}, technologies={self.technologies}, milestones={self.milestones}, "
            f"current_tasks={self.current_tasks}, last_updated={self.last_updated}, id={self.id})")

    def to_dict(self) -> dict:
        """
        Converts the Project object to a dictionary, with dates formatted in ISO format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'repo_link': self.repo_link,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'priority': self.priority,
            'technologies': self.technologies,
            'milestones': self.milestones,
            'current_tasks': self.current_tasks,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        # Assumes `data` contains all keys that match the __init__ parameters of `Project` with compatible value types.
        return cls(**data)
