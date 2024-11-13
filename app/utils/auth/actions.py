"""
Session actions
"""
from datetime import timedelta

from fastapi import HTTPException
from starlette import status

from app.core.access_token import create_access_token
from app.core.config import settings
from app.db.models.users import User


def perform_action_auth(db,
                        action:str,
                        request= None,
                        user=None,
                        grant_type = None,
                        **kargs):
    """
    Perform authentication action
    :param db:
    :param request:
    :param user:
    :param action:
    :param grant_type:
    return User
    """
    match action:
        case "register_user":
            query = db.query(User).filter(User.username == user.username).first()
            if query:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )

            new_user = User(username=user.username,
                            email=user.email)
            new_user.set_password(user.password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_fetched = db.query(User).filter(User.username == new_user.username).first()
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = (
                create_access_token(data={"sub": user_fetched.username},
                                    expires_delta=access_token_expires))
            return {"access_token": access_token,
                    "new_user": user_fetched}


        case "login":
            user_fetched = db.query(User).filter(User.username == request.username).first()
            if not user_fetched:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user_fetched.verify_password(request.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not Authorized",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = (
                create_access_token(data={"sub": user_fetched.username},
                                    expires_delta=access_token_expires))
            return {"access_token": access_token,
                    "user": user_fetched}

        case "swagger_login":
            if grant_type != "password":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid grant type"
                )
            username = kargs.get('username')
            password = kargs.get('password')
            user_fetched = db.query(User).filter(User.username == username).first()
            if not user_fetched or not user_fetched.verify_password(password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": username},
                                               expires_delta=access_token_expires)

            return {"access_token": access_token, "user": user_fetched}
