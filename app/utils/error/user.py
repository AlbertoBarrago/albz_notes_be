"""
    UserErrorHandler
"""
from fastapi import HTTPException
from starlette import status

class UserErrorHandler:
    """
    UserErrorHandler
    """
    @classmethod
    def raise_user_exists(cls):
        """
        Raise user exists error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    @classmethod
    def raise_invalid_password(cls):
        """
        Raise invalid password error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    @classmethod
    def raise_unauthorized_user_action(cls):
        """
        Raise unauthorized user action error
        """
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
