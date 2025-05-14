import os
import requests
from lib.space import Space
from lib.space_repository import SpaceRepository
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection

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

# @app.route('/home_page', methods=['GET'])
# def get_homepage():
#     return render_template('home_page.html')

@app.route('/home_page', methods=['GET'])
def get_spaces():

    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    spaces = repository.all()
    # image_url = get_random_image()

    return render_template("home_page.html", spaces=spaces)

def get_random_image():
    headers = {'Accept-Version': 'v1'}
    res = requests.get("https://api.unsplash.com/photos/random", headers=headers)
    data = res.json()
    print(res.status_code)
    print(res.json())

    return data['urls']['small']

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
