from pydantic import BaseModel, Field

class Dialog(BaseModel):
    conversation_id: str = Field(..., description="The ID of the conversation this dialogue belongs to.")
    message: str = Field(..., description="The message in the dialogue.")
    response: str = Field(..., description="The response to the message.")
