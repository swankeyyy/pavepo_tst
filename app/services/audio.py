from sqlalchemy.ext.asyncio import AsyncSession

from .utils import get_filepath
from src.db.models import AudioFile

class AudioService:
    """
    Service class for handling audio file operations."""

    @staticmethod
    async def saveaudio(file, name: str, session: AsyncSession) -> AudioFile:
        # Save the file to disk and get the file path
        file_path = await get_filepath(file)
        
        # Save the filename and file path to the database
        audio = AudioFile(name=name, path=file_path)
        session.add(audio)
        await session.commit()
        await session.refresh(audio)
        
        # Return the saved audio object
        return audio
    
