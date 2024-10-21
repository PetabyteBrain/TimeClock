"""
Database connection logic.

This module contains functions for establishing a connection to the MySQL database.
"""
import mysql.connector
from mysql.connector import Error
from .config import Config

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        MySQLConnection: A connection object if the connection is successful, 
                         or None if the connection fails.
    """
    config = {
        'user': Config.MYSQL_DATABASE_USERNAME,
        'password': Config.MYSQL_DATABASE_PASSWORD,
        'host': Config.MYSQL_DATABASE_HOST,
        'port': Config.MYSQL_DATABASE_PORT,
        'database': Config.MYSQL_DATABASE_DBNAME
    }

    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            return cnx
    except Error as e:
        print(f"Error: {e}")
    return None
