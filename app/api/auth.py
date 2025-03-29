from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse


from services.user import user_service
from src.settings import settings
from src.db.db_config import db_config
from sqlalchemy.ext.asyncio import AsyncSession

# Initialize router
router = APIRouter()

# OAuth2 scheme
auth_url = (
    f"https://oauth.yandex.ru/authorize?"
    f"response_type=code&"
    f"client_id={settings.YANDEX_CLIENT_ID}&"
    f"redirect_uri={settings.YANDEX_REDIRECT_URL}"
)


@router.get(
    "/yandex/url",
    summary="Get Yandex OAuth URL for authentication. If it not works at swagger need copy URL and paste to browser.",
    responses={
        status.HTTP_200_OK: {
            "description": "Yandex OAuth URL",
            "content": {"application/json": {"example": {"url": auth_url}}},
        },
    },
)
async def login_via_yandex():
    """
    Redirects to Yandex OAuth page for user authentication if it not works at swagger need copy URL and paste to browser.
    """
    # Redirect to Yandex OAuth page and returns code to the callback URL
    return RedirectResponse(auth_url)


@router.get(
    "/yandex/callback",
    summary="Get the code from Yandex OAuth callback URL and register the user in the system. If not works at swagger need copy code from URL",
    responses={
        status.HTTP_201_CREATED: {
            "description": "User successfully registered",
            "content": {"application/json": {"example": {"access_token": "string"}}},
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Missing code parameter in callback URL",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing code parameter in callback URL"}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid Yandex access token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid Yandex access token"}
                }
            },
        },
    },
)
async def yandex_callback(
    code: str, session: AsyncSession = Depends(db_config.get_session)
):
    """Get the code from Yandex OAuth callback URL and register the user in the system."""
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code parameter in callback URL",
        )

    try: 
        #Get token from service
        token = await user_service.create_access_token(code=code, session=session)
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Yandex access token",
        )
