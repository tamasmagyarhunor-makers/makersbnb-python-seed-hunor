import os
from flask import Flask, request, render_template, redirect, session, url_for
from functools import wraps
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from lib.user import *
from lib.user_repository import *
from lib.forms import *
from lib.space_repository import SpaceRepository

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


# new code below

"""
Adds requirement for user to be logged in
To access certain pages
"""
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))  # sends user to /login
        return route_function(*args, **kwargs)
    return wrapper
    
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

"""
get all users
"""
@app.route('/users', methods=['GET'])
@login_required
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
@login_required
def show_user(id):
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user = repository.find(id)
    return render_template('users/show.html', user=user)


"""
User Registration - Main way to create new users
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            connection = get_flask_database_connection(app)
            repository = UserRepository(connection)

            # Get the fields from the form
            name = form.name.data
            email = form.email.data
            password = form.password.data

            # Create a user object
            user = User(None, name, email, password)
            
            # Save user to database
            user = repository.create(user)
            
            # Redirect to the user's profile page
            return redirect(f"/users/{user.id}")
            
        except Exception as e:
            # Handle database errors gracefully
            return render_template('auth/register.html', form=form, error=f"Registration failed: {e}")
    
    # If GET request or form validation failed, show the form
    return render_template('auth/register.html', form=form)

"""
User Login if existing
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            connection = get_flask_database_connection(app)
            repository = UserRepository(connection)

            # Try to find user by email
            user = repository.find_by_email(form.email.data)
            
            if user and user.password == form.password.data:
                # Login successful - redirect to user profile
                session["user_id"] = user.id
                return redirect(f"/users/{user.id}")
            else:
                # Login failed
                return render_template('auth/login.html', form=form, error="Invalid email or password")
                
        except Exception as e:
            return render_template('auth/login.html', form=form, error=f"Login failed: {e}")
    
    # If GET request or form validation failed, show the form
    return render_template('auth/login.html', form=form)

"""
Log user logout and redirect to login
"""
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

"""
Redirect old user creation route to new registration
"""
@app.route('/users/new', methods=['GET'])
def get_new_user():
    return redirect('/register')

@app.route('/spaces', methods=['GET'])
# @login_required
def get_spaces():
    space_repository = SpaceRepository(get_flask_database_connection(app))
    spaces = space_repository.all()
    return render_template("spaces/space.html", spaces=spaces)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))