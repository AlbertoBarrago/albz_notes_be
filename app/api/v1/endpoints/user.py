"""
   User Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.schemas.login import TokenResponse
from app.schemas.user import UserCreate, UserOut, UserUpdate, PasswordReset
from app.utils.audit.actions import log_action
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
    new_user = perform_action_user(db, "register_user", user=user)

    log_action(db,
               user_id=new_user['new_user'].user_id,
               action="Register",
               description="Registered user")

    return {"access_token": new_user['access_token'],
            "token_type": "bearer",
            "user": new_user['new_user']}


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    :param current_user:
    :return: UserOut
    """
    return current_user


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
    updated_user = perform_action_user(db, "update_user",
                                       user=user_update,
                                       current_user=current_user)

    log_action(db,
               user_id=current_user.user_id,
               action="Update",
               description="Updated user information")

    return updated_user


@router.post("/reset-password")
def reset_password(password_reset: PasswordReset,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """
    Reset user password
    :param password_reset:
    :param db:
    :param current_user:
    :return: Success message
    """
    perform_action_user(db, "reset_password",
                        current_user=current_user,
                        new_password=password_reset.new_password,
                        current_password=password_reset.current_password
                        )

    log_action(db,
               user_id=current_user.user_id,
               action="Reset Password",
               description="Password reset successfully")

    return {"message": "Password reset successfully"}


@router.delete("/delete")
def delete_user(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Delete user account
    :param db:
    :param current_user:
    :return: Success message
    """
    perform_action_user(db, "delete_user", current_user=current_user)

    log_action(db,
               user_id=current_user.user_id,
               action="Delete",
               description="Deleted user account")

    return {"message": "User deleted successfully"}
