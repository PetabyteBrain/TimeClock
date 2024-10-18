import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3305',
    'database': 'TimeClockDB'
}

def getUsers():
    print("hello")

try:
    # Unpack config dictionary into the connect method
    cnx = mysql.connector.connect(**config)

    if cnx.is_connected():
        print("Connected to the database")

        with cnx.cursor() as cursor:
            # Execute the query
            cursor.execute("SHOW TABLES")

            # Fetch all rows from the result
            rows = cursor.fetchall()

            # Loop through the results and print each row
            for row in rows:
                print(row)

        # Close the connection
        cnx.close()

    else:
        print("Could not connect to the database")


except Error as e:
    print(f"Error: {e}")

finally:
    # Ensure the connection is closed
    if cnx.is_connected():
        cnx.close()
        print("Connection closed")
