"""
    This module contains the functions for sending emails to users.
"""
from pydantic.v1 import EmailStr

from app.email.email_service import EmailService, EmailSchema


class CommonService:
    """
    This class contains the functions for sending emails to users.
    """

    def __init__(self):
        self.email_service = EmailService()

    def send_email(self, background_tasks, token, user):
        """
        Sends a password setup email to a user using the provided email service,
        schema, and token in a background task.

        Parameters:
            background_tasks: The background tasks queue that will schedule the
                email sending a task.
            token: The unique token used for user email verification.
            user: The user object containing username and email information.

        """
        email_schema = EmailSchema(
            username=user.username,
            email=[EmailStr(user.email)],
        )
        background_tasks.add_task(
            self.email_service.send_password_setup_email,
            email_schema,
            token
        )
