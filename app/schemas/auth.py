"""
Auth Schema
"""
from pydantic import BaseModel

class TokenRequest(BaseModel):
    """
    Token Request Model
    """
    grant_type: str
    email: str
    username: str
    password: str

class Token(BaseModel):
    """
    Token Response Model
    """
    access_token: str
    token_type: str
