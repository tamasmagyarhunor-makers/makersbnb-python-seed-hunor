import os
from flask import Flask, request, render_template, redirect
from lib.space import Space
from lib.space_repository import SpaceRepository

from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for, session

from lib.booking_requests import BookingRequest
from lib.booking_request_repository import BookingRequestRepository

from lib.availability_range_repository import AvailabilityRangeRepository

from lib.database_connection import get_flask_database_connection
from werkzeug.security import generate_password_hash # use for password hashing

from lib.password_hashing_and_validation import *


app = Flask(__name__)
app.secret_key = os.urandom(24) #this creates a random secret key, needed for sessions

# route to open the home page http://localhost:5001/home
@app.route('/home', methods=['GET'])
def get_spaces():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    if "user_id" in session:
        return redirect((url_for("get_logged_in_homepage")))

    spaces = repository.all()
    return render_template("home.html", spaces=spaces)

@app.route('/logged_in_homepage', methods=['GET'])
def get_logged_in_homepage():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()

    if "user_id" not in session:
        return redirect((url_for("login")))

    return render_template('logged_in_homepage.html', spaces=spaces)

# routes for showing sign up page AND submitting sign up form
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST':
        email = request.form.get("email_address")
        name = request.form.get("name")
        password = request.form.get("password")

        if not email or not name or not password:
            error = "Please fill in all the fields"
            return render_template("sign_up.html", error=error)

        all_users = repository.all()

        if any([user.email_address == email for user in all_users]): 
            error = "A user with this email address already exists"
            return render_template("sign_up.html", error=error)

        #hashed_password = generate_password_hash(password)
        new_user = User(None, name, password, email)
        repository.create(new_user)
        session['user_id'] = new_user.id
        print(session['user_id'])
        return redirect(url_for('sign_up_successful'))

    return render_template("sign_up.html")

# route for showing sign up confirmation page
@app.route('/sign_up_confirmation', methods=['GET'])
def sign_up_successful():
    return render_template("sign_up_confirmation.html")

# route for GET login page and POST logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST':
        email = request.form.get("email_address")
        password = request.form.get("password")

        user = repository.find_by_email(email)
        
        if not user:
            error = "Invalid email or password" 
            return render_template("login.html", error=error)
        
        validation = check_password(password,user.password)

        if user and validation:
            session["user_id"] = user.id
            return redirect(url_for("userhome"))
        elif not email or not password:
            #NOTE: this currently has the below error message even with values '0' across fields, perhaps replace with please enter valid inputs
            error = "Please fill in all the fields" 
            return render_template("login.html", error=error)
        else:
            error = "Invalid email or password" 
            return render_template("login.html", error=error)

    return render_template("login.html")

# route for user home (account page)
@app.route('/userhome', methods=['GET'])
def userhome():
    if "user_id" not in session:
        return redirect((url_for("login")))
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    user_spaces = [space for space in repository.all() if space.host_id == session["user_id"]]
    return render_template("userhome.html", spaces=user_spaces, has_properties=bool(user_spaces))

# route for log out
@app.route('/logout')
def logout():
    session.clear() #session is cleared
    return redirect((url_for("login")))

@app.route("/debug_session")
def debug_session():
    return f"Current session data: {session}"
    
@app.route('/userhome/<int:id>/edit', methods=['GET','POST'])
def edit_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find_by_id(id)

    if "user_id" not in session:
        return redirect((url_for("login")))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price_per_night']
        image_url = space.image_url
        host_id = session["user_id"]
        image_url = request.form["image_url"]
        start_date = request.form["availability_start_date"]
        end_date = request.form["availability_end_date"]

        updated_space = Space(id=id,
                            name=name,
                            description=description,
                            price_per_night=price,
                            image_url=image_url,
                            host_id=host_id)

        repository.update(updated_space)

        availabilityrepository = AvailabilityRangeRepository(connection)
        # # Dates need to be turned into correct format
        availabilityrepository.add_range(start_date,end_date,updated_space.id)

        return redirect(url_for('userhome'))

    space = repository.find_by_id(id)
    return render_template('edit_space.html', space=space)

#_____________________________________

@app.route('/home/<int:id>', methods=['GET'])
def get_edited_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price_per_night']
        image_url = request.form['image_Url']
        host_id = session["user_id"]

        updated_space = Space(id=id,
                            name=name,
                            description=description,
                            price_per_night=price,
                            image_url=image_url,
                            host_id=host_id)

        repository.update(updated_space)

        return redirect(url_for('userhome'))

    space = repository.find_by_id(id)
    return render_template('edit_space.html', space=space)

@app.route('/home/add-space', methods=['GET'])
def get_new_space():

    if "user_id" not in session:
        return redirect((url_for("login")))
    
    return render_template('add_property.html')

@app.route('/home', methods=['POST'])
def create_new_space():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)

    if "user_id" not in session:
        return redirect((url_for("login")))

    name = request.form['name']
    description = request.form['description']
    price = request.form['price_per_night']
    image_url = request.form['image_url']
    host_id = session['user_id']

    new_space = Space(None, name, description, price, image_url, host_id)

    if not new_space.is_valid():
        return render_template('add_property.html', space=new_space, errors=new_space.generate_errors()), 400

    space_repo.create(new_space)
    
    return redirect(f'/spaces/{new_space.id}')


# Route to return a single space, including booked days, and populate calendar - SASHA
@app.route('/spaces/<space_id>', methods=['GET'])
def get_space(space_id):
    connection = get_flask_database_connection(app)
    
    if "user_id" not in session:
        return redirect((url_for("login")))

    space_repo = SpaceRepository(connection)
    space = space_repo.find_by_id(space_id) #finds individual space using space id

    available_days = space_repo.available_days_by_id(space_id) #uses available_days method to find host-selected available days for this space id
    occupied_dates = space_repo.booked_days_by_id(space_id) #as above but finds occupied days by checking bookings

    if available_days:
        selectable_start = available_days[0]
        selectable_end = available_days[-1]
    else:
        selectable_start = "2025-01-01"  # Or a default value
        selectable_end = "2025-12-12"  # Or a default value

    occupied_dates_dicts = [{"startDate": d, "endDate": d} for d in occupied_dates] #translates all individual occupied dates to dictionary format, to be passed to Javascript for the calendar

    # return statement brings all space details, plus the available range defined by first and last dates in 'available days' list, as well as a list of dicts for all occupied dates - all fed into calendar JS and marked on calendar
    return render_template('show_space.html', space=space, selectable_start=selectable_start, selectable_end=selectable_end, occupied_dates=occupied_dates_dicts) 

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
