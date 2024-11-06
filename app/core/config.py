from dotenv import load_dotenv

from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DATABASE: str

    class Config:
        env_file = ".env"

settings = Settings()
