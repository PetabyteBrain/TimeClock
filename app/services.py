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
from .utils import is_valid_email, is_valid_datetime, is_duplicate_firstName, is_duplicate_lastName, is_duplicate_tagNum, is_duplicate_email, update_total_time

# /users functions
def get_all_users():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT id, firstName, lastName, tagNum, email FROM user;")
            rows = cursor.fetchall()
            if rows:
                users = [{'id': row[0], 
                          'firstName': row[1], 
                          'lastName': row[2], 
                          'tagNum': row[3], 
                          'email': row[4]
                          } for row in rows]
                return jsonify(users), 200
            else:
                return jsonify({"message": "No Users found"}), 404
    else:
        return jsonify({"message": "Database connection failed"}), 500

def get_user_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT `User`.id, firstName, lastName, tagNum, email, Permissions.title FROM `user` JOIN Permissions ON `User`.permission_id = Permissions.id WHERE `User`.id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                user = {'id': row[0], 
                        'firstName': row[1], 
                        'lastName': row[2], 
                        'tagNum': row[3], 
                        'email': row[4],
                        'permission': row[5]}
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
            cursor.execute("SELECT `User`.id, firstName, lastName, tagNum, email, Permissions.title FROM `user` JOIN Permissions ON `User`.permission_id = Permissions.id WHERE firstName = %s OR lastName = %s", (user_name, user_name))
            rows = cursor.fetchall()  # Fetch all matching rows
            if rows:
                # Construct a list of users
                users = [
                    {
                        'id': row[0],
                        'firstName': row[1],
                        'lastName': row[2],
                        'tagNum': row[3],
                        'email': row[4],
                        'permission': row[5]
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
    
    if user_firstName is None:
        return jsonify({"error": "Required field is missing (firstname)"}), 400
    if user_lastName is None:
        return jsonify({"error": "Required field is missing (lastname)"}), 400
    if user_tagNum is None:
        return jsonify({"error": "Required field is missing (tag Number)"}), 400
    if user_email is None:
        return jsonify({"error": "Required field is missing (email)"}), 400
    if not is_valid_email(user_email):
        return jsonify({"error": "Invalid email format"}), 400
    if user_password is None:
        return jsonify({"error": "Required field is missing (password)"}), 400
    
    if is_duplicate_firstName(user_firstName) == True and is_duplicate_lastName(user_lastName) == True:
        return jsonify({"error": "FirstName and lastName already belongs to another user, try using another."}), 400
    if is_duplicate_email(user_email) == True:
        return jsonify({"error": "Email is already used for another account, try using another."}), 400
    if is_duplicate_tagNum(user_tagNum) == True:
        return jsonify({"error": "Tag number is already in use for another account, try using another."}), 400

    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Start a transaction
                cursor.execute("START TRANSACTION;")

                # Create User in user table
                cursor.execute(
                    "INSERT INTO user (firstName, lastName, tagNum, email, password, permission_id) VALUES (%s, %s, %s, %s, SHA2(%s, 512), (SELECT id FROM Permissions where title = 'Standard User'));",
                    (user_firstName, user_lastName, user_tagNum, user_email, user_password)
                )
                cnx.commit()  # Commit after inserting the user

                # Get the user id from the inserted user
                cursor.execute(
                    "SELECT `User`.id, firstName, lastName, tagNum, email, Permissions.title FROM `user` JOIN Permissions ON `User`.permission_id = Permissions.id WHERE firstName = %s AND lastName = %s;",
                    (user_firstName, user_lastName)
                )
                row = cursor.fetchone()

                if row:
                    user = {'id': row[0], 
                            'firstName': row[1], 
                            'lastName': row[2], 
                            'tagNum': row[3], 
                            'email': row[4],
                            'permission': row[5]}

                    # Create TotalTime for User
                    cursor.execute(
                        "INSERT INTO TotalTime (sumTime, daysWorked, breakTime, user_id) VALUES ('00:00:00', 0, '00:00:00', %s);",
                        (row[0],)  # Passing user id to TotalTime table
                    )
                    cnx.commit()  # Commit if everything works

                    return jsonify(user), 200

                else:
                    # If user data is not retrieved, rollback the transaction and delete the user
                    cnx.rollback()
                    return jsonify({"error": "User creation failed after insert."}), 500

        except Exception as e:
            # If there's any exception, rollback the transaction and remove the user
            cnx.rollback()

            # If a user was created but there's an error, delete the user
            cursor.execute(
                "DELETE FROM user WHERE email = %s AND firstname = %s AND lastname = %s;", (user_email, user_firstName, user_lastName,)
            )
            cnx.commit()  # Commit after deletion
            return jsonify({"error": f"Error: {str(e)}"}), 500
        finally:
            cnx.close()  # Ensure the connection is closed

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
                # Start a transaction
                cursor.execute("START TRANSACTION;")

                # Check if the user exists
                cursor.execute("SELECT id FROM user WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                
                if not row:
                    return jsonify({"message": "User not found"}), 404

                # Delete sessions in the onlinetime table for the user
                cursor.execute("DELETE FROM onlinetime WHERE user_id = %s", (user_id,))

                # Delete the total time associated with the user
                cursor.execute("DELETE FROM totaltime WHERE user_id = %s", (user_id,))

                # Now delete the user from the user table
                cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))

                cnx.commit()  # Commit after all deletions

                return jsonify({"message": f"User with id {user_id} and associated data deleted successfully"}), 200

        except Exception as e:
            # Rollback the transaction if there's an error
            cnx.rollback()

            # Return the error message
            return jsonify({"message": f"Error: {str(e)}"}), 500

        finally:
            cnx.close()  # Ensure the connection is closed

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
            cursor.execute("SELECT User.id, firstName, lastName, dateTimeStart, dateTimeStop, breakTime FROM OnlineTime JOIN `User` ON OnlineTime.user_id = `User`.id;")
            rows = cursor.fetchall()
            onlineTime = [{'id': row[0], 
                           'firstName': row[1], 
                           'lastName': row[2], 
                           'dateTimeStart': row[3], 
                           'dateTimeStop': row[4], 
                           'breakTime': row[5]
                           } for row in rows]
            return jsonify(onlineTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
def get_onlinetime_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT firstName, lastName, dateTimeStart, dateTimeStop, breakTime FROM OnlineTime JOIN `User` ON OnlineTime.user_id = `User`.id where user_id = %s;", (user_id,))
            rows = cursor.fetchall()
            onlineTime = [{'firstName': row[0], 
                           'lastName': row[1], 
                           'dateTimeStart': row[2], 
                           'dateTimeStop': row[3], 
                           'breakTime': row[4]
                           } for row in rows]
            return jsonify(onlineTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
def create_onlinetime(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            """
            check if new session was already created
            """ 
            cursor.execute(
                "SELECT id, dateTimeStart, dateTimeStop, breakTime, user_id  FROM onlinetime where user_id = %s AND dateTimeStop IS NULL order by dateTimeStart desc limit 1;", (user_id,)
            )
            row = cursor.fetchone()
            if row:
                session = {'id': row[0], 
                        'dateTimeStart': row[1], 
                        'dateTimeStop': row[2], 
                        'breakTime': row[3], 
                        'user_id': row[4]}
            try:
                if row == None:
                    cursor.execute(
                    "INSERT INTO OnlineTime (dateTimeStart, user_id) VALUES (NOW(), %s);", (user_id,)
                    )
                    cnx.commit()
                    cursor.execute("SELECT *  FROM onlinetime where user_id = %s AND dateTimeStop IS NULL order by dateTimeStart desc limit 1;", (user_id,)
                                   )
                    row = cursor.fetchone()
                    if row:
                        user = {'id': row[0], 
                                'dateTimeStart': row[1], 
                                'dateTimeStop': row[2], 
                                'breakTime': row[3], 
                                'user_id': row[4]}
                        return jsonify({"message": "Session was succesfully started"}), 200
                else:
                    return jsonify({"message": "Error occured, could not open session"}), 400
            except Exception as e:
                return jsonify({"message": "Error occured, could not open session"}), 400
    else:
        return abort(500, description="Database connection failed")

def stop_onlinetime(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            try:
                cursor.execute("SELECT id, dateTimeStart, dateTimeStop, user_id  FROM onlinetime where user_id = %s AND dateTimeStop IS NULL order by dateTimeStart desc limit 1;", (user_id,)
                           )
                row = cursor.fetchone()
                if row:
                    dateStop_check = {'id': row[0], 
                            'dateTimeStart': row[1], 
                            'dateTimeStop': row[2],
                            'user_id': row[3]}
            except Exception as e:
                print(f"error: {e}")
                return(f"error: {e}")
            else:
                try:
                    if all(var is not None for var in (row[0], row[1], row[3])) and row[2] is None:
                        cursor.execute(
                        "UPDATE onlinetime SET dateTimeStop = now() WHERE user_id = %s AND dateTimeStop IS NULL;", (user_id,)
                        )
                        cnx.commit()
                        cursor.execute("SELECT *  FROM onlinetime where user_id = %s AND dateTimeStop IS not NULL order by dateTimeStart desc limit 1;", (user_id,)
                                       )
                        row = cursor.fetchone()
                        if row:
                            session = {'id': row[0], 
                                    'dateTimeStart': str(row[1]), 
                                    'dateTimeStop': str(row[2]), 
                                    'breakTime': row[3], 
                                    'user_id': row[4]}
                        cursor.execute("SELECT firstName, lastName FROM `User` where id = %s;", (user_id,)
                                       )
                        row2 = cursor.fetchone()
                        if row2:
                            user = {'firstName': row2[0],
                                    'lastName': row2[1]}
                            
                        update_total_time(user_id)
                        return jsonify({"message": "Session was succesfully stopped at: "+ str(row[2]) + ",for the User: "+ row2[0] + " " + row2[1]}), 200
                    elif row == None:
                        return jsonify({"message": "Error occured, could not find open session"}), 404
                    else:
                        return jsonify({"message": "An unexpected error occured"}), 500
                except Exception as e:
                    print(e)
                    return jsonify({"message": "Error occured, could not find open session"}), 404

    else:
        return abort(500, description="Database connection failed")

def update_onlinetime(user_id, session_time_identifier, data):
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
    if 'dateTimeStart' in data and data['dateTimeStart']:
        updates.append("dateTimeStart = %s")
        params.append(data['dateTimeStart'])
    if 'dateTimeStop' in data and data['dateTimeStop']:
        updates.append("dateTimeStop = %s")
        params.append(data['dateTimeStop'])

    # If no fields are provided, return a 400 error
    if not updates:
        abort(400, description="No fields to update")

    # Add the user_id to the parameters (last parameter)
    params.append(user_id)
    params.append(session_time_identifier)

    # Construct the SQL query with the updates
    sql_query = f"UPDATE onlinetime SET {', '.join(updates)} WHERE id = %s AND dateTimeStop = %s"

    cnx = get_db_connection()
    if not is_valid_datetime(session_time_identifier):
                return jsonify({"message": "Invalid session_time_identifier format"}), 400
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Execute the update query
                cursor.execute(sql_query, params)
                cnx.commit()  # Commit the transaction

                # Check if the user was updated
                if cursor.rowcount > 0:
                    update_total_time(user_id)
                    return jsonify({"message": "User updated successfully"}), 200
                else:
                    abort(404, description="User not found")  # Return 404 if no user found
        except Exception as e:
            # Log the error (you might consider adding proper logging)
            abort(500, description=f"Database error: {str(e)}")  # Return 500 if an error occurs
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        return abort(500, description="Database connection failed")  # Return 500 if connection fails

def delete_onlineTime_by_id(user_id, session_time_identifier):
    cnx = get_db_connection()
    if not is_valid_datetime(session_time_identifier):
                return jsonify({"message": "Invalid session_time_identifier format"}), 400
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Check if the user exists
                cursor.execute("Select * from OnlineTime WHERE user_id = %s AND dateTimeStop is not NULL AND dateTimeStop = %s;", (user_id, session_time_identifier))
                row = cursor.fetchall()
                
                if not row:
                    return jsonify({"message": "Session not found"}), 404

                # If user exists, delete them
                else:
                    cursor.execute("DELETE FROM OnlineTime WHERE user_id = %s AND dateTimeStop is not NULL AND dateTimeStop = %s;", (user_id, session_time_identifier))
                    cnx.commit()  # Commit the transaction after the deletion

                    update_total_time(user_id)
                    return jsonify({"message": f"Session from User with id {user_id} was deleted successfully"}), 200
        except Exception as e:
            print(f"Error: {e}")  # Log the error
            return jsonify({"message": "An internal error occurred"}), 500
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        return jsonify({"message": "Database connection failed"}), 500

# /totaltime functions
def get_all_totaltime():
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT `User`.id, firstName, lastName, sumTime, daysWorked, breakTime FROM totaltime JOIN `User` ON totalTime.user_id = `User`.id;")
            rows = cursor.fetchall()
            totalTime = [{'user_id': row[0], 
                          'firstName': row[1], 
                          'lastName': row[2], 
                          'sumTime': str(row[3]),
                          'daysWorked': row[4], 
                          'breakTime': str(row[5])
                          } for row in rows]
            return jsonify(totalTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500

def get_totaltime_by_id(user_id):
    cnx = get_db_connection()
    if cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT `User`.id, firstName, lastName, sumTime, daysWorked, breakTime FROM totaltime JOIN `User` ON totalTime.user_id = `User`.id where `User`.id = %s;", (user_id,))
            rows = cursor.fetchall()
            totalTime = [{'user.id': row[0], 
                          'firstName': row[1], 
                          'lastName': row[2], 
                          'sumTime': str(row[3]),
                          'daysWorked': row[4], 
                          'breakTime': str(row[5])
                          } for row in rows]
            return jsonify(totalTime), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500
    
