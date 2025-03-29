from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


# AudioFile model with owner relationship
class AudioFile(Base):
    """Audio file model"""

    __tablename__ = "audio_files"

    name: Mapped[str] = mapped_column(String, index=True)
    path: Mapped[str]

    def __str__(self):
        return f"AudioFile {self.name} ({self.path})"

    def __repr__(self):
        return f"AudioFile {self.name} ({self.path})"
