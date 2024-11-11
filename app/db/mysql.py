"""
Dependency Utils
"""
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.db.models.users import User

SQLALCHEMY_DATABASE_URL = (f"mysql+pymysql://"
                           f"{settings.MYSQL_USER}:"
                           f"{settings.MYSQL_PASSWORD}"
                           f"@{settings.MYSQL_HOST}"
                           f"/{settings.MYSQL_DATABASE}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/swagger-login")


def get_db():
    """
    Get database session
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    """
    Get Current User in Session
    :param token:
    :param db:
    :return: User
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(status_code=401,
                                detail="Invalid authentication credentials")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Token has expired") from None
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,
                            detail="Invalid token") from None
