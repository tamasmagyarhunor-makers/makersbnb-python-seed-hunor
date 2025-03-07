# Flask Security and Frontend Libraries Documentation

This document provides a concise overview and links to the official documentation for Flask-Login, Flask-WTF, Flask-Bcrypt, and Bootstrap, commonly used in Flask web development.

_Remember to run pip freeze > requirements.txt if you add any of the following to your project: ```flask-login```, ```flask-bcrypt``` or ```flask-wtf```, to update the list of dependencies._

## Flask-Login

* **Description:** Flask-Login provides user session management for Flask. It handles user login, logout, and session persistence.
* **Links:**
    * [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)
    * [Flask-Login on PyPI](https://pypi.org/project/Flask-Login/)
* **Example Implementation:**

    ```python
    from flask import Flask
    from flask_login import LoginManager, UserMixin, login_user

    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)

    class User(UserMixin):
        def __init__(self, id):
            self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/login')
    def login():
        user = User(1)
        login_user(user)
        return 'Logged in'
    ```

## Flask-WTF

* **Description:** Flask-WTF integrates WTForms with Flask, providing form handling and validation. It simplifies form creation and security.
* **Links:**
    * [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/latest/)
    * [Flask-WTF PyPI](https://pypi.org/project/Flask-WTF/)
* **Example Implementation:**

    ```python
    from flask import Flask, render_template, request
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField
    from dotenv import load_dotenv

    load_dotenv()  # Load variables from .env file

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    class MyForm(FlaskForm):
        name = StringField('Name')
        submit = SubmitField('Submit')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = MyForm()
        if form.validate_on_submit():
            return f'Hello, {form.name.data}!'
        return render_template('index.html', form=form)
    ```

    ```python
    # .ENV example
    SECRET_KEY=f8a7e3b9c1d8e5f2
    ```

    ```python
    # .gitignore example. To make sure the .ENV file is never added to your repo
    .ENV
    ```

## Flask-Bcrypt

* **Description:** Flask-Bcrypt provides bcrypt password hashing for Flask. It's used for secure password storage.
* **Links:**
    * [Flask-Bcrypt Documentation](https://flask-bcrypt.readthedocs.io/en/latest/)
    * [Flask-Bcrypt PyPI](https://pypi.org/project/Flask-Bcrypt/)
* **Example Implementation:**

    ```python
    from flask import Flask
    from flask_bcrypt import Bcrypt

    app = Flask(__name__)
    bcrypt = Bcrypt(app)

    password = 'mysecretpassword'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # To check the password
    # if bcrypt.check_password_hash(hashed_password, password):
    #     print("Password matches")
    ```

## Bootstrap

* **Description:** Bootstrap is a popular CSS framework for developing responsive and mobile-first websites. It provides pre-built CSS and JavaScript components for easy web development.
* **Links:**
    * [Bootstrap Documentation](https://getbootstrap.com/)
    * [Bootstrap GitHub](https://github.com/twbs/bootstrap)
* **Usage in Flask:**
    * Include Bootstrap CSS and JavaScript files in your HTML templates.
    * Use Bootstrap classes to style your HTML elements.
    * Example using CDN links inside your HTML `<head>` tag.
    ```html
    <link rel="stylesheet" href="[https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css)">
    <script src="[https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js)"></script>
    ```
    * Or, download the files and include them locally.
* **Bootstrap Login Form (MUI-like):**

    Here's an example of a Bootstrap login form that aims to mimic the clean, minimalist style of Material UI (MUI).

    <img src="example_bootstrap_login_form.png" alt="Login form with bootstrap" style="width: 65%;">


    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <link rel="stylesheet" href="[https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css)">
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f8f9fa; /* Light background */
            }
            .form-container {
                width: 350px;
                padding: 30px;
                background-color: #ffffff; /* White form background */
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            }
            .form-group label {
              font-weight: 500;
              margin-bottom: 5px;
            }
            .form-control{
              border-radius: 6px;
              padding: 10px;
              border: 1px solid #ced4da;
            }
            .btn-primary{
              width: 100%;
              padding: 12px;
              border-radius: 6px;
              background-color: #007bff;
              border: none;
            }
            .btn-primary:hover{
              background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2 class="text-center mb-4">Login</h2>
            <form>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" class="form-control" id="username" placeholder="Enter username">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" class="form-control" id="password" placeholder="Enter password">
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
        </div>
        <script src="[https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js](https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js)"></script>
    </body>
    </html>
    ```

