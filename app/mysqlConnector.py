import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
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
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/users', methods=['GET'])
def get_users():
    result = subprocess.check_output(['users']).decode('utf-8')
    return jsonify({'users': result.strip()})
'''

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico')

@app.route('/api/data', methods=['GET'])
def get_data():
    # Sample data to return
    data = {
        'message': 'Hello from Flask!',
        'status': 'success'
    }
    return jsonify(data)



@app.route('/users', methods=['GET'])
def get_users():
    print("getting Users")
    try:
    # Unpack config dictionary into the connect method
        cnx = mysql.connector.connect(**config)

        if cnx.is_connected():
            print("Connected to the database")

            with cnx.cursor() as cursor:
                # Execute the query
                cursor.execute("Select id, firstName, lastName, tagNum, email from user")

                # Fetch all rows from the result
                rows = cursor.fetchall()

                # Loop through the results and print each row
                print(rows)
                return jsonify(rows)

            # Close the connection
            cnx.close()

        else:
            print("Could not connect to the database")


    except Error as e:
        print(f"Error: {e}")

    finally:
        # Ensure the connection is closed
        # Ensure the connection is closed
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()
            print("Connection closed")

def example_func():
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
        # Ensure the connection is closed
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()
            print("Connection closed")

if __name__ == '__main__':
    app.run(debug=True)


