import os
from flask import Flask, request, render_template, redirect
from lib.space import Space
from lib.space_repository import SpaceRepository

from lib.user import User
from lib.user_repository import UserRepository
from flask import Flask, request, render_template, redirect, url_for, session

from lib.database_connection import get_flask_database_connection
from werkzeug.security import generate_password_hash # use for password hashing


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
    # print(session['user_id'])

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

        if user and user.password == password:
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
    spaces = repository.all()
    return render_template("userhome.html", spaces=spaces)

# route for log out
@app.route('/logout')
def logout():
    session.clear() #session is cleared
    return redirect((url_for("login")))

@app.route("/debug_session")
def debug_session():
    return f"Current session data: {session}"


# routes related to spaces
@app.route('/userhome/<int:id>/edit', methods=['GET','POST'])
def edit_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price_per_night']
        host_id = session["user_id"]

        updated_space = Space(id=id,
                            name=name,
                            description=description,
                            price_per_night=price,
                            host_id=host_id)

        repository.update(updated_space)

        return redirect(url_for('userhome'))

    space = repository.find_by_id(id)
    return render_template('edit_space.html', space=space)


@app.route('/home/<int:id>', methods=['GET'])
def get_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find_by_id(id)
    return render_template('show_space.html', space=space)

@app.route('/home/add-space', methods=['GET'])
def get_new_space():
    return render_template('add_property.html')

@app.route('/home', methods=['POST'])
def create_new_space():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)

    name = request.form['name']
    description = request.form['description']
    price = request.form['price_per_night']
    image_url = request.form['imageUrl']
    host_id = session['user_id']

    new_space = Space(None, name, description, price, image_url, host_id)

    if not new_space.is_valid():
        return render_template('add_property.html', space=new_space, errors=new_space.generate_errors()), 400

    space_repo.create(new_space)

    return redirect(f'/home/{new_space.id}')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
