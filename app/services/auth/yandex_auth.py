import httpx
from fastapi import HTTPException, status

from src.settings import settings

async def get_yandex_user_info(access_token: str):
    """Retrieves user information from Yandex using the access token."""
    async with httpx.AsyncClient() as client:
        
        # Set the headers with the access token
        headers = {"Authorization": f"OAuth {access_token}"}
        response = await client.get(
            "https://login.yandex.ru/info",
            headers=headers,
            params={"format": "json"}
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Yandex access token"
            )
        
        return response.json()
    
    # If the response is not 200, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not get Yandex user info"
    )

async def get_yandex_access_token(code: str) -> str:
    """Get authorization code from Yandex OAuth callback URL and exchange it for an access token."""
    
    # Check if the code is provided
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET
        }
        
        response = await client.post(
            "https://oauth.yandex.ru/token",
            data=data
        )
        
        # Check if the response is successful
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not get Yandex access token"
            )
        
        #Return the access token from the response
        return response.json()["access_token"]
    
    # If the response is not 200, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not get Yandex access token"
    )