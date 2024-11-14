"""
Access Token
"""
from datetime import datetime, timedelta
import jwt

from fastapi import HTTPException

from app.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
     Create a JWT access token
    :param data:
    :param expires_delta:
    :return: encoded_jwt
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode a JWT access token
    :param token:
    :return: jwt.decode() -> str
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Token expired") from None
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token") from None


def generate_user_token(user):
    """Generate access token for user"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
