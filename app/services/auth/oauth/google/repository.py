"""
 Google OAuth Actions
"""
import secrets

import requests
from pydantic.v1 import EmailStr
from starlette.responses import JSONResponse

from app.core import generate_user_token
from app.core.exeptions.auth import AuthErrorHandler
from app.db.models import User
from app.email.email_service import (EmailService,
                                     EmailSchema)
from app.schemas.auth.request import TokenRequest
from app.services.audit.repository import log_audit_event
from app.services.logger.repository import LoggerService

logger = LoggerService().logger


def get_info_from_google(token):
    """
    Get info from Google
    :param token:
    :return:
    """
    response = None
    if not token:
        return JSONResponse(content={"error": "Token not present"}, status_code=400)

    google_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'

    try:
        response = requests.get(google_url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        AuthErrorHandler.raise_unauthorized()

    user_info = response.json()
    email = user_info.get('email')
    name = user_info.get('name')
    picurl = user_info.get('picture')
    if not email or not name:
        AuthErrorHandler.raise_unauthorized()
    return {
        "email": email,
        "name": name,
        "picurl": picurl
    }


def get_user_info(db, request):
    """
    Get User Info
    :param db:
    :param request:
    :return:
    """
    user_from_google = get_info_from_google(request.credential)

    if 'error' in user_from_google:
        AuthErrorHandler.raise_invalid_token()

    user = db.query(User).filter(User.email == user_from_google['email']).first()

    if not user:
        AuthErrorHandler.raise_user_not_found()

    if not user.picture_url:
        user.picture_url = user_from_google['picurl']
        db.commit()
        db.refresh(user)

    request = TokenRequest(username=user_from_google['name'])

    log_audit_event(db, user_id=user.user_id, action="login", description="Login from Google")
    logger.info("User %s login from Google", user.user_id)

    return request


def add_user_to_db(db, request, background_tasks):
    """
    Add User to DB and send email
    :param db:
    :param request:
    :param background_tasks:
    :return:
    """
    result = None
    user_from_google = get_info_from_google(request.credential)

    existing_user = db.query(User).filter(User.email == user_from_google['email']).first()

    if existing_user:
        AuthErrorHandler.raise_existing_user_error()

    if not existing_user:
        temp_password = secrets.token_urlsafe(32)
        user = User(
            email=user_from_google['email'],
            username=user_from_google['name'],
            picture_url=user_from_google['picurl'],
        )
        user.set_password(temp_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        user_fetched = db.query(User).filter(User.email == user_from_google['email']).first()
        log_audit_event(db,
                        user_id=user_fetched.user_id,
                        action="Google Registered",
                        description="Registered user By Google")
        logger.info("User %s registered", user_fetched.user_id)

        token = generate_user_token(user_fetched)

        try:
            email_service = EmailService()
            email_schema = EmailSchema(
                username=user.username,
                email=[EmailStr(user.email)],
            )
            background_tasks.add_task(
                email_service.send_password_setup_email,
                email_schema,
                token
            )
        except (ConnectionError, TimeoutError):
            GlobalErrorHandler.raise_mail_not_sent()


        result = {
            "access_token": token,
            "token_type": "bearer",
            "user": user_fetched
        }
    return result
