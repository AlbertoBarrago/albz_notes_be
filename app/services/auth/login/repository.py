"""
Session actions
"""
from app.core.exeptions.auth import AuthErrorHandler
from app.core.security import generate_user_token_and_return_user
from app.db.models.users import User
from app.services.audit.repository import log_audit_event
from app.services.logger.repository import LoggerService

logger = LoggerService().logger

class LoginManager:
    """
    Session manager
    """
    def __init__(self, db):
        self.db = db

    def _get_user(self, username):
        """
        Get user from database
        :param username:
        :return: User object
        """
        return (self.db.query(User)
                .filter((User.username == username) |
                        (User.email == username))
                .first())

    def _log_action(self, user_id, action, description):
        """
        Log action
        :param user_id:
        :param action:
        :param description:
        """
        logger.info("User %s %s %s", user_id, action, description)
        log_audit_event(self.db, user_id=user_id, action=action, description=description)

    def login(self, request, oauth=False):
        """
        Login user
        :param request:
        :param oauth:
        :return: TokenResponse object
        """
        user = self._get_user(request.username)

        if not user:
            AuthErrorHandler.raise_user_not_found()

        if not oauth and not user.verify_password(request.password):
            AuthErrorHandler.raise_invalid_credentials()

        action_name = f"${len('login') > 0 and 'login' or 'Login'}"
        self._log_action(
            user_id=user.user_id,
            action=action_name,
            description="User logged in successfully"
        )

        return generate_user_token_and_return_user(user)

    def swagger_login(self, username, password):
        """
        Login user from swagger
        :param username:
        :param password:
        :return: TokenResponse object
        """
        user = self._get_user(username)

        if not user or not user.verify_password(password):
            AuthErrorHandler.raise_invalid_credentials()

        self._log_action(
            user_id=user.user_id,
            action="Login",
            description="Logged from swagger"
        )

        return generate_user_token_and_return_user(user)

    def perform_action_auth(self, action: str, request=None, **kwargs):
        """
        Perform action auth
        :param action:
        :param request:
        :param kwargs:
        :return: TokenResponse object
        """
        match action:
            case "login":
                return self.login(request, oauth=kwargs.get('oauth', False))
            case "swagger_login":
                return self.swagger_login(kwargs.get('username'), kwargs.get('password'))
