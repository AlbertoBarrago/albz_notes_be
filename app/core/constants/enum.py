"""
 Enum
"""
from enum import Enum

class UserRole(str, Enum):
    """User Role Enum"""
    ADMIN = "ADMIN"
    GUEST = "GUEST"
