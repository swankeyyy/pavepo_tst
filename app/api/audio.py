import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import os

# Initialize router
router = APIRouter()


@router.post("/upload")
async def upload_audio(
    name: str,
    file: UploadFile = File(...),
):
    # Check if the file is an audio file
    if not file.filename.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Create the directory if it doesn't exist
    os.makedirs("app/static/audio", exist_ok=True)

    # Generate a unique file name
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join("app/static/audio", filename)

    # Save file to the server
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    
