"""
   User Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.schemas.login import TokenResponse, OauthRequest
from app.schemas.user import UserCreate, UserOut, UserUpdate, PasswordReset
from app.utils.oauth.google.actions import add_user_to_db
from app.utils.user.actions import perform_action_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register user
    :param user:
    :param db:
    :return: UserOut
    """
    return perform_action_user(db, "register_user", user=user)

@router.post("/register/google", response_model=TokenResponse)
def register_from_google(request: OauthRequest,
                 db: Session = Depends(get_db)):
    """
    Register from Google
    :param request:
    :param db:
    :return: Token
    """
    return add_user_to_db(db, request)


@router.post("/reset-password")
def reset_password(password_reset: PasswordReset,
                   db: Session = Depends(get_db)):
    """
    Reset user password
    :param password_reset:
    :param db:
    :return: Success message
    """

    return perform_action_user(db, "reset_password",
                               user_username=password_reset.username,
                               new_password=password_reset.new_password,
                               current_password=password_reset.current_password
                               )


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    """
    Get current user information
    :param current_user:
    :param db:
    :return: UserOut
    """
    return perform_action_user(db,
                               "me",
                               current_user=current_user)


@router.put("/update", response_model=UserOut)
def update_user(user_update: UserUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Update user information
    :param user_update:
    :param db:
    :param current_user:
    :return: UserOut
    """
    return perform_action_user(db, "update_user",
                               user=user_update,
                               current_user=current_user)


@router.delete("/delete")
def delete_user(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Delete user account
    :param db:
    :param current_user:
    :return: Success message
    """
    return perform_action_user(db,
                               "delete_user",
                               current_user=current_user)
