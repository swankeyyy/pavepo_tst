from fastapi import Header

from services.auth.auth import get_user_from_token



async def get_user_dependency(
        token: str = Header(alias="access_token")
    ) -> dict:
        """
        This function is a placeholder for the actual implementation of getting the current user.
        In a real application, this would typically involve decoding a JWT token.
        """

        # Decode the token and get user data
        user = await get_user_from_token(token)

        return user