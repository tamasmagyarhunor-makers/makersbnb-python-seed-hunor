import os
from lib.space import Space
from lib.space_repository import SpaceRepository
from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for
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


@app.route('/home_page', methods=['GET'])
def get_spaces():

    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    spaces = repository.all()

    return render_template("home_page.html", spaces=spaces)


@app.route('/sign_up', methods=['GET', 'POST']) # can do getting page and posting to it in one
def sign_up():

    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST':
        email = request.form.get("email_address") # getting the info from the forms
        name = request.form.get("name")
        password = request.form.get("password")
        # user = User()

        if not email or not name or not password:
            error = "Please fill in all the fields"
            return render_template("sign_up.html", error=error)
        
        # all_users = repository.all()
        # if any(email == user.email_address for user in all_users):
        #     error = "A user with this email address already exists"
        #     return render_template("sign_up.html", error=error)

        repository.create(name, password, email)
        return redirect(url_for('sign_up_successful')) # redirecting to route below
    
    return render_template("sign_up.html")

@app.route('/sign_up_confirmation', methods=['GET'])
def sign_up_successful():

    connection = get_flask_database_connection(app)
    return render_template("sign_up_confirmation.html")

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
