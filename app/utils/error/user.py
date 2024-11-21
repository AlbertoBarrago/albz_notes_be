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

    @classmethod
    def raise_user_not_found(cls):
        """
        Raise user not found error
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    @classmethod
    def raise_password_not_match(cls):
        """
        Raise password not match error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
