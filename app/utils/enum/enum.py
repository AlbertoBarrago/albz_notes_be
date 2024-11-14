"""
 Enum
"""
from enum import Enum  # Python Enum for user roles

class UserRole(str, Enum):
    """User Role Enum"""
    ADMIN = "ADMIN"
    GUEST = "GUEST"
