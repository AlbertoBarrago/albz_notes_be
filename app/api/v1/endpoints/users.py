"""
   User Endpoints
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.repositories.user.repository import UserManager
from app.schemas.auth.request import TokenResponse
from app.schemas.user.request import UserOut, UserBase, UserRequestAdd, UserResponse

router = APIRouter()


@router.get("/", response_model=UserOut, responses={
    401: {
        "description": "Not authenticated",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated",
                }
            }
        }
    }
})
def get_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user
    :param current_user:
    :param db:
    :return: User
    """
    return UserManager(db).perform_action_user('get_user', current_user)


@router.get("/list", response_model=List[UserOut], responses={
    401: {
        "description": "Not authenticated",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated",
                }
            }
        }
    }
})
def get_users_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user
    :param current_user:
    :param db:
    :return: User
    """
    return UserManager(db).perform_action_user(
        "get_users_list",
        current_user=current_user
    )


@router.post("/",
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
                 },
                 401: {
                     "description": "Not authenticated",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Not authenticated",
                             }
                         }
                     }
                 }
             })
async def register_user(user: UserRequestAdd, db: Session = Depends(get_db)):
    """
    Register user
    :param user:
    :param db:
    :return: UserOut
    """
    return await UserManager(db).perform_action_user("register_user",
                                                     user=user)


@router.put("/",
            response_model=UserResponse,
            responses={
                401: {
                    "description": "Not authenticated",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Not authenticated",
                                "status_code": 401
                            }
                        }
                    }
                }
            })
async def update_user(user_update: UserBase,
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


@router.delete("/",
               responses={
                   401: {
                       "description": "Not authenticated",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Not authenticated",
                                   "status_code": 401
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
