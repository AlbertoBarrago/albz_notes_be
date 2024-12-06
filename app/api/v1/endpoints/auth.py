"""
    Auth Endpoint
"""
from fastapi import APIRouter, Depends, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.mysql import get_db, get_current_user
from app.repositories.auth.login.repository import LoginManager
from app.repositories.auth.reset.repository import PasswordManager
from app.repositories.user.repository import UserManager
from app.schemas.auth.request import TokenRequest, TokenResponse, ResetRequest, ResetUserEmail
from app.schemas.common.responses import CommonResponses
from app.schemas.user.request import ResetPswRequest

router = APIRouter()


@router.post("/auth/login",
             response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
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
    return LoginManager(db).perform_action_auth("login", request)


@router.post("/auth/swagger",
             response_model=TokenResponse,
             responses=CommonResponses.UNAUTHORIZED,
             include_in_schema=False)
def swagger_login(
        grant_type: str = Form(description="OAuth grant type"),
        username: str = Form(description="User's username or email"),
        password: str = Form(description="User's password"),
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

    return LoginManager(db).perform_action_auth(
        "swagger_login",
        grant_type=grant_type,
        username=username,
        password=password)


@router.post("/auth/refresh-token", response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
async def refresh_token(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
    Refresh access token
    """
    return UserManager(db).perform_action_user(
        "generate_user_token_and_return_user",
        current_user)


@router.post("/auth/reset",
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
async def reset_password(
        psw_req: ResetPswRequest,
        db: Session = Depends(get_db)
):
    """
    Reset user password
    :param psw_req: Google reset request containing a token and new password
    :param db: Database session
    :return: Success message
    """
    return await UserManager(db).perform_action_user(
        "reset_password",
        token=psw_req.token,
        new_password=psw_req.new_password
    )


@router.post("/auth/send-reset-email",
             response_model=TokenResponse,
             responses={**CommonResponses.INTERNAL_SERVER_ERROR, **CommonResponses.UNAUTHORIZED})
def send_reset_email(
        request: ResetRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
    Send it reset a password email
    :return: Success message
    """
    return PasswordManager(db).send_password_reset_email(
        username=request.username,
        token=request.token,
        background_tasks=background_tasks,
    )


@router.post("/auth/password-reset")
async def request_password_reset(
        request: ResetUserEmail,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
       Initiate a password reset process for a user

       Args:
           request (ResetUserEmail): Email request object containing user's email
           background_tasks (BackgroundTasks): FastAPI background tasks handler
           db (Session): Database session dependency

       Returns:
           dict: Response containing status of password reset initiation
       """
    return PasswordManager(db).initiate_password_reset(request.email, background_tasks)
