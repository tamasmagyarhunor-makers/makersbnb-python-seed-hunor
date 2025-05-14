import os
from lib.space import Space
from lib.space_repository import SpaceRepository
from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for, session
from lib.database_connection import get_flask_database_connection
from werkzeug.security import generate_password_hash

# Create a new Flask app
app = Flask(__name__)
app.secret_key = "jmns_secretkey"



# == Your Routes Here ==

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

# routes for showing sign up page AND submitting sign up form
@app.route('/sign_up', methods=['GET', 'POST']) # can do getting page and posting to it in one
def sign_up():

    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST':
        email = request.form.get("email_address") # getting the info from the forms
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

        repository.create(name, password, email)
        return redirect(url_for('sign_up_successful')) # redirecting to route below
    
    return render_template("sign_up.html")

# route for showing sign up confirmation page
@app.route('/sign_up_confirmation', methods=['GET'])
def sign_up_successful():
    return render_template("sign_up_confirmation.html")

# route for showing login page and logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if request.method == 'POST':
        email = request.form.get("email_address")
        password = request.form.get("password")

        user = repository.find_by_email(email)

        if user and user.password == password:
            session["user_id"] = user.id
            return redirect(url_for("userhome"))
        else:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
    
    return render_template("login.html")

# route for user home (account page)
@app.route('/userhome', methods=['GET'])
def userhome():
    if "user_id" not in session:
        return redirect((url_for("login")))
    return render_template("userhome.html")

# log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect((url_for("login")))


#_____________________________________
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
