from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import date
from typing import List, Optional

class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the project.")
    description: str = Field(..., max_length=255, description="A brief description of the project.")
    
    # Optional fields for updates (default to None or empty list)
    repo_link: Optional[HttpUrl] = Field(None, description="The repository URL for the project, e.g., 'https://github.com/atari-monk/script'.")
    status: Optional[str] = Field(None, description="Current status of the project (e.g., 'In Progress', 'Completed', 'On Hold').")
    start_date: Optional[date] = Field(None, description="The date when the project started.")
    end_date: Optional[date] = Field(None, description="The planned or actual end date of the project.")
    priority: Optional[str] = Field(None, description="The priority level of the project (e.g., 'Low', 'Medium', 'High').")
    technologies: Optional[List[str]] = Field(None, description="List of technologies used in the project.")
    milestones: Optional[List[str]] = Field(None, description="Key milestones or goals for the project.")
    current_tasks: Optional[List[str]] = Field(None, description="List of active tasks or issues related to the project.")
    last_updated: Optional[date] = Field(None, description="The date when the project was last updated.")
    
    # Custom Validators
    @staticmethod
    def _contains_only_valid_characters(value: str) -> bool:
        return all(c.isalnum() or c.isspace() for c in value)

    @field_validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if not cls._contains_only_valid_characters(value):
            raise ValueError("Project name must contain only alphanumeric characters and spaces.")
        return value

    @field_validator('description')
    def validate_description(cls, value):
        return value.strip()
