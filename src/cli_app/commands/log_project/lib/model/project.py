from typing import List, Optional, Literal
from datetime import date

class Project:
    def __init__(
        self,
        name: str,
        description: str,
        repo_link: Optional[str] = None,
        status: Optional[Literal['Not Started', 'In Progress', 'Completed', 'On Hold']] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        priority: Optional[Literal['Low', 'Medium', 'High']] = None,
        technologies: List[str] = None,
        milestones: List[str] = None,
        current_tasks: List[str] = None,
        last_updated: Optional[date] = None,
    ):
        self.start_date = start_date
        self.end_date = self._validate_dates(end_date, start_date)
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.repo_link = repo_link
        self.status = status
        self.priority = priority
        self.technologies = technologies or []
        self.milestones = milestones or []
        self.current_tasks = current_tasks or []
        self.last_updated = last_updated
    
    def _validate_name(self, value: str) -> str:
        value = value.strip()
        if not all(c.isalnum() or c.isspace() or c in "-_" for c in value):
            raise ValueError("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
        return value
    
    def _validate_description(self, value: str) -> str:
        value = value.strip()
        if len(value.split()) < 5:
            raise ValueError("Description should contain at least 5 words.")
        return value
    
    def _validate_dates(self, end_date: Optional[date], start_date: Optional[date]) -> Optional[date]:
        if start_date and end_date and end_date < start_date:
            raise ValueError("End date must be after the start date.")
        return end_date
    
    def __repr__(self):
        return f"Project(name={self.name}, description={self.description}, start_date={self.start_date}, end_date={self.end_date}, status={self.status})"
