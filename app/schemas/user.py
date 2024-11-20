"""
User Schema
"""
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    User Base Model
    """
    role: str = "GUEST"
    username: str
    email: str


class UserRequestAdd(UserBase):
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

class GoogleEmailRequest(BaseModel):
    """
    Google Email Request Model
    """
    email: str
    new_password: str


class UserOut(UserBase):
    """
    User Out Model
    """
    user_id: str
    username: str
    email: str
    picture_url: Optional[str] = None
