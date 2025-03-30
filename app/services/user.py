from fastapi import HTTPException, Header

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.auth.yandex_auth import get_yandex_access_token, get_yandex_user_info
from services.auth.auth import create_access_token, get_user_from_token
from src.db.models import User
from src.settings import settings

class UserService:
    
    async def create_user_from_yandex(self, code: str, session: AsyncSession) -> User:
        """
        Create a user from Yandex OAuth callback code.
        This function retrieves the access token from Yandex using the provided code,
        fetches the user information, and checks if the user already exists in the database.
        If the user does not exist, it creates a new user in the database.
        """
         # Get the access token from Yandex
        access_token = await get_yandex_access_token(code)

        # Get user info from Yandex using the access token
        user_info = await get_yandex_user_info(access_token)
        
        # Check if the user already exists in the database or not by email
        email = user_info.get("default_email")
        stmt = select(User).where(User.email == email)
        user = await session.execute(stmt)
        user = user.scalars().first()
        
        if not user:
            user = User(email=email, name=user_info.get("first_name"), is_superuser=False)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        self.user = user
        return user
    
    
    async def create_access_token(self, code: str, session: AsyncSession, expires_delta=settings.ACCESS_TOKEN_EXPIRE) -> str:
        """
        Create an access token for the user.
        This function generates a JWT token for the user using their ID and email.
        """
        # Get the user ID and email
        user = await self.create_user_from_yandex(code=code, session=session,)
        
        # Create the token payload
        to_encode = {"user_id": str(user.id), "is_superuser": str(user.is_superuser)}
        access_token = create_access_token(
            data=to_encode, expires_delta=expires_delta
        )
        
        # Return the access token
        return access_token        
        
    async def get_user_dependency(self, token: str = Header(alias="access_token")) -> dict:
        """
        This function is a placeholder for the actual implementation of getting the current user.
        In a real application, this would typically involve decoding a JWT token.
        """
    
        # Decode the token and get user data
        user = await get_user_from_token(token)
        
        return user
    
    async def get_user(self, user: dict, session: AsyncSession) -> User:
        """
        Get user by ID.
        This function retrieves a user from the database using their ID.
        """
        # Get the user by ID
        user_id = user.get("user_id")
        stmt = select(User).where(User.id == user_id)
        user = await session.execute(stmt)
        user = user.scalars().first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    
# Initialize the UserService
user_service = UserService()