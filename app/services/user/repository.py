"""
User actions
"""
from datetime import datetime

import jwt
from fastapi import HTTPException
from pydantic.v1 import EmailStr
from sqlalchemy import or_

from app.core.exceptions.user import UserErrorHandler
from app.core.security import generate_user_token_and_return_user, decode_access_token
from app.db.models.user.model import User
from app.email.email_service import EmailService, EmailSchema
from app.services.audit.repository import log_audit_event
from app.services.logger.repository import LoggerService

logger = LoggerService().logger


class UserManager:
    """
    User manager class
    """

    def __init__(self, db):
        self.db = db
        self.email_service = EmailService()

    def _get_user(self, user_id=None, username=None):
        """
        Get user from a database
        """
        if user_id:
            return self.db.query(User).filter(User.user_id == user_id).first()
        return self.db.query(User).filter(
            or_(User.username == username,
                User.email == username)).first()

    def _log_action(self, user_id, action, description):
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    @staticmethod
    def _user_to_dict(user):
        """
        Convert a user object to dictionary
        """
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "picture_url": user.picture_url if user.picture_url else None,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }

    async def register_user(self, user):
        """
        Register new user
        """
        user_fetched = self._get_user(username=user.username)
        if user_fetched:
            UserErrorHandler.raise_user_exists()

        new_user = User(username=user.username, email=user.email, role=user.role)
        new_user.set_password(user.password)

        email_schema = EmailSchema(
            username=new_user.username,
            email=[EmailStr(new_user.email)]
        )
        await self.email_service.welcome_email(email_schema)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        user_fetched = self._get_user(username=new_user.username)
        self._log_action(user_fetched.user_id, "Register", "Registered user")

        return generate_user_token_and_return_user(user_fetched)

    def reset_password(self, user_username, current_password, new_password):
        """
        Reset user password
        """
        user = self._get_user(username=user_username)
        if not user:
            UserErrorHandler.raise_user_not_found()
        if not user.verify_password(current_password):
            UserErrorHandler.raise_password_not_match()

        user.set_password(new_password)
        user.updated_at = datetime.now()
        self._log_action(user.user_id, "Reset Password", "Password reset successfully")
        self.db.commit()

        return {"message": "Password reset successfully", "user": self._user_to_dict(user)}

    def reset_google_password(self, user_username, new_password):
        """
        Reset user password from Google
        :param user_username:
        :param new_password:
        :return: Success message
        """
        user = self._get_user(username=user_username)
        if not user:
            UserErrorHandler.raise_user_not_found()

        user.set_password(new_password)
        user.updated_at = datetime.now()
        self._log_action(user.user_id, "Reset Google Password", "Password reset successfully")
        self.db.commit()

        return {"message": "Password reset successfully", "user": self._user_to_dict(user)}

    def get_user(self, current_user):
        """
        Get user info by id
        :param current_user:
        :return: User
        """
        user = self._get_user(user_id=current_user.user_id)

        self._log_action(current_user.user_id, "Get user info", "Get user info")
        return self._user_to_dict(user)

    def get_users(self, current_user):
        """
        Get users info by id
        :param current_user:
        :return: User
        """
        users = self.db.query(User).all()
        if current_user.role != "ADMIN":
            UserErrorHandler.raise_unauthorized_user_action()

        self._log_action(current_user.user_id, "Get users", "Get users")
        return [self._user_to_dict(user) for user in users]

    def update_user(self, current_user, user_data):
        """
        Update user info
        :param current_user:
        :param user_data:
        :return: User
        """
        user = self._get_user(user_id=current_user.user_id)

        if user.user_id != current_user.user_id:
            UserErrorHandler.raise_unauthorized_user_action()

        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email

        user.updated_at = datetime.now()
        self._log_action(current_user.user_id, "Update", "Updated user information")
        self.db.commit()
        self.db.refresh(user)

        return {"user": self._user_to_dict(user), "message": "User updated successfully"}

    def delete_user(self, current_user):
        """
        Delete user
        :param current_user:
        :return: User
        """
        user = self._get_user(user_id=current_user.user_id)

        if user.user_id != current_user.user_id:
            UserErrorHandler.raise_unauthorized_user_action()

        self._log_action(current_user.user_id, "Delete",
                         "Deleted his user account where username is {}".format(user.username))
        user_dict = self._user_to_dict(user)
        self.db.delete(user)
        self.db.commit()

        return {"message": "User deleted successfully", "user": user_dict}

    async def reset_google_password_with_token(self, token: str, new_password: str):
        """
        Reset password using Google token
        :param token: JWT token
        :param new_password: New password to set
        :return: a Success message with user info
        """
        try:
            payload = decode_access_token(token)
            if not payload:
                raise HTTPException(status_code=400, detail="Invalid or expired token")

            return self.reset_google_password(
                user_username=payload,
                new_password=new_password
            )
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not validate token, {e}"
            ) from e

    def generate_user_token_and_return_user(self, current_user):
        """
        Generate user token and return user with refreshed token
        :param current_user: Current user object
        :return: User with new access token
        """
        user = self._get_user(user_id=current_user.user_id)
        if not user:
            UserErrorHandler.raise_user_not_found()

        self._log_action(current_user.user_id, "Refresh token", "Refresh token")

        return generate_user_token_and_return_user(user)

    async def perform_action_user(self, action: str, user=None, current_user=None, **kwargs):
        """
        Perform an action on a user
        :param action:
        :param user:
        :param current_user:
        :param kwargs:
        :return: Success message
        """
        actions = {
            "register_user": lambda: self.register_user(user),
            "reset_password": lambda: self.reset_password(kwargs.get('user_username'),
                                                          kwargs.get('current_password'),
                                                          kwargs.get('new_password')),
            "reset_google_password": lambda: self.reset_google_password(kwargs.get('user_username'),
                                                                        kwargs.get('new_password')),
            "get_user": lambda: self.get_user(current_user),
            "get_users": lambda: self.get_users(current_user),
            "update_user": lambda: self.update_user(current_user, user),
            "delete_user": lambda: self.delete_user(current_user)
        }

        return await actions[action]() if action == "register_user" else actions[action]()