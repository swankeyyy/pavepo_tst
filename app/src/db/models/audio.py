from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from .user import User
from .base import Base


# AudioFile model with user relationship
class AudioFile(Base):
    """Audio file model"""

    __tablename__ = "audio_files"

    name: Mapped[str] = mapped_column(String, index=True)
    path: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="audios")

    def __str__(self):
        return f"AudioFile {self.name} ({self.path})"

    def __repr__(self):
        return f"AudioFile {self.name} ({self.path})"
