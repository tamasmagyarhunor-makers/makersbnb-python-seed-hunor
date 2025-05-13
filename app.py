import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection

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

<<<<<<< HEAD
@app.route('/home')
def get_home():
    return render_template('home.html')

@app.route('/login')
def get_login():
    return render_template('login.html')

@app.route('/signup')
def get_signup():
    return render_template('signup.html')
=======

>>>>>>> make-a-listing

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
