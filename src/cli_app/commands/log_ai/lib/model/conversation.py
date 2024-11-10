from pydantic import BaseModel, Field
from typing import List

class Conversation(BaseModel):
    conversation_id: str = Field(..., description="Unique identifier for the conversation.")
    project_id: str = Field(..., description="ID of the project associated with the conversation.")
    tags_id: str = Field(..., description="ID of the tag associated with the conversation.")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the conversation.")
    description: str = Field(..., max_length=255, description="Description of the conversation.")
    start_timestamp: str = Field(..., description="Timestamp of when the conversation started.")
    last_mod_timestamp: str = Field(..., description="Timestamp of the last modification.")
    dialogues: List[dict] = Field([], description="List of dialogues in the conversation.")
