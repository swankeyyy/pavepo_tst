from fastapi import APIRouter, Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_config import db_config
from services.user import user_service
from schemas.user import UserReadSchema, UserUpdateSchema
from services.dependencies.user_dependency import get_user_dependency

# Init router
router = APIRouter()


@router.get(
    "/me",
    response_model=UserReadSchema,
    summary="Get curren user info by access token",
    responses={
        status.HTTP_200_OK: {"description": "User info retrieved successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Unsupported file format"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_user(
    user: dict = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_config.get_session),
):
    """Get current user info by access token.
    """
    user = await user_service.get_user(user=user, session=session)
    return user


@router.patch("/me", response_model=UserReadSchema, responses={
    status.HTTP_200_OK: {"description": "User updated successfully"},
    status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
    status.HTTP_404_NOT_FOUND: {"description": "User not found"},
})
async def update_user(
    update_data: UserUpdateSchema,
    user: dict = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_config.get_session),
):
    """
        Update user info by access token.
    """
    user = await user_service.update_user(
        user=user, update_data=update_data, session=session
    )
    return user


@router.delete("/user_id")
async def delete_user(
    user_id: str,
    user: dict = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_config.get_session),
):
    """
        Delete user by access token.
    """
    await user_service.delete_user(user_id=user_id, user=user, session=session)
    return {"message": "User deleted successfully"}