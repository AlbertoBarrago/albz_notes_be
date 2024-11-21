"""
Session actions
"""
from app.core.access_token import generate_user_token_and_return_user
from app.db.models.users import User
from app.utils.audit.actions import logger
from app.utils.error.auth import AuthErrorHandler


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
                AuthErrorHandler.raise_user_not_found()

            if not kargs.get('oauth') and not user_fetched.verify_password(request.password) :
                AuthErrorHandler.raise_unauthorized()

            logger(db,
                   user_id=user_fetched.user_id,
                   action=f"${len(action) > 0 and action or 'Login'}",
                   description="User logged in successfully")


            result = generate_user_token_and_return_user(user_fetched)
        case "swagger_login":
            if grant_type != "password":
                AuthErrorHandler.raise_invalid_grant_type()

            username = kargs.get('username')
            password = kargs.get('password')
            user_fetched = (db.query(User)
                            .filter((User.username == username) |
                                    (User.email == username))
                            .first())
            if not user_fetched or not user_fetched.verify_password(password):
                AuthErrorHandler.raise_invalid_credentials()

            logger(db,
                   user_id=user_fetched.user_id,
                   action="Login",
                   description="Logged from swagger")

            result = generate_user_token_and_return_user(user_fetched)

    return result
