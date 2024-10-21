"""
Initialize the Flask app and extensions.

This module sets up the Flask application and its extensions, including CORS 
for handling cross-origin requests and Swagger for API documentation.
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)  # Enable CORS for all routes
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

# Import blueprints or routes
from .routes import init_routes

# Register routes
init_routes(app)
