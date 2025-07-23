import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from lib.user import *
from lib.user_repository import *

# Load environment variables from .env file 
load_dotenv()

# Create a new Flask app
app = Flask(__name__)

# Configuirng Flask-WTF - needed for CSRF protection and form handling
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application. Check your .env file.")


# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')



# new code below
"""
get all users
"""
@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)
        users = repository.all()
        return render_template('users/index.html', users=users)
    except Exception as e:
        return f"Database error: {e}"
"""
get a single user by id
"""
@app.route('/users/<int:id>', methods=['GET'])
def show_user(id):
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user = repository.find(id)
    return render_template('users/show.html', user=user)

"""
post a new user
"""
# GET /users/new
# Returns a form to create a new book
@app.route('/users/new', methods=['GET'])
def get_new_user():
    return render_template('users/new.html')

@app.route('/users', methods=['POST'])
def create_user():
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    # Get the fields from the request form
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Create a user object
    user = User(None, name, email, password)

    # # Check for validity and if not valid, show the form again with errors
    # if not user.is_valid():
    #     return render_template('users/new.html', user=user, errors=user.generate_errors()), 400

    # Save the book to the database
    user = repository.create(user)

    # Redirect to the book's show route to the user can see it
    return redirect(f"/users/{user.id}")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))