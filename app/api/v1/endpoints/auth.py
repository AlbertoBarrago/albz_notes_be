"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.schemas.auth.request import TokenRequest, TokenResponse
from app.schemas.user.request import PasswordReset
from app.services.auth.login.repository import LoginManager
from app.services.user.repository import UserManager

router = APIRouter()


@router.post("/auth/login",
             response_model=TokenResponse,
             responses={
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
                 },
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
             })
def login(
        request: TokenRequest,
        db: Session = Depends(get_db)
):
    """
    Login from Web JSON
    :param request:
    :param db:
    :return: Token
    """
    return LoginManager(db).perform_action_auth("login", request)


@router.post("/auth/swagger",
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
             },
             include_in_schema=False)
def swagger_login(
        grant_type: str = Form(description="OAuth grant type"),
        username: str = Form(description="User's username or email"),
        password: str = Form(description="User's password"),
        db: Session = Depends(get_db)
):
    """
    Login Swagger
    :param grant_type:
    :param username:
    :param password:
    :param db:
    :return: Token
    """

    return LoginManager(db).perform_action_auth(
        "swagger_login",
        grant_type=grant_type,
        username=username,
        password=password)


@router.post("/auth/refresh-token", response_model=TokenResponse)
async def refresh_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Refresh access token
    """
    return UserManager(db).generate_user_token_and_return_user(current_user)


@router.post("/auth/reset",
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
