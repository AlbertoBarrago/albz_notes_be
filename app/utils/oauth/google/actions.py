"""
 Google OAuth Actions
"""
import secrets

import requests
from fastapi import HTTPException
from pydantic.v1 import EmailStr
from starlette import status
from starlette.responses import JSONResponse

from app.core.access_token import generate_user_token
from app.db.models import User
from app.schemas.login import TokenRequest
from app.utils.audit.actions import log_action
from app.email.email_service import EmailService, EmailSchema


def get_info_from_google(token):
    """
    Get info from Google
    :param token:
    :return:
    """
    if not token:
        return JSONResponse(content={"error": "Token not present"}, status_code=400)

    google_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'

    try:
        response = requests.get(google_url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return {
            "error": f"Errore durante la richiesta a Google: {e}"
        }

    user_info = response.json()
    email = user_info.get('email')
    name = user_info.get('name')
    picurl = user_info.get('picture')
    if not email or not name:
        return {
            "error": "Informazioni utente non valide"
        }
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

    user = db.query(User).filter(User.email == user_from_google['email']).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.picture_url:
        user.picture_url = user_from_google['picurl']
        db.commit()
        db.refresh(user)

    request = TokenRequest(username=user_from_google['name'])

    if not user:
        return {
            "error": "User not found"
        }

    return request

async def add_user_to_db(db, request):
    """
    Add User to DB
    :param db:
    :param request:
    :return:
    """

    user_from_google = get_info_from_google(request.credential)

    existing_user = db.query(User).filter(User.email == user_from_google['email']).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User exist, try to login...",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
        log_action(db,
                   user_id=user_fetched.user_id,
                   action="Google Registered",
                   description="Registered user By Google")

        token = generate_user_token(user_fetched)
        #Send email with temp password
        email_service = EmailService()
        email_schema = EmailSchema(
            username=user.username,
            email=[EmailStr(user.email)],
        )
        await email_service.send_password_setup_email(email_schema, token)

        result = {
            "access_token": token,
            "token_type": "bearer",
            "user": user_fetched
        }
        return result
