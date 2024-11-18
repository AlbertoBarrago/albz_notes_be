"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.login import TokenResponse, OauthRequest
from app.utils.login.actions import perform_action_auth
from app.db.mysql import get_db
from app.utils.oauth.google.actions import get_user_info

router = APIRouter()


@router.post("/oauth/google", response_model=TokenResponse)
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
