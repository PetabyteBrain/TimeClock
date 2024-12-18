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
from .services import * #Temoporary 
from .authentication import * #Temoporary
from . import csrf



def init_routes(app):
    @csrf.exempt
    @app.route('/')
    def index():
        return render_template('home.html')

    @csrf.exempt
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    # Routing for Authentication ------------------------------------------------------------------
    @app.route('/home', methods=['GET'])
    def home():
        """
        Home page
        ---
        tags:
          - Navigation
        responses:
          200:
            description: The home page
        """
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        User Login
        ---
        tags:
          - Authentication
        parameters:
          - name: email
            in: formData
            type: string
            required: True
            description: User email address
          - name: password
            in: formData
            type: string
            required: True
            description: User password
        responses:
          200:
            description: Login successful
          401:
            description: Invalid credentials
        """
        return auth_login()

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        User Registration
        ---
        tags:
          - Authentication
        responses:
          201:
            description: Registration successful
          400:
            description: Invalid registration data
        """
        return auth_register()

    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """
        User Dashboard
        ---
        tags:
          - Dashboard
        responses:
          200:
            description: Dashboard loaded successfully
          401:
            description: Unauthorized access
        """
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/admin', methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def admin_dashboard():
        """
        Admin Dashboard
        ---
        tags:
          - Dashboard
        responses:
          200:
            description: Admin dashboard loaded successfully
          403:
            description: Access forbidden - Admin role required
        """
        return render_template('adminDashboard.html', user=current_user)
    
    @csrf.exempt
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        """
        User Logout
        ---
        tags:
          - Authentication
        responses:
          200:
            description: Logout successful
          401:
            description: Unauthorized - User not logged in
        """
        return auth_logout()
    
    # Error handler for unauthorized access
    @app.errorhandler(403)
    def forbidden(e):
        """
        Access Forbidden Error
        ---
        tags:
          - Errors
        responses:
          403:
            description: Access forbidden - User lacks required permissions
        """
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Access Forbidden</title>
            <script>
                alert('Access forbidden: You do not have the necessary permissions.');
                window.history.back(); // Redirect the user back to the previous page
            </script>
        </head>
        <body>
            <h1>Access Forbidden</h1>
            <p>You do not have the necessary permissions to view this page.</p>
        </body>
        </html>
        """, 403

    # Inject current_user into templates
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    # Routing for /user -----------------------------------------------------------------------------
    @app.route('/users/all', methods=['GET'])
    @login_required
    @role_required('admin')
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

    @app.route('/users', methods=['GET'])
    @login_required
    def get_user_byid():
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
        user_id = current_user.id  # Get the ID of the logged-in user
        return get_user_by_id(user_id)

    @app.route('/users/<string:user_name>', methods=['GET'])
    @login_required
    @role_required('admin')
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
    @login_required
    @role_required('admin')
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

    @app.route('/users', methods=['PUT'])
    @login_required
    def edit_user_route():
        """
        Edit an existing user
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
        user_id = current_user.id  # Get the ID of the logged-in user
        data = request.get_json()
        return update_user(user_id, data)
    
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @login_required
    @role_required('admin')
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
    @app.route('/onlinetime/all', methods=['GET'])
    @login_required
    @role_required('admin')
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
    
    @app.route('/onlinetime', methods=['GET'])
    @login_required
    def get_onlinetime_byid():
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
        user_id = current_user.id  # Get the ID of the logged-in user
        return get_onlinetime_by_id(user_id)
    
    @app.route('/onlinetime/start', methods=['POST'])
    @login_required
    def create_onlinetime_route():
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
        user_id = current_user.id  # Get the ID of the logged-in user
        return create_onlinetime(user_id)
    
    @app.route('/onlinetime/stop', methods=['POST'])
    @login_required
    def stop_onlinetime_route():
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
        user_id = current_user.id  # Get the ID of the logged-in user
        return stop_onlinetime(user_id)
    
    @app.route('/onlinetime/edit/<int:user_id>/<string:session_time_identifier>', methods=['PUT'])
    @login_required
    @role_required('admin')
    def edit_onlinetime_route(user_id, session_time_identifier):
        """
        Edit an existing session
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
              description: The identifier for the session (typically end time)
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
    @login_required
    @role_required('admin')
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
    @app.route('/totaltime/all', methods=['GET'])
    @login_required
    @role_required('admin')
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
    
    @app.route('/totaltime', methods=['GET'])
    @login_required
    def get_totaltime_byid():
        """
        Get total time for the logged-in user
        ---
        tags:
          - Totaltime
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
        user_id = current_user.id  # Get the ID of the logged-in user
        return get_totaltime_by_id(user_id)