import os
from flask import Flask, request, render_template, redirect
from lib.space import Space
from lib.space_repository import SpaceRepository

from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for, session

from lib.booking_requests import BookingRequest
from lib.booking_request_repository import BookingRequestRepository

from lib.database_connection import get_flask_database_connection
from werkzeug.security import generate_password_hash # use for password hashing

# Create a new Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24) #this creates a random secret key, needed for sessions

#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# route to open the home page http://localhost:5001/home_page
@app.route('/home_page', methods=['GET'])
def get_spaces():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    if "user_id" in session: #if the user is logged in
        return redirect((url_for("get_logged_in_homepage"))) #redirect to home page for logged in users

    spaces = repository.all()
    return render_template("home_page.html", spaces=spaces)

@app.route('/logged_in_homepage', methods=['GET'])
def get_logged_in_homepage():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()

    if "user_id" not in session: #if the user is not logged in
        return redirect((url_for("login"))) #prompt them to login

    return render_template('logged_in_homepage.html', spaces=spaces)

# routes for showing sign up page AND submitting sign up form
@app.route('/sign_up', methods=['GET', 'POST']) # can do getting page and posting to it in one
def sign_up():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST': # if filling in the form...
        email = request.form.get("email_address") # getting the info from the forms
        name = request.form.get("name") # quotes must match html name
        password = request.form.get("password")

        if not email or not name or not password: # if these are invalid values (0, "", None)
            error = "Please fill in all the fields" # error message
            return render_template("sign_up.html", error=error)
        
        all_users = repository.all()
        #if any of the email addresses in all_users match the given email
        if any([user.email_address == email for user in all_users]): 
            error = "A user with this email address already exists"
            return render_template("sign_up.html", error=error)

        #hashed_password = generate_password_hash(password)

        repository.create(name, password, email) # creating new user
        return redirect(url_for('sign_up_successful')) # redirecting to sign up confirmation route below
    
    return render_template("sign_up.html") # getting sign up page

# route for showing sign up confirmation page
@app.route('/sign_up_confirmation', methods=['GET'])
def sign_up_successful():
    return render_template("sign_up_confirmation.html")

# route for GET login page and POST logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST': # if logging in
        email = request.form.get("email_address")
        password = request.form.get("password")

        user = repository.find_by_email(email) #finding the user by their email

        if user and user.password == password: #if a user exists and the password is the same...
            session["user_id"] = user.id #a session is created with their user id
            return redirect(url_for("userhome")) #and the user is redirected to their user homepage
        elif not email or not password: #if either the email or password is incomplete
            #NOTE: this currently has the below error message even with values '0' across fields, perhaps replace with please enter valid inputs
            error = "Please fill in all the fields" #request to fill in fields
            return render_template("login.html", error=error)
        else:
            error = "Invalid email or password" #if the email or the password is wrong
            return render_template("login.html", error=error)
    
    return render_template("login.html") #GETS login page

# route for user home (account page)
@app.route('/userhome', methods=['GET'])
def userhome():
    if "user_id" not in session: #if the user is not logged in
        return redirect((url_for("login"))) #prompt them to login
    return render_template("userhome.html") #otherwise send to user home

# route for log out
@app.route('/logout')
def logout():
    session.clear() #session is cleared
    return redirect((url_for("login"))) #sent to login page, can change to home page

# debugging route -> if log in doesn't redirect, run this after logging in. If 
#                    session shows as empty, there's a problem with browser cookies,
#                    try run in incognito window instead. #TODO: this probably needs fixing proper
@app.route("/debug_session")
def debug_session():
    return f"Current session data: {session}"

#_____________________________________

# @app.route('/home_page/<int:id>', methods=['GET'])
# def get_space(id):
#     connection = get_flask_database_connection(app)
#     repository = SpaceRepository(connection)
#     space = repository.find_by_id(id)
#     return render_template('show_space.html', space=space)

@app.route('/home_page/add-space', methods=['GET'])
def get_new_space():
    return render_template('add_property.html')

@app.route('/home_page', methods=['POST'])
def create_new_space():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    
    name = request.form['name']
    description = request.form['description']
    price = request.form['price_per_night']
    host_id = 2 # TODO: Replace with session['user_id'] or something once login is implemented [fixme]
    
    new_space = Space(None, name, description, price, host_id)
    
    if not new_space.is_valid():
        return render_template('add_property.html', space=new_space, errors=new_space.generate_errors()), 400
    
    space_repo.create(new_space)
    
    return redirect(f'/home_page/{new_space.id}')

# Route to return a single space, including booked days, and populate calendar - SASHA
@app.route('/spaces/<space_id>', methods=['GET'])
def get_space(space_id):
    connection = get_flask_database_connection(app)

    space_repo = SpaceRepository(connection)
    space = space_repo.find_by_id(space_id) #finds individual space using space id

    available_days = space_repo.available_days_by_id(space_id) #uses available_days method to find host-selected available days for this space id
    occupied_dates = space_repo.booked_days_by_id(space_id) #as above but finds occupied days by checking bookings

    occupied_dates_dicts = [{"startDate": d, "endDate": d} for d in occupied_dates] #translates all individual occupied dates to dictionary format, to be passed to Javascript for the calendar

    # return statement brings all space details, plus the available range defined by first and last dates in 'available days' list, as well as a list of dicts for all occupied dates - all fed into calendar JS and marked on calendar
    return render_template('show_space.html', space=space, selectable_start=available_days[0], selectable_end=available_days[-1], occupied_dates=occupied_dates_dicts) 

# Route to make a booking request - SASHA

@app.route('/spaces/<space_id>', methods=['POST'])
def make_booking_request(space_id):
    connection = get_flask_database_connection(app)
    booking_request_repo = BookingRequestRepository(connection)

    # NEEDS CHECKING THAT IT WORKS
    if "user_id" not in session: #if the user is not logged in
        return redirect((url_for("login"))) #prompt them to login

    # Get form data from calendar input
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    user_id = session.get('user_id')  # Use session user_id for user id

    # NEEDS SORTING
    if not start_date or not end_date:
        error = "Please select both a start and end date."
        return redirect((url_for("logged_in_homepage")))

    # Add booking request to the database
    booking_request = booking_request_repo.add_booking_request(start_date, end_date, space_id, user_id)

    # Show confirmation page with booking details
    return render_template('booking_request_confirmation.html', booking_request=booking_request)

# Route to return a list of properties based on selected dates - SASHA

@app.route('/search_by_dates', methods=['POST'])
def search_by_dates():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    # Takes date input from the calendar
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not start_date or not end_date:
        error = "Please select both a start and end date."
        return redirect((url_for("get_logged_in_homepage")))

    spaces = repository.get_available_unbooked_spaces(start_date, end_date) # uses the get available unbooked spaces method to filter for spaces available between the start and end date
    return render_template("property_search.html", spaces=spaces, start_date=start_date, end_date=end_date) # renders to HTML showing list of available properties

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
