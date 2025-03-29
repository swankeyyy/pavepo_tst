from fastapi import APIRouter

from src.settings import settings
from .audio import router as audio_router
from .auth import router as auth_router

# Initialize router with prefix from db for including other routers
router = APIRouter(prefix=settings.API_PREFIX)

# Include the audio router
router.include_router(audio_router, prefix="/audio", tags=["audio"])

# Include the auth router
router.include_router(auth_router, prefix="/auth", tags=["auth"])