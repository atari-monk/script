from pydantic import BaseModel, Field

class Dialog(BaseModel):
    dialog_id: str = Field(..., description="Unique identifier for the dialog entry.")
    message: str = Field(..., description="The message in the dialogue.")
    response: str = Field(..., description="The response to the message.")
