"""
 Auth Error Handler
"""
from fastapi import HTTPException, status


class AuthErrorHandler:
    """
    Auth Error Handler
    """
    @staticmethod
    def raise_invalid_credentials():
        """
        Raise invalid credentials error
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def raise_unauthorized():
        """
        Raise unauthorized error
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def raise_invalid_grant():
        """
        Raise invalid grant error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type"
        )

    @classmethod
    def raise_invalid_grant_type(cls):
        """
        Raise invalid grant type error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type"
        )

    @classmethod
    def raise_existing_user_error(cls):
        """
        Raise existing user error
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists, Try to login"
        )

    @classmethod
    def raise_invalid_token(cls):
        """
        Raise invalid token error
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    @classmethod
    def raise_user_not_found(cls):
        """
        Raise user not found error
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found, Try to register",
            headers={"WWW-Authenticate": "Bearer"}
        )
