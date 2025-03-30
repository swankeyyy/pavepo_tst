from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt


from src.settings import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token. With optional expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=90)

    # Add time expiration to the token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGHORITHM
    )

    # Return the encoded JWT token
    return encoded_jwt

async def get_user_from_token(token: str):
    """Get user from token. Decode the JWT token and return the user data."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGHORITHM]
        )
        data = payload.copy()
        return data
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Token is invalid")
