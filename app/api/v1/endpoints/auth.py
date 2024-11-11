"""
    Auth Endpoint
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from starlette import status

from app.core.access_token import create_access_token
from app.core.config import settings
from app.db.models.users import User
from app.schemas.auth import TokenRequest, Token
from app.schemas.user import UserOut, UserCreate
from app.utils.audit import log_action
from app.utils.dependency import get_db

router = APIRouter()


@router.post("/swagger-login", response_model=Token)
def login_swagger(grant_type: str = Form(...),
                  username: str = Form(...),
                  password: str = Form(...),
                  db: Session = Depends(get_db)
                  ):
    """
    Login Swagger
    :param grant_type:
    :param username:
    :param password:
    :param db:
    :return: Token
    """
    if grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type"
        )

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

    log_action(db, user_id=user.user_id, action="Login", description="Logged from swagger")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(
        request: TokenRequest,
        db: Session = Depends(get_db)
):
    """
    Login from Web JSON
    :param request:
    :param db:
    :return: Token
    """

    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = (
        create_access_token(data={"sub": user.username}, expires_delta=access_token_expires))

    log_action(db, user_id=user.user_id, action="Token", description="Logged from token")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register user
    :param user:
    :param db:
    :return: UserOut
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    new_user = User(username=user.username, email=user.email)
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_action(db, user_id=new_user.user_id, action="Register", description="Registered user")
    return new_user
