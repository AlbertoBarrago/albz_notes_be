"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.mysql import get_db
from app.schemas.auth.request import TokenResponse, OauthRequest
from app.schemas.user.request import GoogleResetRequest
from app.services.auth.login.repository import LoginManager
from app.services.auth.oauth.google.repository import get_user_info, add_user_to_db
from app.services.user.repository import UserManager

router = APIRouter()


@router.post("/oauth/login",
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

    return  LoginManager(db).perform_action_auth(
                               "login",
                               get_user_info(db, request),
                               oauth=True)


@router.post("/oauth/register",
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


@router.post("/oauth/reset",
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
async def reset_google_password(
        google_req: GoogleResetRequest,
        db: Session = Depends(get_db)
):
    """
    Reset user password
    :param google_req: Google reset request containing a token and new password
    :param db: Database session
    :return: Success message
    """
    return await UserManager(db).reset_google_password_with_token(
        token=google_req.token,
        new_password=google_req.new_password
    )
