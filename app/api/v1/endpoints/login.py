"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.schemas.login import TokenRequest, TokenResponse
from app.db.mysql import get_db
from app.services.login.actions import LoginManager

router = APIRouter()


@router.post("/login",
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


@router.post("/swagger",
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
