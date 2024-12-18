from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw
from functools import wraps
from .mysqlConnector import get_db_connection
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from .utils import * #Temoporary 

app = Flask(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class (required by Flask-Login)
class User(UserMixin):
    def __init__(self, id, firstName, lastName, email, role):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.role = role


class RegisterForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    tagNum = StringField('Tag Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Register')

# Role-based access decorator
def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if(current_user.role == 1):
                current_user.role = "dev"
            elif(current_user.role == 2):
                current_user.role = "admin"
            elif(current_user.role == 3):
                current_user.role = "supervisor"
            elif(current_user.role == 4):
                current_user.role = "user"
            elif(current_user.role == 4):
                current_user.role = "guest"
            print(current_user.role)
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Define a login form using Flask-WTF
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

def auth_login():
    form = LoginForm()
    if form.validate_on_submit():  # Automatically checks CSRF token
        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM User WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            login_user(User(id=user['id'], firstName=user['firstName'], lastName=user['lastName'], email=user['email'], role=user['permission_id']), remember=True)
            return redirect(url_for('dashboard'))
        return 'Invalid credentials!'
    return render_template('login.html', form=form)


def auth_register():
    form = RegisterForm()

    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        tagNum = form.tagNum.data

        # Hash the password
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("START TRANSACTION;")

            # Insert into User table
            cursor.execute(
                "INSERT INTO User (firstName, lastName, tagNum, email, password, permission_id) "
                "VALUES (%s, %s, %s, %s, %s, (SELECT id FROM Permissions WHERE title = 'Standard User'));",
                (firstName, lastName, tagNum, email, hashed_password)
            )
            conn.commit()

            cursor.execute(
                "SELECT id FROM User WHERE email = %s;",
                (email,)
            )
            user_id = cursor.fetchone()

            if user_id:
                cursor.execute(
                    "INSERT INTO TotalTime (sumTime, daysWorked, breakTime, user_id) "
                    "VALUES ('00:00:00', 0, '00:00:00', %s);",
                    (user_id[0],)
                )
                conn.commit()

                return redirect(url_for('login'))
            else:
                conn.rollback()
                return jsonify({"error": "User creation failed after insert."}), 500

        except Exception as e:
            conn.rollback()
            return jsonify({"error": f"Error: {str(e)}"}), 500
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html', form=form)

def auth_logout():
    logout_user()
    return redirect(url_for('login'))

