"""
Config props
"""
import os

from dotenv import load_dotenv

from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Settings class
    """
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DATABASE: str
    SECRET_KEY: str = (
        os
        .getenv("SECRET_KEY", "8d0f39701a43810766d0c9fa25acd6f0097dff05c2d0322d8983969c88c81bd8"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_SECRET_KEY: str = os.getenv("GOOGLE_SECRET_KEY")
    RATE_LIMIT: str = os.getenv("RATE_LIMIT")
    RATE_LIMIT_WINDOW: str = os.getenv("RATE_LIMIT_WINDOW")

    class Config:
        """
        Config class
        """
        env_file = ".env"

settings = Settings()
