"""
Session module
"""
import mysql
from mysql.connector import Error


class DbConnection:
    """
    Db Connector Mysql
    """
    def __init__(self, **config):
        self.config = config
        self.connection = None

    def connect(self):
        """
        Connect to MySQL
        """
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        """
        Close MySQL connection
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def fetch_query(self, query, params=None):
        """
        Fetch query from MySQL database
        :param query:
        :param params:
        """
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
        """
        Commit changes to MySQL database
        """
        if self.connection and self.connection.is_connected():
            try:
                self.connection.commit()
                print("Transaction committed")
            except Error as e:
                print(f"Error committing transaction: {e}")

    def rollback(self):
        """
        Rollback changes to MySQL database
        """
        if self.connection and self.connection.is_connected():
            try:
                self.connection.rollback()
                print("Transaction rolled back")
            except Error as e:
                print(f"Error rolling back transaction: {e}")
