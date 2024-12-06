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
from .services import *

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
                permissionLevel:
                  type: string
                  example: "User"
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
    
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user_byid(user_id):
        """
        Delete user by ID
        ---
        tags:
          - Users
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user to delete
        responses:
          200:
            description: User deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User with id 1 deleted successfully"
          404:
            description: User not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
          500:
            description: Database connection failed
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Database connection failed"
        """
        return delete_user_by_id(user_id)

  
    # Routing for /permissions
    @app.route('/permissions', methods=['GET'])
    def get_permissions():
        """
        Get all permisssions
        ---
        tags:
          - Permissions
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
        return get_all_permissions()
    

    # Routing for /onlinetime
    @app.route('/onlinetime', methods=['GET'])
    def get_onlinetime():
        """
        Get all onlinetime
        ---
        tags:
          - Onlinetime
        responses:
          200:
            description: Successful operation
            schema:
              type: array
              items:
                type: object
                properties:
                  firstName:
                    type: string
                    example: "John"
                  lastName:
                    type: string
                    example: "Doe"
                  dateTimeStart:
                    type: string
                    example: "Fri, 01 Nov 2024 08:00:00 GMT"
                  dateTimeStop:
                    type: string
                    example: "Fri, 01 Nov 2024 17:00:00 GMT"
                  breakTime:
                    type: string
                    example: "60"
                  id:
                    type: int
                    example: "1"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: Not found
        """
        return get_all_onlinetime()
    
    @app.route('/onlinetime/<int:user_id>', methods=['GET'])
    def get_onlinetime_byid(user_id):
        """
        Get online time by user ID
        ---
        tags:
          - Onlinetime
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
                firstName:
                  type: string
                  example: "John"
                lastName:
                  type: string
                  example: "Doe"
                dateTimeStart:
                  type: string
                  example: "Fri, 01 Nov 2024 08:00:00 GMT"
                dateTimeStop:
                  type: string
                  example: "Fri, 01 Nov 2024 17:00:00 GMT"
                breakTime:
                  type: string
                  example: "60"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: User not found
        """
        return get_onlinetime_by_id(user_id)
    
    @app.route('/onlinetime/start/<int:user_id>', methods=['POST'])
    def create_onlinetime_route(user_id):
        """
        Start a new Session
        ---
        tags:
          - Onlinetime
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user
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
        return create_onlinetime(user_id)
    
    @app.route('/onlinetime/stop/<int:user_id>', methods=['POST'])
    def stop_onlinetime_route(user_id):
        """
        Stop an existing Session
        ---
        tags:
          - Onlinetime
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user
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
        return stop_onlinetime(user_id)
    
    @app.route('/onlinetime/edit/<int:user_id>/<string:session_time_identifier>', methods=['PUT'])
    def edit_onlinetime_route(user_id, session_time_identifier):
        """
        Edit a previous Session
        ---
        tags:
          - Onlinetime
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user to edit
          - name: session_time_identifier
            in: path
            required: true
            type: string
            description: the End time of the Session
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                dateTimeStart:
                  type: string
                  example: "2024-11-01 08:00:00"
                dateTimeStop:
                  type: string
                  example: "2024-11-01 17:00:00"
        responses:
          200:
            description: Session updated successfully
          400:
            description: Invalid input
          404:
            description: Session not found
          500:
            description: Database connection failed
        """
        data = request.get_json()
        return update_onlinetime(user_id, session_time_identifier, data)
      
    @app.route('/onlinetime/<int:user_id>/<string:session_time_identifier>', methods=['DELETE'])
    def delete_onlineTime_byid(user_id, session_time_identifier):
        """
        Delete onlinetime by User_ID & End time of session
        ---
        tags:
          - Onlinetime
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user to delete
          - name: session_time_identifier
            in: path
            required: true
            type: string
            description: the End time of the Session
        responses:
          200:
            description: User deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User with id 1 deleted successfully"
          404:
            description: User not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
          500:
            description: Database connection failed
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Database connection failed"
        """
        return delete_onlineTime_by_id(user_id, session_time_identifier)
  
  # Routing for /totaltime
    @app.route('/totaltime', methods=['GET'])
    def get_totaltime():
        """
        Get all Totaltime
        ---
        tags:
          - Totaltime
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
                  sumTime:
                    type: string
                    example: "40:00:00"
                  daysWorked:
                    type: integer
                    example: 5
                  breakTime:
                    type: string
                    example: "2:30:00"
          400:
            description: Invalid status value
          401:
            description: Unauthorized request
          404:
            description: Not found
          500:
            description: Internal server error
        """
        return get_all_totaltime()
    
    @app.route('/totaltime/<int:user_id>', methods=['GET'])
    def get_totaltime_byid(user_id):
        """
        Get total time by user ID
        ---
        tags:
          - Totaltime
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
        return get_totaltime_by_id(user_id)