"""
 Email Service
"""
from typing import List

from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.settings import settings


class EmailService:
    """
       Initialize FastMail
       :return: None
    """
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=587,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True
        )
        self.fastmail = FastMail(self.conf)

    async def welcome_email(self, email: str, username: str):
        """Send welcome email"""
        body = f"""
        Hi {username},
        Welcome to Notes App! We're excited to have you on board.
        Best regards,
        Notes App Team
        """
        message = MessageSchema(
            subject="Welcome to Notes App",
            recipients=List[EmailStr]([email]),
            body=body,
            subtype=MessageType.html
        )
        await self.fastmail.send_message(message)

    async def send_password_setup_email(self, email: str, username: str, token: str):
        """Send password setup email for OAuth users"""
        body = f"""
        Hi {username},

        Welcome to Notes App! Since you registered using Google OAuth, 
        please set up your password for full account access.

        Click here to set your password: {settings.FRONTEND_URL}/set-password?token={token}

        This link will expire in 24 hours.

        Best regards,
        Notes App Team
        """

        message = MessageSchema(
            subject="Welcome to Notes App - Set Your Password",
            recipients=List[EmailStr]([email]),
            body=body,
            subtype=MessageType.html
        )

        await self.fastmail.send_message(message)
