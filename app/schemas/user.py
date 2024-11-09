"""
User Schema
"""
from datetime import datetime

from pydantic import BaseModel

class UserBase(BaseModel):
    """
    User Base Model
    """
    username: str
    email: str

class UserCreate(UserBase):
    """
    User Create Model
    """
    password: str

class UserOut(UserBase):
    """
    User Out Model
    """
    created_at: datetime

    model_config = {"env_file": ".env"}
