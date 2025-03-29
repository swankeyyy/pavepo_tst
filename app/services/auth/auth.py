from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


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



