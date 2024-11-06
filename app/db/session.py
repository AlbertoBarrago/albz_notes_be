import mysql
from mysql.connector import Error


class DbConnection:
    def __init__(self, **config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def fetch_query(self, query, params=None):
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except Error as e:
                print(f"Error fetching data: {e}")
                return None
            finally:
                cursor.close()
        return None

    def commit(self):
        if self.connection and self.connection.is_connected():
            try:
                self.connection.commit()
                print("Transaction committed")
            except Error as e:
                print(f"Error committing transaction: {e}")

    def rollback(self):
        if self.connection and self.connection.is_connected():
            try:
                self.connection.rollback()
                print("Transaction rolled back")
            except Error as e:
                print(f"Error rolling back transaction: {e}")
