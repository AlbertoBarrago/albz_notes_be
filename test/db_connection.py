import pymysql

from app.core.config import settings


def test_mysql_connection():
    try:
        connection = pymysql.connect(
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            host=settings.MYSQL_HOST,
            database=settings.MYSQL_DATABASE
        )
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")

