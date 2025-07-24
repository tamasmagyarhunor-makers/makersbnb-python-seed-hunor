import os
from flask import Flask, request, render_template, redirect
from datetime import datetime
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from lib.user import *
from lib.user_repository import *
from lib.forms import *
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.availability import *
from lib.availability_repository import *
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

#new code below
"""
get all availabilities
"""
@app.route('/spaces/availability', methods=['GET'])
def get_all_availabilities():
    try:
        connection = get_flask_database_connection(app)
        repository = AvailabilityRepository(connection)
        availability = repository.all()
        return render_template('/spaces/availability/index.html', availabilities=availability)
    except Exception as e:
        return f"Database error: {e}"

"""
get availability by availability_id
"""
@app.route('/spaces/availability/<int:id>', methods=['GET'])
def show_availability_by_availability_id(id):
    connection = get_flask_database_connection(app)
    repository = AvailabilityRepository(connection)
    availabilities = repository.find_by_id(id)
    availability = availabilities[0]
    return render_template('spaces/availability/show.html', availability=availability)

"""
get availability by space_id
"""


"""
create a new availability"""
# GET /availability/new
# Returns a form to create a new availability
@app.route('/spaces/availability/new', methods=['GET'])
def get_new_availability():
    return render_template('/spaces/availability/new.html')

# POST /availability
# Creates a new availability
@app.route('/spaces/availability', methods=['POST'])
def create_availability():
    connection = get_flask_database_connection(app)
    repository = AvailabilityRepository(connection)

    space_id = int(request.form['space_id'])
    # parse ISO 'YYYY-MM-DD' into date
    available_from = datetime.strptime(request.form['available_from'], '%Y-%m-%d').date()
    available_to   = datetime.strptime(request.form['available_to'],   '%Y-%m-%d').date()

    availability = Availability(None, space_id, available_from, available_to)
    if not availability.is_valid():
        return render_template('spaces/availability/new.html', availability=availability, errors=availability.generate_errors()), 400

    availability = repository.create(availability)
    return redirect(f"/spaces/availability/{availability.id}")



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
                return redirect(f"/users/{user.id}")
            else:
                # Login failed
                return render_template('auth/login.html', form=form, error="Invalid email or password")
                
        except Exception as e:
            return render_template('auth/login.html', form=form, error=f"Login failed: {e}")
    
    # If GET request or form validation failed, show the form
    return render_template('auth/login.html', form=form)

"""
Redirect old user creation route to new registration
"""
@app.route('/users/new', methods=['GET'])
def get_new_user():
    return redirect('/register')

"""
Spaces routes
"""

@app.route('/spaces', methods=['GET'])
def get_spaces():
    space_repository = SpaceRepository(get_flask_database_connection(app))
    spaces = space_repository.all()
    return render_template("spaces/space.html", spaces=spaces)

@app.route('/spaces/new', methods=['GET', 'POST'])
def get_new_spaces():
    form = SpaceForm()
    
    if form.validate_on_submit():
            connection = get_flask_database_connection(app)
            repository = SpaceRepository(connection)

            space = Space(None, form.name.data, 
            form.description.data, 
            form.price_per_night.data, 
            form.user_id.data)

            repository.create(space)
            return redirect('/spaces')
    
    # If GET request or form validation failed, show the form
    return render_template('spaces/new.html', form=form)





# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))