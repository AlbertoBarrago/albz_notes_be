"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.login import TokenResponse, OauthRequest
from app.utils.login.actions import perform_action_auth
from app.db.mysql import get_db
from app.utils.oauth.google.actions import get_user_info, add_user_to_db

router = APIRouter()


@router.post("/login/google", response_model=TokenResponse)
async def login_google(request: OauthRequest,
                 db: Session = Depends(get_db)):
    """
    Login from Google
    :param request:
    :param db:
    :return: Token
    """
    return await perform_action_auth(db,
                               "login",
                               get_user_info(db, request),
                               oauth=True)

@router.post("/register/google", response_model=TokenResponse)
async def register_from_google(request: OauthRequest,
                 db: Session = Depends(get_db)):
    """
    Register from Google
    :param request:
    :param db:
    :return: Token
    """
    return await add_user_to_db(db, request)
