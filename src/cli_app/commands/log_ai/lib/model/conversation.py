from pydantic import BaseModel, Field
from typing import List, Optional

class Conversation(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the conversation.")
    description: str = Field(..., max_length=255, description="Description of the conversation.")
    
    start_timestamp: Optional[str] = Field(None, description="Timestamp of when the conversation started.")
    last_mod_timestamp: Optional[str] = Field(None, description="Timestamp of the last modification.")
