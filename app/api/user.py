from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_config import db_config
from services.user import user_service
from schemas.user import UserReadSchema

# Init router
router = APIRouter()


@router.get(
    "/me",
    response_model=UserReadSchema,
    summary="Get curren user info by access token",
    responses={
        status.HTTP_200_OK: {
            "description": "User info retrieved successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Unsupported file format"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_user(
    user: dict = Depends(user_service.get_user_dependency),
    session: AsyncSession = Depends(db_config.get_session),
):
    """_summary_

    Args:
        user (dict, optional): _description_. Defaults to Depends(user_service.get_user_dependency).
        session (AsyncSession, optional): _description_. Defaults to Depends(db_config.get_session).

    Returns:
        _type_: _description_
    """
    user = await user_service.get_user(user=user, session=session)
    return user
