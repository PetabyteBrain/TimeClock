import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
import subprocess

load_dotenv()
MYSQL_DATABASE_USERNAME = os.getenv('MYSQL_DATABASE_USERNAME')
MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')
MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST')
MYSQL_DATABASE_PORT = os.getenv('MYSQL_DATABASE_PORT')
MYSQL_DATABASE_DBNAME = os.getenv('MYSQL_DATABASE_DBNAME')

config = {
    'user': MYSQL_DATABASE_USERNAME,
    'password': MYSQL_DATABASE_PASSWORD,
    'host': MYSQL_DATABASE_HOST,
    'port': MYSQL_DATABASE_PORT,
    'database': MYSQL_DATABASE_DBNAME
}

app = Flask(__name__)
swagger = Swagger(app, 
                  template={
                      "swagger": "2.0",
                      "info": {
                          "title": "Stempel Uhr",
                          "version": "1.0.0",
                          "description": "API documentation for Punch in clock."
                      },
                      "basePath": "/",
                      "schemes": ["http", "https"],
                  })
CORS(app)  # Enable CORS for all routes

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ip', methods=['GET'])
def get_ip():
    # Get the IP address from the request
    ip_address = request.remote_addr
    return jsonify({'ip_address': ip_address})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico')

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    Get answer from Flask
    ---
    responses:
      200:
        description: A list of sample data
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Sample Item"
    """
    # Sample data to return
    sample_data = [
        {"id": 1, "name": "Sample Item 1"},
        {"id": 2, "name": "Sample Item 2"},
    ]
    return jsonify(sample_data)

# Function to get a database connection
def get_db_connection():
    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            return cnx
    except Error as e:
        print(f"Error: {e}")
    return None


# /users
@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all Users
    ---
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
    print("Getting all users")
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user")
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append({
                    'id': row[0],
                    'firstName': row[1],
                    'lastName': row[2],
                    'tagNum': row[3],
                    'email': row[4]
                })
            return jsonify(users), 200  # Return users with a 200 OK status
    else:
        return jsonify({"message": "Database connection failed"}), 500  # Return 500 if connection fails


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_byid(user_id):
    """
    Get user by id
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        schema:
          type: string
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
        description: Not found
    """
    print(f"Getting user with ID: {user_id}")
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE id = %s", (user_id,))
            rows = cursor.fetchall()
            if rows:
                user = {
                    'id': rows[0][0],
                    'firstName': rows[0][1],
                    'lastName': rows[0][2],
                    'tagNum': rows[0][3],
                    'email': rows[0][4]
                }
                return jsonify(user), 200  # Return user with a 200 OK status
            else:
                return jsonify({"message": "User not found"}), 404  # Return 404 if no user found
    else:
        return jsonify({"message": "Database connection failed"}), 500  # Return 500 if connection fails
    
@app.route('/users/<string:user_name>', methods=['GET'])
def get_user_byName(user_name):
    """
    Get user by name
    ---
    parameters:
      - name: user_name
        in: path
        type: string
        required: true
        schema:
          type: string
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
        description: Not found
    """
    print(f"Getting user with ID: {user_name}")
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE firstName = %s OR lastName = %s", (user_name, user_name))
            rows = cursor.fetchall()
            if rows:
                user = {
                    'id': rows[0][0],
                    'firstName': rows[0][1],
                    'lastName': rows[0][2],
                    'tagNum': rows[0][3],
                    'email': rows[0][4]
                }
                return jsonify(user), 200  # Return user with a 200 OK status
            else:
                return jsonify({"message": "User not found"}), 404  # Return 404 if no user found
    else:
        return jsonify({"message": "Database connection failed"}), 500  # Return 500 if connection fails

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create new user
    ---
    parameters:
      - name: user_name
        in: path
        type: string
        required: true
        schema:
          type: string
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
        description: Not found
    """
    data = request.get_json()

    # Extract user data from the request
    user_firstName = data.get('firstName')
    user_lastName = data.get('lastName')
    user_tagNum = data.get('tagNum')
    user_email = data.get('email')
    user_password = data.get('password')

    print(f"Creating user {user_firstName} {user_lastName}")

    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user (firstName, lastName, tagNum, email, password) VALUES (%s, %s, %s, %s, SHA2(%s, 512));",
                    (user_firstName, user_lastName, user_tagNum, user_email, user_password)
                )
                cnx.commit()  # Commit the transaction

                cursor.execute(
                    "SELECT id, firstName, lastName, tagNum, email FROM user WHERE firstName = %s OR lastName = %s",
                    (user_firstName, user_lastName)
                )
                rows = cursor.fetchall()
                if rows:
                    user = {
                        'id': rows[0][0],
                        'firstName': rows[0][1],
                        'lastName': rows[0][2],
                        'tagNum': rows[0][3],
                        'email': rows[0][4]
                    }
                    return jsonify(user), 200  # Return user with a 200 OK status
                else:
                    return jsonify({"message": "User not found"}), 404  # Return 404 if no user found
        except Exception as e:
            return jsonify({"message": str(e)}), 500  # Return 500 if an error occurs
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        return jsonify({"message": "Database connection failed"}), 500  # Return 500 if connection fails


@app.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    """
    Edit an existing user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
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
            tagNum:
              type: string
              example: "5498754759"
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

    # Initialize a list to hold the fields to update
    updates = []
    params = []

    # Check each field and add to updates if it's provided
    if 'firstName' in data and data['firstName']:
        updates.append("firstName = %s")
        params.append(data['firstName'])
    if 'lastName' in data and data['lastName']:
        updates.append("lastName = %s")
        params.append(data['lastName'])
    if 'tagNum' in data and data['tagNum']:
        updates.append("tagNum = %s")
        params.append(data['tagNum'])
    if 'email' in data and data['email']:
        updates.append("email = %s")
        params.append(data['email'])

    # If no fields are provided, return a 400 error
    if not updates:
        return jsonify({"message": "No fields to update"}), 400

    # Add the user_id to the parameters
    params.append(user_id)

    # Construct the SQL query
    sql_query = f"UPDATE user SET {', '.join(updates)} WHERE id = %s"

    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Execute the update query
                cursor.execute(sql_query, params)
                cnx.commit()  # Commit the transaction

                # Check if the user was updated
                if cursor.rowcount > 0:
                    return jsonify({"message": "User updated successfully"}), 200
                else:
                    return jsonify({"message": "User not found"}), 404  # Return 404 if no user found
        except Exception as e:
            return jsonify({"message": str(e)}), 500  # Return 500 if an error occurs
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        return jsonify({"message": "Database connection failed"}), 500  # Return 500 if connection fails



#start app
if __name__ == '__main__':
    app.run(debug=True)


