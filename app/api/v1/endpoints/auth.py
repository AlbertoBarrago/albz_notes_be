"""
    Auth Endpoint
"""

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.schemas.auth import TokenRequest, TokenResponse
from app.schemas.user import UserCreate
from app.utils.audit.actions import log_action
from app.utils.auth.actions import perform_action_auth
from app.db.mysql import get_db

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register user
    :param user:
    :param db:
    :return: UserOut
    """
    new_user = perform_action_auth(db, "register_user", user=user)

    log_action(db,
               user_id=new_user['new_user'].user_id,
               action="Register",
               description="Registered user")

    return {"access_token": new_user['access_token'],
            "token_type": "bearer",
            "user": new_user['user']}


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

    log_action(db,
               user_id=user_logged['user'].user_id,
               action="Token",
               description="Logged from token")

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

    log_action(db,
               user_id=user_logged['user'].user_id,
               action="Login",
               description="Logged from swagger")

    return {"access_token": user_logged['access_token'],
            "token_type": "bearer",
            "user": user_logged['user']}
