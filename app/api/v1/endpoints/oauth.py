"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.login import TokenResponse, OauthRequest
from app.utils.login.actions import perform_action_auth
from app.db.mysql import get_db
from app.utils.oauth.google.actions import get_user_info, add_user_to_db

router = APIRouter()


@router.post("/login/google",
             response_model=TokenResponse,
             responses={
                 401: {
                     "description": "Incorrect username or password",
                     "content": {
                         "application/json": {
                           "example": {
                               "status_code": 401,
                               "detail": "Incorrect username or password",
                               "headers": {
                                   "WWW-Authenticate": "Bearer"
                               }
                           }
                         }
                     }
                 },
                 404: {
                     "description": "User not found",
                     "content": {
                         "application/json": {
                             "example": {
                                 "status_code": 404,
                                  "detail": "User not found, Try to register",
                                 "headers": {
                                      "WWW-Authenticate": "Bearer"
                                  }
                             }
                         }
                     }
                 }
             })
def login_google(request: OauthRequest,
                 db: Session = Depends(get_db)):
    """
    Login from Google
    :param request:
    :param db:
    :return: Token
    """
    return perform_action_auth(db,
                               "login",
                               get_user_info(db, request),
                               oauth=True)


@router.post("/register/google",
             response_model=TokenResponse,
             responses={
                 400: {
                     "description": "User already exists",
                     "content": {
                         "application/json": {
                             "example": {
                                 "status_code": 400,
                                 "detail": "User already exists, Try to login",
                                 "headers": {
                                     "WWW-Authenticate": "Bearer"
                                 }
                             }
                         }
                     }
                 },
                 401: {
                     "description": "Not authorized",
                     "content": {
                         "application/json": {
                             "example": {
                                 "status_code": 401,
                                 "detail": "Not authorized",
                                 "headers": {
                                     "WWW-Authenticate": "Bearer"
                                 }
                             }
                         }
                     }
                 },
                 404: {
                     "description": "User not found",
                     "content": {
                         "application/json": {
                             "example": {
                                 "status_code": 404,
                                 "detail": "User not found, Try to register",
                                 "headers": {
                                     "WWW-Authenticate": "Bearer"
                                 }
                             }
                         }
                     }
                 }
             })
def register_from_google(request: OauthRequest,
                         background_tasks: BackgroundTasks,
                         db: Session = Depends(get_db)):
    """
    Register from Google
    :param request:
    :param background_tasks:
    :param db:
    :return: Token
    """
    return add_user_to_db(db, request, background_tasks)
