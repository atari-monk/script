from pydantic import BaseModel, Field

class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the project.")
    description: str = Field(..., max_length=255, description="A brief description of the project.")

    # Custom validators
    @staticmethod
    def _contains_only_valid_characters(value: str) -> bool:
        return all(c.isalnum() or c.isspace() for c in value)

    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not cls._contains_only_valid_characters(value):
            raise ValueError("Project name must contain only alphanumeric characters and spaces.")
        return value

    @classmethod
    def validate_description(cls, value):
        return value.strip()
    