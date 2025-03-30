from uuid import UUID

from .base import BaseSchema


class UserReadSchema(BaseSchema):
    """Schema for reading user data."""

    id: UUID
    email: str
    name: str
    is_superuser: bool


class UserUpdateSchema(BaseSchema):
    """Schema for updating user data."""
    email: str | None = None
    name: str | None = None
    
