"""
Utility functions (e.g., for validation)

Functions:
 - is_valid_email(email): Validates an email address format.
"""
import re
from datetime import datetime
from .mysqlConnector import get_db_connection

def is_valid_email(email):
    """
    Validates an email address format.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # Improved regex pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_valid_datetime(value):
    try:
        datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

#check if User values are already in DB at creation --------------------------------------------------------
def is_duplicate_firstName(value):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Query to check if there is any other user with the same first name
                cursor.execute("SELECT id FROM user WHERE firstName = %s", (value,))
                row = cursor.fetchone()  # Fetch one row (if any)

                if row:
                    return True  # Duplicate found
                else:
                    return False  # No duplicate found
        except Exception as e:
            print(f"Error: {e}")
            return True  #returning True in case of an error (failure to check duplicates)
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        print("Database connection failed")
        return True  # Return True to indicate failure in checking duplicates

def is_duplicate_lastName(value):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Query to check if there is any other user with the same first name
                cursor.execute("SELECT id FROM user WHERE lastName = %s", (value,))
                row = cursor.fetchone()  # Fetch one row (if any)

                if row:
                    return True  # Duplicate found
                else:
                    return False  # No duplicate found
        except Exception as e:
            print(f"Error: {e}")
            return True  #returning True in case of an error (failure to check duplicates)
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        print("Database connection failed")
        return True  # Return True to indicate failure in checking duplicates

def is_duplicate_tagNum(value):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Query to check if there is any other user with the same first name
                cursor.execute("SELECT id FROM user WHERE tagNum = %s", (value,))
                row = cursor.fetchone()  # Fetch one row (if any)

                if row:
                    return True  # Duplicate found
                else:
                    return False  # No duplicate found
        except Exception as e:
            print(f"Error: {e}")
            return True  #returning True in case of an error (failure to check duplicates)
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        print("Database connection failed")
        return True  # Return True to indicate failure in checking duplicates

def is_duplicate_email(value):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Query to check if there is any other user with the same first name
                cursor.execute("SELECT id FROM user WHERE email = %s", (value,))
                row = cursor.fetchone()  # Fetch one row (if any)

                if row:
                    return True  # Duplicate found
                else:
                    return False  # No duplicate found
        except Exception as e:
            print(f"Error: {e}")
            return True  #returning True in case of an error (failure to check duplicates)
        finally:
            cnx.close()  # Ensure the connection is closed
    else:
        print("Database connection failed")
        return True  # Return True to indicate failure in checking duplicates
    
#calculate summed time for Totaltime table --------------------------------------------------------
def update_total_time(user_id):
    cnx = get_db_connection()
    if cnx:
        try:
            with cnx.cursor() as cursor:
                # Calculate total session time in seconds
                cursor.execute(
                    "SELECT SUM(TIMESTAMPDIFF(SECOND, dateTimeStart, dateTimeStop)) AS total_seconds "
                    "FROM OnlineTime WHERE user_id = %s AND dateTimeStop IS NOT NULL;", 
                    (user_id,)
                )
                result = cursor.fetchone()
                
                if result[0] is None:
                    # No completed sessions, set to 0
                    total_seconds = 0
                else:
                    total_seconds = result[0]
                
                # Calculate hours, minutes, and seconds
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                
                # Calculate daysWorked and remaining hours
                days_worked = hours // 24
                remaining_hours = hours % 24
                formatted_time = f"{remaining_hours:02}:{minutes:02}:{seconds:02}"

                # Overwrite TotalTime values
                cursor.execute(
                    "UPDATE TotalTime SET sumTime = %s, daysWorked = %s WHERE user_id = %s;",
                    (formatted_time, days_worked, user_id)
                )
                cnx.commit()
        except Exception as e:
            print(f"Error updating total time for user {user_id}: {e}")
        finally:
            cnx.close()
