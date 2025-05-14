import os
from lib.space import Space
from lib.space_repository import SpaceRepository
from flask import Flask, request, render_template, redirect
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

    return render_template("home_page.html", spaces=spaces)

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
    
    new_space = space_repo.create(new_space)
    
    return redirect(f'/home_page/{new_space.id}')


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
