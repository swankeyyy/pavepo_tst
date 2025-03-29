from pydantic import BaseModel, ConfigDict


# Define a base schema class for all schemas
class BaseSchema(BaseModel):
    """Base schema class for all schemas."""
    model_config = ConfigDict(from_attributes=True)
