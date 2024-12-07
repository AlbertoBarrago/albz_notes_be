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
from app.db.models import Audit
from app.db.models.user.model import User
from app.dto.user.userDTO import UserDTO
from app.email.email_service import EmailService, EmailSchema
from app.repositories.audit.repository import log_audit_event
from app.repositories.logger.repository import LoggerService

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
        try:
            if user_id:
                return self.db.query(User).filter(User.user_id == user_id).first()
            return self.db.query(User).filter(
                or_(User.username == username,
                    User.email == username)).first()
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def _log_action(self, user_id, action, description):
        try:
            logger.info("User %s %s %s", user_id, action, description)
            log_audit_event(self.db, user_id=user_id, action=action, description=description)
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def _reset_password_with_token(self, token: str, new_password: str):
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

            return self.reset_password(
                user_username=payload,
                new_password=new_password
            )

        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not validate token, {e}"
            ) from e

    def _generate_user_token_and_return_user(self, current_user):
        """
        Generate user token and return user with refreshed token
        :param current_user: Current user object
        :return: User with new access token
        """
        try:
            user = self._get_user(user_id=current_user.user_id)
            if not user:
                UserErrorHandler.raise_user_not_found()

            self._log_action(current_user.user_id, "Refresh token", "Refresh token")

            return generate_user_token_and_return_user(user)
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    async def register_user(self, user):
        """
        Register new user
        """
        try:
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
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def reset_password(self, user_username, new_password):
        """
        Reset user password from Google
        :param user_username:
        :param new_password:
        :return: Success message
        """
        try:
            user = self._get_user(username=user_username)
            if not user:
                UserErrorHandler.raise_user_not_found()

            user.set_password(new_password)
            user.updated_at = datetime.now()
            self._log_action(user.user_id, "Reset Google Password", "Password reset successfully")
            self.db.commit()

            return {"user": UserDTO.from_model(user),
                    "message": "Password reset successfully"}
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def get_user(self, current_user):
        """
        Get user info by id
        :param current_user:
        :return: User
        """
        try:
            user = self._get_user(user_id=current_user.user_id)
            self._log_action(current_user.user_id, "Get user info", "Get user info")
            return UserDTO.from_model(user)
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def get_users(self, current_user):
        """
        Get users info by id
        :param current_user:
        :return: User
        """
        try:
            users = self.db.query(User).all()
            if current_user.role != "ADMIN":
                UserErrorHandler.raise_unauthorized_user_action()

            self._log_action(current_user.user_id, "Get users", "Get users")
            return [UserDTO.from_model(user) for user in users]
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def update_user(self, current_user, user_data):
        """
        Update user info
        :param current_user:
        :param user_data:
        :return: User
        """
        try:
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

            return {'user': UserDTO.from_model(user),
                    'message': "Updated user information"}
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])

    def delete_user(self, current_user):
        """
        Delete user
        :param current_user:
        :return: User
        """
        try:
            user = self._get_user(user_id=current_user.user_id)

            if user.user_id != current_user.user_id:
                UserErrorHandler.raise_unauthorized_user_action()

            self._log_action(current_user.user_id, "Delete",
                             f"Deleted his user account where username is {user.username}")

            if user:
                self.db.query(Audit).filter(Audit.user_id == user.user_id).delete()
                self.db.delete(user)
                self.db.commit()
                return {"message": "User deleted successfully"}

        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])
        return None

    async def perform_action_user(self, action: str, user=None, current_user=None, **kwargs):
        """
        Perform an action on a user
        :param action:
        :param user:
        :param current_user:
        :param kwargs:
        :return: Success message
        """
        try:
            actions = {
                "register_user": lambda: self.register_user(user),
                "reset_password": lambda: self._reset_password_with_token(
                    kwargs.get('token'),
                    kwargs.get('new_password')),
                "get_user": lambda: self.get_user(current_user),
                "get_users": lambda: self.get_users(current_user),
                "update_user": lambda: self.update_user(current_user, user),
                "delete_user": lambda: self.delete_user(current_user),
                "generate_user_token_and_return_user": lambda:
                self._generate_user_token_and_return_user(current_user)
            }

            return await actions[action]() if action == "register_user" else actions[action]()
        except Exception as e:
            self.db.rollback()
            raise UserErrorHandler.raise_server_error(e.args[0])
