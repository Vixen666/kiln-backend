import mysql.connector
from config import db_config

def get_db_connection():
    return mysql.connector.connect(**db_config)

def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()