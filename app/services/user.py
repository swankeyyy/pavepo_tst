from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.auth.yandex_auth import get_yandex_access_token, get_yandex_user_info
from services.auth.auth import create_access_token
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
            user = User(
                email=email, name=user_info.get("first_name"), is_superuser=False
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        self.user = user
        return user

    async def create_access_token(
        self,
        code: str,
        session: AsyncSession,
        expires_delta=settings.ACCESS_TOKEN_EXPIRE,
    ) -> str:
        """
        Create an access token for the user.
        This function generates a JWT token for the user using their ID and email.
        """
        # Get the user ID and email
        user = await self.create_user_from_yandex(
            code=code,
            session=session,
        )

        # Create the token payload
        to_encode = {"user_id": str(user.id), "is_superuser": user.is_superuser}
        access_token = create_access_token(data=to_encode, expires_delta=expires_delta)

        # Return the access token
        return access_token

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

    async def update_user(
        self, user: User, update_data: dict, session: AsyncSession
    ) -> User:
        """
        Update user info.
        This function updates the user's information in the database.
        """

        # Get the user by ID
        user_id = user.get("user_id")
        stmt = select(User).where(User.id == user_id)
        user = await session.execute(stmt)
        user = user.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert update_data to a dictionary
        update_dict = update_data.dict(exclude_unset=True)

        # Update user info
        for key, value in update_dict.items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def delete_user(
        self, user_id: str, user: dict, session: AsyncSession
    ) -> None:
        """Delete user by ID, only for superuser."""

        # Check if the user is a superuser
        if not user.get("is_superuser"):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        # Get the user by ID
        stmt = select(User).where(User.id == user_id)
        user = await session.execute(stmt)
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        await session.delete(user)
        await session.commit()

        return {"detail": "User deleted successfully"}


# Initialize the UserService
user_service = UserService()
