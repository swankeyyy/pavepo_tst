from uuid import UUID

from .base import BaseSchema

# Initializing the UserSchema class
class UserSchema(BaseSchema):
    """Base schema for user data."""
    id: UUID
    
class UserReadSchema(UserSchema):
    """Schema for reading user data."""
    email: str
    name: str
    is_superuser: bool
