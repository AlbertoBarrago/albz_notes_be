"""
   User Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.access_token import decode_access_token
from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.schemas.login import TokenResponse
from app.schemas.user import UserOut, UserRequestAdd, PasswordReset, GoogleResetRequest
from app.utils.user.actions import UserManager

router = APIRouter()


@router.post("/register",
             response_model=TokenResponse,
             responses={
                 400: {
                     "description": "Username already registered",
                     "content": {
                         "application/json": {
                             "example": {
                                 "status_code": 400,
                                 "detail": "Username already registered"
                             }
                         }
                     }
                 }
             }
             )
async def register_user(user: UserRequestAdd, db: Session = Depends(get_db)):
    """
    Register user
    :param user:
    :param db:
    :return: UserOut
    """
    return await UserManager(db).perform_action_user("register_user", user=user)


@router.post("/reset/password", responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "status_code": 404
                    }
                }
            }
        },
        400: {
            "description": "Invalid password",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect current password",
                        "status_code": 400
                    }
                }
            }
        }
    })
async def reset_password(password_reset: PasswordReset,
                         db: Session = Depends(get_db)):
    """
    Reset user password
    :param password_reset:
    :param db:
    :return: Success message
    """

    return await (UserManager(db)
                  .perform_action_user("reset_password",
                                       user_username=password_reset.username,
                                       new_password=password_reset.new_password,
                                       current_password=password_reset.current_password))


@router.post("/reset/google-password", responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "status_code": 404
                    }
                }
            }
        },
        400: {
            "description": "Invalid password",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect current password",
                        "status_code": 400
                    }
                }
            }
        }
    })
async def reset_google_password(google_req: GoogleResetRequest,
                                db: Session = Depends(get_db)):
    """
    Reset user password
    :param google_req:
    :param db:
    :return: Success message
    """

    payload = decode_access_token(google_req.token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return await UserManager(db).perform_action_user(
        "reset_google_password",
        user_username=payload,
        new_password=google_req.new_password)


@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    """
    Get current user information
    :param current_user:
    :param db:
    :return: UserOut
    """
    return await UserManager(db).perform_action_user(
        "me",
        current_user=current_user)


@router.put("/update",
            response_model=UserOut,
            responses={
                404: {
                    "description": "User not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "User not found",
                                "status_code": 404
                            }
                        }
                    }
                },
                403: {
                    "description": "Not authorized",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Not authorized to update this user",
                                "status_code": 403
                            }
                        }
                    }
                }
            })
async def update_user(user_update: UserRequestAdd,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user),):
    """
    Update user information
    :param user_update:
    :param db:
    :param current_user:
    :return: UserOut
    """
    return await UserManager(db).perform_action_user("update_user",
                                                     user=user_update,
                                                     current_user=current_user)


@router.delete("/delete",
               responses={
                  404: {
                       "description": "User not found",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "User not found",
                                   "status_code": 404
                               }
                           }
                       }
                   },
                   403: {
                       "description": "Not authorized",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Not authorized to delete this user",
                                   "status_code": 403
                               }
                           }
                       }
                   }
               }
               )
async def delete_user(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Delete user account
    :param db:
    :param current_user:
    :return: Success message
    """
    return await UserManager(db).perform_action_user("delete_user",
                                                     current_user=current_user)
