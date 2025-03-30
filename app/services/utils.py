from fastapi import status
import os
import uuid
from fastapi import HTTPException

from src.settings import settings

# Directory to save uploaded files
DIR = settings.STATIC_DIR


async def get_filepath(user_id: str, file) -> str | None:
    # Check if the file is an audio file
    if not file.filename.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format"
        )
    # Make upload dir for current user
    UPLOAD_DIR = DIR + user_id + "/"
    # Create the directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a unique file name
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file to the server
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            return file_path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )
