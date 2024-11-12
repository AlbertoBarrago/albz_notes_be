"""
Auth Schema
"""
from pydantic import BaseModel

from app.schemas.user import UserBase


class TokenRequest(BaseModel):
    """
    Token Request Model
    """
    username: str
    password: str

class TokenResponse(BaseModel):
    """
    Token Response Model
    """
    access_token: str
    token_type: str
    user: UserBase
