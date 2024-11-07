import os

from dotenv import load_dotenv

from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DATABASE: str

    SECRET_KEY: str = os.getenv("SECRET_KEY", "8d0f39701a43810766d0c9fa25acd6f0097dff05c2d0322d8983969c88c81bd8")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
