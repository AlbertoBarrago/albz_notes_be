"""
Login Schema
"""
from pydantic import BaseModel

from app.schemas.user import UserBase

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
    password: str = None

class TokenResponse(BaseModel):
    """
    Token Response Model
    """
    access_token: str
    token_type: str
    user: UserBase
