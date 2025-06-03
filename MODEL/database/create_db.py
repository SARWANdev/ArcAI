from .utils.db_connector import database_connection
import mysql.connector
from mysql.connector import Error
from .utils.configuration import DB_CONFIG


def create_database():
    # Connect without specifying a database
    config = DB_CONFIG.copy()
    del config['database']
    try:
        with mysql.connector.connect(**config) as connection:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print(f"Database {DB_CONFIG['database']} created successfully")

            # Create tables
            create_tables()
    except Error as e:
        print(f"Error creating database: {e}")


def create_tables():
    with database_connection() as connection:
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS User
                       (
                           user_id    INT AUTO_INCREMENT PRIMARY KEY,
                           first_name VARCHAR(50)  NOT NULL,
                           last_name  VARCHAR(50)  NOT NULL,
                           email      VARCHAR(100) NOT NULL UNIQUE,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                       )
                       """)

        # Projects table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Project
                       (
                           project_id  INT AUTO_INCREMENT PRIMARY KEY,
                           user_id     INT          NOT NULL,
                           name        VARCHAR(100) NOT NULL,
                           description TEXT,
                           note        TEXT,
                           created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                           FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
                       )
                       """)

        # Documents table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Document
                       (
                           document_id    INT AUTO_INCREMENT PRIMARY KEY,
                           project_id     INT          NOT NULL,
                           name           VARCHAR(100) NOT NULL,
                           path           VARCHAR(255) NOT NULL,
                           note           TEXT,
                           is_it_read     BOOLEAN   DEFAULT FALSE, 
                           is_it_favorite BOOLEAN   DEFAULT FALSE, 
                           journal        TEXT,                    
                           first_author   VARCHAR(100),            
                           tag            VARCHAR(50),             
                           created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                           FOREIGN KEY (project_id) REFERENCES Project (project_id) ON DELETE CASCADE
                       )
                       """)

        print("Tables created successfully")


if __name__ == "__main__":
    create_database()

