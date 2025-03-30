from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .audio import AudioFile


from .base import Base


class User(Base):
    """User model for the application with UUID, used in all models"""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    audios: Mapped[List["AudioFile"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="joined"
    )
