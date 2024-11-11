from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    project_id: int = Field(..., description="The ID of the project this task is associated with.")
    title: str = Field(..., min_length=1, max_length=100, description="The title of the task.")
    status: str = Field('pending', description="Status of the task (e.g., pending, in progress, completed)")

    # Optional fields listed below
    description: Optional[str] = Field(None, max_length=255, description="A brief description of the task.")
    priority: Optional[str] = Field('medium', description="Priority of the task (e.g., low, medium, high).")
    due_date: Optional[datetime] = Field(None, description="The due date for the task.")
    created_at: datetime = Field(default_factory=datetime.now, description="The date and time when the task was created.")

    # Validate status to ensure it's one of the allowed values
    @field_validator('status')
    def validate_status(cls, value):
        allowed_statuses = ['pending', 'in progress', 'completed']
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return value

    # Validate priority to ensure it's one of the allowed values
    @field_validator('priority')
    def validate_priority(cls, value):
        allowed_priorities = ['low', 'medium', 'high']
        if value not in allowed_priorities:
            raise ValueError(f"Priority must be one of {allowed_priorities}")
        return value

    # Optional: You could also validate the `due_date` if you want it to always be in the future.
    @field_validator('due_date')
    def validate_due_date(cls, value):
        if value and value < datetime.now():
            raise ValueError("Due date must be in the future.")
        return value
