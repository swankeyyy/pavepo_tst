from fastapi import APIRouter, Depends, UploadFile, File, status


from sqlalchemy.ext.asyncio import AsyncSession

from schemas.audio import AudioCreateSchema, AudioReadSchema
from services.audio import audio_service
from src.db.db_config import db_config
from services.dependencies.user_dependency import get_user_dependency

# Initialize router
router = APIRouter()


@router.post(
    "/upload",
    summary="Upload an audio file and save it to the server, returning the file path",
    responses={
        status.HTTP_200_OK: {
            "description": "File uploaded successfully",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Unsupported file format"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    response_model=AudioCreateSchema,
)
async def upload_audio(
    name: str,
    user: dict = Depends(get_user_dependency),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_config.get_session),
):
    """
    Uploads an audio file and saves it to the server with a unique filename.

    - **file**: Audio file to upload (supported formats: .mp3, .wav, .ogg, .flac)
    - **returns**: JSON with saved file path
    """

    audio = await audio_service.saveaudio(
        user=user, file=file, name=name, session=session
    )
    return audio


@router.get(
    "/",
    response_model=list[AudioReadSchema],
    summary="Get all audios for current user by users token",
    responses={
        status.HTTP_200_OK: {"description": "success"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
    },
)
async def get_all_audios(
    user: dict = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_config.get_session),
):
    """Get all audios"""

    audios = await audio_service.get_audios(user=user, session=session)
    return audios
