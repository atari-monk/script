from pydantic import BaseModel, Field

class Tag(BaseModel):
    tag_id: str = Field(..., description="Unique identifier for the tag.")
    name: str = Field(..., min_length=1, max_length=100, description="The name of the tag.")
