"""
   User Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.schemas.auth.request import TokenResponse
from app.schemas.user.request import UserRequestAdd, UserOut
from app.services.user.repository import UserManager

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
    return await UserManager(db).perform_action_user("register_user",
                                                     user=user)


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
                      current_user: User = Depends(get_current_user), ):
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
