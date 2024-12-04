"""
Login Schema
"""
from pydantic import BaseModel

from app.schemas.user.request import UserOut


class OauthRequest(BaseModel):
    """
    Oauth Request Model
    """
    clientId: str
    credential: str
    username: str = None
    email: str = None


class TokenRequest(BaseModel):
    """
    Token Request Model
    """
    username: str
    email: str = None
    password: str = None

class TokenResponse(BaseModel):
    """
    Token Response Model
    """
    access_token: str
    token_type: str
    user: UserOut


class ResetRequest(BaseModel):
    """
    Reset Request Model
    """
    username: str
    token: str


class ResetUserEmail(BaseModel):
    """
    Reset Request Model
    """
    email: str
