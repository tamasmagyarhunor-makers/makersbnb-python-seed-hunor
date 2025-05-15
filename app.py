import os
from flask import Flask, request, render_template, redirect
from lib.space import Space
from lib.space_repository import SpaceRepository

from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for, session

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

@app.route('/home_page/<int:id>', methods=['GET'])
def get_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find_by_id(id)
    return render_template('show_space.html', space=space)

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



# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
