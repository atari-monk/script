from datetime import datetime
from typing import Optional

class Task:
    allowed_statuses = ['pending', 'in progress', 'completed']
    allowed_priorities = ['low', 'medium', 'high']

    def __init__(
        self,
        project_id: int,
        title: str,
        status: str = 'pending',
        description: Optional[str] = None,
        priority: str = 'medium',
        due_date: Optional[datetime] = None,
        created_at: datetime = None
    ):
        self.project_id = project_id
        self.title = self._validate_title(title)
        self.status = self._validate_status(status)
        self.description = self._validate_description(description)
        self.priority = self._validate_priority(priority)
        self.due_date = self._validate_due_date(due_date)
        self.created_at = created_at or datetime.now()

    def _validate_title(self, title: str) -> str:
        if not (1 <= len(title) <= 100):
            raise ValueError("Title must be between 1 and 100 characters.")
        return title

    def _validate_status(self, status: str) -> str:
        if status not in self.allowed_statuses:
            raise ValueError(f"Status must be one of {self.allowed_statuses}")
        return status

    def _validate_description(self, description: Optional[str]) -> Optional[str]:
        if description and len(description) > 255:
            raise ValueError("Description must be 255 characters or fewer.")
        return description

    def _validate_priority(self, priority: str) -> str:
        if priority not in self.allowed_priorities:
            raise ValueError(f"Priority must be one of {self.allowed_priorities}")
        return priority

    def _validate_due_date(self, due_date: Optional[datetime]) -> Optional[datetime]:
        if due_date and due_date < datetime.now():
            raise ValueError("Due date must be in the future.")
        return due_date

    def __repr__(self):
        return (f"Task(project_id={self.project_id}, title={self.title}, status={self.status}, "
                f"priority={self.priority}, due_date={self.due_date}, created_at={self.created_at})")

    def to_dict(self) -> dict:
        """Converts the Task object to a dictionary, with datetime objects converted to ISO format."""
        return {
            'project_id': self.project_id,
            'title': self.title,
            'status': self.status,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Creates a Task instance from a dictionary."""
        data['due_date'] = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        data['created_at'] = datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now()
        return cls(**data)
    