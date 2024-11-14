"""
User actions
"""
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_
from starlette import status

from app.core.access_token import generate_user_token
from app.db.models.users import User


def user_to_dict(user):
    """Convert User object to dictionary"""
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }


def perform_action_user(db,
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
    match action:
        case "register_user":
            user_fetched = db.query(User).filter(User.username == user.username).first()
            if user_fetched:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )

            new_user = User(username=user.username,
                            email=user.email)
            new_user.set_password(user.password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_fetched = db.query(User).filter(User.username == new_user.username).first()
            return generate_user_token(user_fetched)

        case "get_user":
            user_obj = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_obj:
                raise HTTPException(status_code=404, detail="User not found")
            return user_to_dict(user_obj)

        case "get_users":
            users = db.query(User).all()
            return [user_to_dict(user) for user in users]

        case "update_user":
            user_obj = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_obj:
                raise HTTPException(status_code=404, detail="User not found")

            if user_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this user")

            if user.username:
                user_obj.username = user.username
            if user.email:
                user_obj.email = user.email

            user_obj.updated_at = datetime.now()
            db.commit()
            db.refresh(user_obj)
            return user_to_dict(user_obj)

        case "delete_user":
            user_obj = db.query(User).filter(User.user_id == current_user.user_id).first()
            if not user_obj:
                raise HTTPException(status_code=404, detail="User not found")

            if user_obj.user_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this user")

            db.delete(user_obj)
            db.commit()
            return {"message": "User deleted successfully"}

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
            db.commit()
            return {"message": "Password reset successfully", "user": user_to_dict(user_fetched)}
