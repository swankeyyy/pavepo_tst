from uuid import UUID

from .base import BaseSchema

class AudioCreateSchema(BaseSchema):
    """
    Schema for creating an audio file.
    """
    id: UUID
    path: str
    name: str