"""
User actions
"""
from datetime import datetime

from fastapi import HTTPException
from pydantic.v1 import EmailStr
from sqlalchemy import or_
from starlette import status

from app.core.access_token import generate_user_token_and_return_user
from app.db.models.users import User
from app.utils.audit.actions import logger
from app.email.email_service import EmailService, EmailSchema


def user_to_dict(user):
    """Convert User object to dictionary"""
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "picture": user.picture_url if user.picture_url else None,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }


async def perform_action_user(db,
                              action: str,
                              user=None,
                              current_user=None,
                              **kwargs):
    """
    Perform database actions for users
    :param db: Database connection
    :param action: Action to perform
    :param user: User object
    :param current_user: Current authenticated user
    :return: JSON list of users or single user
    """
    result = None

    match action:
        case "register_user":
            user_fetched = db.query(User).filter(User.username == user.username).first()
            if user_fetched:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )

            new_user = User(username=user.username,
                            email=user.email,
                            role=user.role)
            new_user.set_password(user.password)

            email_service = EmailService()
            email_schema = EmailSchema(
                username=new_user.username,
                email=[EmailStr(new_user.email)]
            )

            await email_service.welcome_email(email_schema)

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_fetched = db.query(User).filter(User.username == new_user.username).first()

            logger(db,
                   user_id=user_fetched.user_id,
                   action="Register",
                   description="Registered user")

            result = generate_user_token_and_return_user(user_fetched)
        case "reset_password":
            user_fetched = (db.query(User)
                            .filter(or_(
                User.username == kwargs.get('user_username'),
                User.email == kwargs.get('user_username')
            ))
                            .first())
            if not user_fetched:
                raise HTTPException(status_code=404, detail="User not found")

            if not user_fetched.verify_password(kwargs.get('current_password')):
                raise HTTPException(status_code=400, detail="Incorrect current password")

            user_fetched.set_password(kwargs.get('new_password'))
            user_fetched.updated_at = datetime.now()

            logger(db,
                   user_id=user_fetched.user_id,
                   action="Reset Password",
                   description="Password reset successfully")
            db.commit()
            result = {"message": "Password reset successfully", "user": user_to_dict(user_fetched)}
        case "reset_google_password":
            user_fetched = (db.query(User)
                            .filter(or_(
                User.username == kwargs.get('user_username')))
                            .first())

            if not user_fetched:
                raise HTTPException(status_code=404, detail="User not found")

            user_fetched.set_password(kwargs.get('new_password'))
            user_fetched.updated_at = datetime.now()

            logger(db,
                   user_id=user_fetched.user_id,
                   action="Reset Google Password",
                   description="Password reset successfully")
            db.commit()
            result = {"message": "Password reset successfully", "user": user_to_dict(user_fetched)}
        case "me":
            logger(db,
                   action="Get current user info",
                   user_id=current_user.user_id,
                   description="Get current user info")

            result = user_to_dict(current_user)
        case "get_user":
            user_fetched = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_fetched:
                raise HTTPException(status_code=404, detail="User not found")

            logger(db,
                   action="Get user info",
                   user_id=current_user.user_id,
                   description="Get user info")

            result = user_to_dict(user_fetched)
        case "get_users":
            users = db.query(User).all()
            if not users:
                raise HTTPException(status_code=404, detail="No users found")
            logger(db,
                   action="Get users",
                   user_id=current_user.user_id,
                   description="Get users")

            result = {"users": user_to_dict(user) for user in users}
        case "update_user":
            user_fetched = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_fetched:
                raise HTTPException(status_code=404, detail="User not found")

            if user_fetched.user_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this user")

            if user.username:
                user_fetched.username = user.username
            if user.email:
                user_fetched.email = user.email

            user_fetched.updated_at = datetime.now()

            logger(db,
                   user_id=current_user.user_id,
                   action="Update",
                   description="Updated user information")

            db.commit()
            db.refresh(user_fetched)

            result = {"user": user_to_dict(user_fetched),
                      "message": "Password reset successfully"}
        case "delete_user":
            user_fetched = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_fetched:
                raise HTTPException(status_code=404, detail="User not found")

            if user_fetched.user_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this user")

            logger(db,
                   user_id=current_user.user_id,
                   action="Delete",
                   description="Deleted user account")

            db.delete(user_fetched)
            db.commit()
            result = {"message": "User deleted successfully",
                      "user": user_to_dict(user_fetched)}

    return result
