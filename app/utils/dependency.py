from app.core.config import settings
from app.db.session import DbConnection


def get_db():
    db = DbConnection(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE
    )
    db.connect()
    try:
        yield db
    finally:
        db.close()
