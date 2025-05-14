import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.booking_repository import BookingRepository
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/users', methods=['POST'])
def post_users():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user_name = request.form['user_name']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']

    user = User(None, user_name, email, phone)
    repository.create(user)

@app.route('/spaces/new', methods=['GET'])
def get_list_a_space():
    return render_template('list_a_space.html')


@app.route('/spaces/request/<space_id>', methods=['GET'])
def get_request_space(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)   

    bookings = repository.find_for_space(space_id)
    return render_template('request_a_space.html', space_id = space_id, user_id = 1, bookings = bookings)

@app.route('/spaces/request', methods=['POST'])
def post_request_space():
    space_id = request.form['space_id']
    requested_date = datetime.strptime(request.form['requested_date'], '%Y-%m-%d').date()
    space_name = "SpaceName"
    space_description = "Space description blah blah blah"

    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)   
    booking = Booking(None, request.form['user_id'], space_id, requested_date, 'Requested')
    repository.create(booking)

    requested_date_str = datetime.strftime(requested_date,"%d %B %Y")
    return render_template('space_requested.html', space_id = space_id, space_name = space_name, requested_date_str = requested_date_str )

@app.route('/requests', methods=['GET'])
def get_requests():
    user_id = 1 # TODO: user session stuff!!!

    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)

    bookings_made = repository.find_for_user(user_id)

    return render_template('requests.html', bookings_made = bookings_made)

@app.route('/requests/<id>', methods=['GET'])
def get_request(id):
    user_id = 1 # TODO: user session stuff!!!

    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    user_repo = UserRepository(connection)
    #space_repo = SpacesRepository(connection)

    booking = booking_repo.find(id)
    requesting_user = user_repo.find(booking.user_id)
    #space = space_repo.find(booking.space_id)

    #space_user_id = space.user_id
    space_user_id = 1

    if space_user_id == user_id:
        page_mode = 'approver'
    else:
        page_mode = ''

    return render_template('view_request.html', id=id, page_mode=page_mode, booking=booking, requesting_user=requesting_user)

@app.route('/requests/<id>/<action>', methods=['GET'])
def get_user_request_update(id, action):
    user_id = 1 # TODO: user session stuff!!!

    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    #space_repo = SpacesRepository(connection)

    booking = booking_repo.find(id)
    #space = space_repo.find(booking.space_id)

    #space_user_id = space.user_id
    space_user_id = 1

    if action == 'approve':
        new_status = "Booked"
    if action == 'deny':
        new_status = "Rejected"
    
    if action != None and space_user_id == user_id:
            booking_repo.update_status(id, new_status)
    
    return redirect("/requests")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
