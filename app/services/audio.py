from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import get_filepath
from src.db.models import AudioFile


class AudioService:
    """
    Service class for handling audio file operations."""

    async def saveaudio(
        self, user: dict, file, name: str, session: AsyncSession
    ) -> AudioFile:
        """Save auidofile with current user id"""

        # Get user_id
        user_id = user.get("user_id")

        # Save the file to disk and get the file path
        file_path = await get_filepath(user_id=user_id, file=file)

        # Save the filename and file path to the database
        audio = AudioFile(name=name, path=file_path, user_id=user_id)
        session.add(audio)
        await session.commit()
        await session.refresh(audio)

        # Return the saved audio object
        return audio

    async def get_audios(self, user: dict, session: AsyncSession) -> list:
        """Get list of all audios for current user"""

        # Get user_id from user
        user_id = user.get("user_id")

        # Get all audios by user_id
        stmt = select(AudioFile).where(AudioFile.user_id == user_id)
        audios = await session.scalars(stmt)
        if audios:
            return list(audios)

        # If not audios
        return []


# Initialize the audio service
audio_service = AudioService()
