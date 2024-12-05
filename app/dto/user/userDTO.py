"""
This module defines the UserDTO class, which is used to transfer data between the application and the database.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    user_id: int
    username: str
    email: str
    role: str
    picture_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(user) -> dict:
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "picture_url": user.picture_url or None,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }
