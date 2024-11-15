"""
 Google OAuth Actions
"""
import requests
from starlette.responses import JSONResponse

from app.db.models import User
from app.schemas.login import TokenRequest



def get_user_info(db, request):
    """
    Get User Info
    :param db:
    :param request:
    :return:
    """
    token = request.credential
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

    user = db.query(User).filter((User.email == email) | (User.username == name)).first()

    if user is None:
        print("User is None, cannot access user.picture.")
    else:
        if not user.picture and picurl:
            user.picture = picurl
            db.commit()
            db.refresh(user)

    request = TokenRequest(username=name)

    if not user:
        return {
            "error": "Utente non trovato"
        }

    return request
