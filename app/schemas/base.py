from pydantic import BaseModel, ConfigDict


# Define a base schema class for all schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
