"""
Initialize the Flask app and extensions.

This module sets up the Flask application and its extensions, including CORS 
for handling cross-origin requests and Swagger for API documentation.
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError
from .config import Config
from .mysqlConnector import get_db_connection

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure SECRET_KEY is set
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong key

# Initialize CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Initialize extensions
CORS(app)
swagger = Swagger(app, 
                  template={
                      "swagger": "2.0",
                      "info": {
                          "title": "Stempel Uhr",
                          "version": "1.0.0",
                          "description": "API documentation for Punch in clock.",
                          "license": {
                              "name": "GNU GENERAL PUBLIC LICENSE",
                              "url": "https://www.gnu.org/licenses/gpl-3.0.en.html"
                          }
                      },
                      "externalDocs": {
                          "description": "Find out more about TimeClock",
                          "url": "https://github.com/PetabyteBrain/TimeClock"
                      },
                      "basePath": "/",
                      "schemes": ["http", "https"],
                  })

# User loader for Flask-Login
from .authentication import User

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM User WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(
            id=user['id'],
            firstName=user['firstName'],
            lastName=user['lastName'],
            email=user['email'],
            role=user['permission_id']
        )
    return None

# Register routes
from .routes import init_routes
init_routes(app)

# Optional: CSRF error handling
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return "CSRF token missing or invalid.", 400
