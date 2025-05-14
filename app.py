import os
from flask import Flask, request, render_template, redirect, url_for, flash
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository 
from lib.listing import Listing
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


# Create a new Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/home')
def get_home():
    return render_template('home.html')

@app.route('/login')
def get_login():
    return render_template('login.html')

@app.route('/signup')
def get_signup():
    return render_template('signup.html')

@app.route('/listings', methods=['GET'])
def get_all_listings():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all_listings()
    return render_template('listings.html', listings=listings)

@app.route('/find/<int:listing_id>', methods=['GET'])
def find_listing_by_id(listing_id):
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listing = repository.find_by_id(listing_id) 
    return render_template('listing.html', listing=listing)

@app.route('/new-listing')
def get_to_new_listing():
        return render_template('newlisting.html')

@app.route('/create-listing', methods=['POST'])
def create_listing():
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']
        user_id = 1
        if image:
            filename = secure_filename(image.filename)
            upload_path = os.path.join(app.static_folder, 'uploads', filename)
            image.save(upload_path)
        else:
            filename = None
        connection = get_flask_database_connection(app)
        repository = ListingRepository(connection)
        listing = Listing(id=None, name=name, description=description, price=price, image=filename, user_id=user_id)
        repository.create_listing(listing)
        return redirect(url_for('get_all_listings'))

@app.route('/requests', methods=['GET'])
def get_requests():
    return render_template('requests.html')


@app.route('/listing/<int:listing_id>', methods=['GET'])
def show_listing_with_calendar(listing_id):
    connection = get_flask_database_connection(app)
    repo = ListingRepository(connection)
    listing = repo.find_by_id(listing_id)
    if not listing:
        flash("Listing not found.")
        return redirect('/listings')
    # Convert the disabled dates to strings for proper serialization
    disabled_dates = repo.get_booked_dates(listing_id)
    return render_template('listing.html', listing=listing, disabled_dates=disabled_dates)

@app.route('/book', methods=['POST'])
def book_listing():
    listing_id = int(request.form['listing_id'])
    date_range = request.form['date_range']
    try:
        start_str, end_str = date_range.split(" to ")
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.")
        return redirect(f"/listing/{listing_id}")
    repo = ListingRepository(get_flask_database_connection(app))
    if not repo.create_booking(listing_id, start_date, end_date):
        flash(":x: Those dates are already booked.")
    else:
        flash(":white_tick: Booking successful!")
    return redirect(f"/listing/{listing_id}")

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
