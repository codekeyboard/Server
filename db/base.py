from util.config import config
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host=config("db.host"),
        user=config("db.user"),
        password=config("db.password"),
        database=config("db.database"),
    )
    return conn