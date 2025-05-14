import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository 
from lib.listing import Listing

# Create a new Flask app
app = Flask(__name__, static_folder='static')

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
    listing = repository.find_by_id(listing_id)  # You need to define this method
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
        print(image)
        connection = get_flask_database_connection(app)
        repository = ListingRepository(connection)
        listing = Listing(id=None, name=name, description=description, price=price, user_id=user_id)
        repository.create_listing(listing)
        return redirect(url_for('get_all_listings'))





# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
