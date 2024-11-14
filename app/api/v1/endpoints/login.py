"""
    Auth Endpoint
"""

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.schemas.login import TokenRequest, TokenResponse
from app.utils.login.actions import perform_action_auth
from app.db.mysql import get_db

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
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

    user_logged = perform_action_auth(db,
                                      "login",
                                      request)


    return {"access_token": user_logged['access_token'],
            "token_type": "bearer",
            "user": user_logged['user']}


@router.post("/swagger-login", response_model=TokenResponse)
def swagger_login(grant_type: str = Form(...),
                  username: str = Form(...),
                  password: str = Form(...),
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
    user_logged = perform_action_auth(db, "swagger_login",
                                      grant_type=grant_type,
                                      username=username,
                                      password=password)


    return {"access_token": user_logged['access_token'],
            "token_type": "bearer",
            "user": user_logged['user']}
