from pydantic.v1 import EmailStr

from app.core import generate_user_token
from app.core.exceptions.auth import AuthErrorHandler
from app.core.exceptions.generic import GlobalErrorHandler
from app.db.models import User
from app.email.email_service import EmailService, EmailSchema
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

logger = LoggerService().logger


class ResetManager:
    """
    Session manager
    """

    def __init__(self, db):
        self.db = db

    def _get_user(self, username):
        """
        Get user from database
        :param username:
        :return: User object
        """
        return (self.db.query(User)
                .filter((User.username == username) |
                        (User.email == username))
                .first())

    def _log_action(self, user_id, action, description):
        """
        Log action
        :param user_id:
        :param action:
        :param description:
        """
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    def send_password_reset_email(self, username, background_tasks):
        """
        Send password reset email
        :param username:
        :param background_tasks:
        :return:
        """
        user = self._get_user(username)
        if not user:
            AuthErrorHandler.raise_user_not_found()
            return

        token = generate_user_token(user)

        log_audit_event(self.db,
                        user_id=user.user_id,
                        action="Password Reset",
                        description="Password reset requested")

        try:
            email_service = EmailService()
            email_schema = EmailSchema(
                username=user.username,
                email=[EmailStr(user.email)],
            )
            background_tasks.add_task(
                email_service.send_password_setup_email,
                email_schema,
                user.user_id
            )

            result = {
                "access_token": token,
                "token_type": "bearer",
                "username": user.username,
                "user": user
            }

            return result

        except (ConnectionError, TimeoutError):
            GlobalErrorHandler.raise_mail_reset_not_sent()
