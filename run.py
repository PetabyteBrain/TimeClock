"""
Start script to run the application.

This script serves as the entry point for the Flask application. 
When executed, it runs the application in debug mode, allowing for easier development and debugging.
"""
from app import app

if __name__ == '__main__':
    app.run(debug=True)
