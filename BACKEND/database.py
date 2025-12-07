# database.py
import mariadb

# Production Database
# DB_CONFIG = {
#     "host": "202.28.24.55",
#     "user": "python_engine",
#     "password": "c#@4573kt",
#     "database": "cvdtt_lab",
#     "port": 3306
# }

# test Database
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "cvdtt_lab",
    "port": 3306
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None