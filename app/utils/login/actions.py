"""
Session actions
"""
from fastapi import HTTPException
from starlette import status

from app.core.access_token import generate_user_token_and_return_user
from app.db.models.users import User
from app.utils.audit.actions import log_action


def perform_action_auth(db,
                        action: str,
                        request=None,
                        grant_type=None,
                        **kargs):
    """
    Perform authentication action
    :param db:
    :param request:
    :param action:
    :param grant_type:
    return User
    """
    result = None
    match action:
        case "login":
            user_fetched = (db.query(User)
                            .filter((User.username == request.username) |
                                    (User.email == request.username))
                            .first())


            if not user_fetched:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not kargs.get('oauth') and not user_fetched.verify_password(request.password) :
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not Authorized",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            log_action(db,
                       user_id=user_fetched.user_id,
                       action=f"${len(action) > 0 and action or 'Login'}",
                       description="User logged in successfully")


            result = generate_user_token_and_return_user(user_fetched)
        case "swagger_login":
            if grant_type != "password":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid grant type"
                )
            username = kargs.get('username')
            password = kargs.get('password')
            user_fetched = (db.query(User)
                            .filter((User.username == username) |
                                    (User.email == username))
                            .first())
            if not user_fetched or not user_fetched.verify_password(password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            log_action(db,
                       user_id=user_fetched.user_id,
                       action="Login",
                       description="Logged from swagger")

            result = generate_user_token_and_return_user(user_fetched)

    return result
