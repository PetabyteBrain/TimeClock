"""
Route definitions

Functions:
 - init_routes(app): Initializes all the routes for the Flask application.
    - index(): Renders the main index page.
    - get_ip(): Returns the client's IP address as a JSON response.
    - favicon(): Serves the favicon for the application.
    - get_users(): Retrieves and returns a list of all users.
    - get_user_byid(user_id): Retrieves and returns user information by user ID.
    - get_user_byName(user_name): Retrieves and returns user information by username.
    - create_user_route(): Creates a new user based on the provided data.
    - edit_user_route(user_id): Updates an existing user with the provided data.
"""
from flask import jsonify, request, render_template, abort, send_from_directory
import os
from .mysqlConnector import get_db_connection
from .services import get_all_users, get_user_by_id, get_user_by_name, create_user, update_user
from .utils import is_valid_email

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/ip', methods=['GET'])
    def get_ip():
        ip_address = request.remote_addr
        return jsonify({'ip_address': ip_address})

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico')


    # Routing for /user
    @app.route('/users', methods=['GET'])
    def get_users():
        """
        Get all Users
        ---
        tags:
          - Users
        responses:
          200:
            description: Successful operation
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  firstName:
                    type: string
                    example: "James"
                  lastName:
                    type: string
                    example: "Bond"
                  tagNum:
                    type: string
                    example: "5498754759"
                  email:
                    type: string
                    example: "example@example.com"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: Not found
        """
        return get_all_users()

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user_byid(user_id):
        """
        Get user by ID
        ---
        tags:
          - Users
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user
        responses:
          200:
            description: Successful operation
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                firstName:
                  type: string
                  example: "James"
                lastName:
                  type: string
                  example: "Bond"
                email:
                  type: string
                  example: "example@example.com"
                tagNum:
                  type: string
                  example: "5498754759"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: User not found
        """
        return get_user_by_id(user_id)

    @app.route('/users/<string:user_name>', methods=['GET'])
    def get_user_byName(user_name):
        """
        Get user by name
        ---
        tags:
          - Users
        parameters:
          - name: user_name
            in: path
            required: true
            type: string
            description: The name of the user
        responses:
          200:
            description: Successful operation
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                firstName:
                  type: string
                  example: "James"
                lastName:
                  type: string
                  example: "Bond"
                email:
                  type: string
                  example: "example@example.com"
                tagNum:
                  type: string
                  example: "5498754759"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: User not found
        """
        return get_user_by_name(user_name)

    @app.route('/users', methods=['POST'])
    def create_user_route():
        """
        Create a new user
        ---
        tags:
          - Users
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                firstName:
                  type: string
                  example: "James"
                lastName:
                  type: string
                  example: "Bond"
                tagNum:
                  type: string
                  example: "5498754759"
                email:
                  type: string
                  example: "example@example.com"
                password:
                  type: string
                  example: "password123"
        responses:
          200:
            description: User created successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                firstName:
                  type: string
                  example: "James"
                lastName:
                  type: string
                  example: "Bond"
                tagNum:
                  type: string
                  example: "5498754759"
                email:
                  type: string
                  example: "example@example.com"
          400:
            description: Invalid input
          500:
            description: Database connection failed
        """
        return create_user()

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def edit_user_route(user_id):
        """
        Edit an existing user
        ---
        tags:
          - Users
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user to edit
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                firstName:
                  type: string
                  example: "James"
                lastName:
                  type: string
                  example: "Bond"
                email:
                  type: string
                  example: "example@example.com"
        responses:
          200:
            description: User updated successfully
          400:
            description: Invalid input
          404:
            description: User not found
          500:
            description: Database connection failed
        """
        data = request.get_json()
        return update_user(user_id, data)
