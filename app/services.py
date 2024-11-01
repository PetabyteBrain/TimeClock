"""
Business logic and service layer

Functions:
 - get_all_users(): Retrieves and returns a list of all users from the database.
 - get_user_by_id(user_id): Retrieves and returns user information by user ID.
 - get_user_by_name(user_name): Retrieves and returns user information by username.
 - create_user(): Creates a new user based on the provided data and returns the created user.
 - update_user(user_id, data): Updates user details in the database based on the provided user ID and data.
"""
from flask import jsonify, abort, request
from .mysqlConnector import get_db_connection
from .utils import is_valid_email

# /users functions
def get_all_users():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user")
            rows = cursor.fetchall()
            users = [{'id': row[0], 
                      'firstName': row[1], 
                      'lastName': row[2], 
                      'tagNum': row[3], 
                      'email': row[4]
                      } for row in rows]
            return jsonify(users), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500

def get_user_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                user = {'id': row[0], 
                        'firstName': row[1], 
                        'lastName': row[2], 
                        'tagNum': row[3], 
                        'email': row[4]}
                return jsonify(user), 200
            else:
                return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "Database connection failed"}), 500

def get_user_by_name(user_name):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            # Query to search for users with the same first or last name
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE firstName = %s OR lastName = %s", (user_name, user_name))
            rows = cursor.fetchall()  # Fetch all matching rows
            if rows:
                # Construct a list of users
                users = [
                    {
                        'id': row[0],
                        'firstName': row[1],
                        'lastName': row[2],
                        'tagNum': row[3],
                        'email': row[4]
                    } for row in rows
                ]
                return jsonify(users), 200  # Return the list of users
            else:
                return jsonify({"message": "User not found"}), 404  # If no users found
    else:
        return jsonify({"message": "Database connection failed"}), 500  # If DB connection fails


def create_user():
    data = request.get_json()
    user_firstName = data.get('firstName')
    user_lastName = data.get('lastName')
    user_tagNum = data.get('tagNum')
    user_email = data.get('email')
    user_password = data.get('password')

    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user (firstName, lastName, tagNum, email, password) VALUES (%s, %s, %s, %s, SHA2(%s, 512));",
                (user_firstName, user_lastName, user_tagNum, user_email, user_password)
            )
            cnx.commit()
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE firstName = %s OR lastName = %s",
                           (user_firstName, user_lastName))
            row = cursor.fetchone()
            if row:
                user = {'id': row[0], 
                        'firstName': row[1], 
                        'lastName': row[2], 
                        'tagNum': row[3], 
                        'email': row[4]}
                return jsonify(user), 200
    return jsonify({"message": "Database connection failed"}), 500

def update_user(user_id, data):
    """
    Updates user details in the database.
    :param user_id: The ID of the user to update.
    :param data: JSON data containing the fields to update.
    :return: JSON response and status code.
    """
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
    if 'email' in data and data['email']:
        if not is_valid_email(data['email']):
            abort(400, description="Invalid email format")
        updates.append("email = %s")
        params.append(data['email'])

    # If no fields are provided, return a 400 error
    if not updates:
        abort(400, description="No fields to update")

    # Add the user_id to the parameters (last parameter)
    params.append(user_id)

    # Construct the SQL query with the updates
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
                    abort(404, description="User not found")  # Return 404 if no user found
        except Exception as e:
            # Log the error (you might consider adding proper logging)
            abort(500, description=f"Database error: {str(e)}")  # Return 500 if an error occurs
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        abort(500, description="Database connection failed")  # Return 500 if connection fails

def delete_user_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Check if the user exists
                cursor.execute("SELECT id FROM user WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                
                if not row:
                    return jsonify({"message": "User not found"}), 404

                # If user exists, delete them
                cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
                cnx.commit()  # Commit the transaction after the deletion

                return jsonify({"message": f"User with id {user_id} deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500  # Return an error if the deletion fails
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        return jsonify({"message": "Database connection failed"}), 500


# /permission functions
def get_all_permissions():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT permissionLevel, title FROM permissions")
            rows = cursor.fetchall()
            users = [{'permissionLevel': row[0], 
                      'title': row[1]
                      } for row in rows]
            return jsonify(users), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
# /onlinetime functions
def get_all_onlinetime():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT tagNum, firstName , lastname, dateTimeStart, dateTimeStop, break FROM onlinetime Join user;")
            rows = cursor.fetchall()
            onlineTime = [{'tagNum': row[0], 
                           'firstName': row[1], 
                           'lastName': row[2], 
                           'dateTimeStart': row[3], 
                           'dateTimeStop': row[4], 
                           'break': row[5]
                           } for row in rows]
            return jsonify(onlineTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
def get_onlinetime_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT tagNum, firstName, lastName, dateTimeStart, dateTimeStop, break FROM onlinetime JOIN user ON onlinetime.user_Fid = user.id WHERE user.id = %s", (user_id,))
            rows = cursor.fetchall()
            onlineTime = [{'tagNum': row[0], 
                           'firstName': row[1], 
                           'lastName': row[2], 
                           'dateTimeStart': row[3], 
                           'dateTimeStop': row[4], 
                           'break': row[5]
                           } for row in rows]
            return jsonify(onlineTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
def create_onlinetime():
    data = request.get_json()
    user_firstName = data.get('firstName')
    user_lastName = data.get('lastName')
    user_tagNum = data.get('tagNum')
    user_email = data.get('email')
    user_password = data.get('password')

    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user (firstName, lastName, tagNum, email, password) VALUES (%s, %s, %s, %s, SHA2(%s, 512));",
                (user_firstName, user_lastName, user_tagNum, user_email, user_password)
            )
            cnx.commit()
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user WHERE firstName = %s OR lastName = %s",
                           (user_firstName, user_lastName))
            row = cursor.fetchone()
            if row:
                user = {'id': row[0], 
                        'firstName': row[1], 
                        'lastName': row[2], 
                        'tagNum': row[3], 
                        'email': row[4]}
                return jsonify(user), 200
    return jsonify({"message": "Database connection failed"}), 500

def update_onlinetime(user_id, data):
    """
    Updates user details in the database.
    :param user_id: The ID of the user to update.
    :param data: JSON data containing the fields to update.
    :return: JSON response and status code.
    """
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
    if 'email' in data and data['email']:
        if not is_valid_email(data['email']):
            abort(400, description="Invalid email format")
        updates.append("email = %s")
        params.append(data['email'])

    # If no fields are provided, return a 400 error
    if not updates:
        abort(400, description="No fields to update")

    # Add the user_id to the parameters (last parameter)
    params.append(user_id)

    # Construct the SQL query with the updates
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
                    abort(404, description="User not found")  # Return 404 if no user found
        except Exception as e:
            # Log the error (you might consider adding proper logging)
            abort(500, description=f"Database error: {str(e)}")  # Return 500 if an error occurs
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        abort(500, description="Database connection failed")  # Return 500 if connection fails
    

# /totaltime functions
def get_all_totaltime():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT user.id, firstName, lastName, sumTime, daysWorked, breakTime from totalTime right JOIN user ON totaltime.user_Fid = user.id;")
            rows = cursor.fetchall()
            totalTime = [{'user.id': row[0], 
                          'firstName': row[1], 
                          'lastName': row[2], 
                          'sumTime': row[3], 
                          'daysWorked': row[4], 
                          'breakTime': row[5]
                          } for row in rows]
            return jsonify(totalTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500

def get_totaltime_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT user.id, firstName, lastName, sumTime, daysWorked, breakTime from totalTime right JOIN user ON totaltime.user_Fid = user.id WHERE user.id = %s", (user_id,))
            rows = cursor.fetchall()
            totalTime = [{'user.id': row[0], 
                          'firstName': row[1], 
                          'lastName': row[2], 
                          'sumTime': row[3], 
                          'daysWorked': row[4], 
                          'breakTime': row[5]
                          } for row in rows]
            return jsonify(totalTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
