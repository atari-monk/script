from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Optional
from datetime import date
from typing import Literal

class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the project.")
    description: str = Field(..., max_length=255, description="A brief description of the project.")
    
    # Optional fields for updates (default to empty list)
    repo_link: Optional[HttpUrl] = Field(None, description="The repository URL for the project.")
    status: Optional[Literal['Not Started', 'In Progress', 'Completed', 'On Hold']] = Field(None, description="Current status of the project.")
    start_date: Optional[date] = Field(None, description="The date when the project started.")
    end_date: Optional[date] = Field(None, description="The planned or actual end date of the project.")
    priority: Optional[Literal['Low', 'Medium', 'High']] = Field(None, description="The priority level of the project.")
    technologies: Optional[List[str]] = Field([], description="List of technologies used in the project.")
    milestones: Optional[List[str]] = Field([], description="Key milestones or goals for the project.")
    current_tasks: Optional[List[str]] = Field([], description="List of active tasks or issues related to the project.")
    last_updated: Optional[date] = Field(None, description="The date when the project was last updated.")
    
    # Custom Validators
    @staticmethod
    def _contains_only_valid_characters(value: str) -> bool:
        return all(c.isalnum() or c.isspace() or c in "-_" for c in value)

    @field_validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if not cls._contains_only_valid_characters(value):
            raise ValueError("Project name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
        return value

    @field_validator('description')
    def validate_description(cls, value):
        value = value.strip()
        if len(value.split()) < 5:
            raise ValueError("Description should contain at least 5 words.")
        return value

    @field_validator('end_date')
    def validate_dates(cls, value, values):
        start_date = values.start_date if hasattr(values, 'start_date') else None  # Access directly
        if start_date and value and value < start_date:
            raise ValueError("End date must be after the start date.")
        return value
