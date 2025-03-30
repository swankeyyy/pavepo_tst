from uuid import UUID

from .base import BaseSchema

class AudioCreateSchema(BaseSchema):
    """
    Schema for creating an audio file.
    """
    path: str
    name: str
    
class AudioReadSchema(BaseSchema):
    """Schema for list of audio files for currentuser"""
    id: UUID
    name: str
    path: str
    user_id: UUID