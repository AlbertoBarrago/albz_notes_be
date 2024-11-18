"""
User Schema
"""
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    User Base Model
    """
    role: str = "GUEST"
    username: str
    email: str
    picture: str = None


class UserPsw(UserBase):
    """
    User Update Model
    """
    password: str


class PasswordReset(BaseModel):
    """
    Password Reset Model
    """
    username: str
    current_password: str
    new_password: str


class UserOut(UserBase):
    """
    User Out Model
    """
    created_at: datetime
