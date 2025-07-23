import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv

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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
