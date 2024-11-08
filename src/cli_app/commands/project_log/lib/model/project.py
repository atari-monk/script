from pydantic import BaseModel, Field
from typing import Optional

class Project(BaseModel):
    """Data model for a project."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    id: Optional[int] = None
    