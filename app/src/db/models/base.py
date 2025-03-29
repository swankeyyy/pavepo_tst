from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

import uuid


# Base class for SQLAlchemy models with UUID, used in all models
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models with UUID"""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
