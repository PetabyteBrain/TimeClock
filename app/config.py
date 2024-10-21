"""
Configuration settings (e.g., database, environment).

This module contains configuration settings for the application, 
including database connection details. It loads environment variables 
from a .env file for secure management of sensitive information.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for application settings.

    Attributes:
        MYSQL_DATABASE_USERNAME (str): The username for the MySQL database.
        MYSQL_DATABASE_PASSWORD (str): The password for the MySQL database.
        MYSQL_DATABASE_HOST (str): The host for the MySQL database.
        MYSQL_DATABASE_PORT (str): The port for the MySQL database.
        MYSQL_DATABASE_DBNAME (str): The name of the MySQL database.

    Additional configuration settings can be added as needed.
    """
    MYSQL_DATABASE_USERNAME = os.getenv('MYSQL_DATABASE_USERNAME')
    MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')
    MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST')
    MYSQL_DATABASE_PORT = os.getenv('MYSQL_DATABASE_PORT')
    MYSQL_DATABASE_DBNAME = os.getenv('MYSQL_DATABASE_DBNAME')

    # Additional configuration settings can be added here