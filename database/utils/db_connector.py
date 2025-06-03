import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

from .configuration import DB_CONFIG


@contextmanager
def database_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()
