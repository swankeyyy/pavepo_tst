from fastapi import APIRouter

from src.settings import settings
from .audio import router as audio_router
from .auth import router as auth_router
from .user import router as users_router

# Initialize router with prefix from db for including other routers
router = APIRouter(prefix=settings.API_PREFIX)

# Include other routers
router.include_router(audio_router, prefix="/audio", tags=["audio"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])