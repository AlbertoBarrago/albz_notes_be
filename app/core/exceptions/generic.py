"""
Global error handler
"""
from fastapi import HTTPException
from starlette import status


class GlobalErrorHandler:
    """
    Handle global error
    """

    @classmethod
    def raise_mail_not_sent(cls: Exception):
        """
        Raise mail not sent error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send welcome email, but user was registered successfully",
            headers={"X-Error-Type": "email_failure"}
        )
