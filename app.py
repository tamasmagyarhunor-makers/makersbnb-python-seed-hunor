import os
from flask import Flask, request, redirect, render_template, flash
from flask_login import LoginManager, login_user
from lib.forms import LoginForm
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from dotenv import load_dotenv

# Create a new Flask app
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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
    return redirect('/login')

@app.route('/spaces/new', methods=['GET'])
def get_list_a_space():
    return render_template('list_a_space.html')

# @app.route('/login', methods=['GET'])
# def get_login_page():
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.user_name.data).first()
        login_user(user)
        # Change /index when we know the name of the list of spaces
        return redirect('/index')
    else:
        return render_template('login.html', title='Log In', form=form)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
