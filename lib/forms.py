from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    """
    Registration form for new users
    Flask-WTF automatically handles CSRF (Cross-Site Request Forgery) protection and validation - keeping forms secure
    """


    name = StringField(
        'Full Name',
        validators=[DataRequired(message="Name is required")],
        render_kw={"placeholder": "Enter your full name"}
    )

    # Email field with validation
    email = StringField(
        'Email Address', # Label that appears on the form
        validators=[
            DataRequired(message="Email is required"), # Field cannot be empty
            Email(message="Please enter a valid email address") # Must be a valid email format
        ],
        render_kw={"placeholder": "Enter your email address"} # HTML placeholder text
    )

    # Password field with validation
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long")  # Minimum length
        ],
        render_kw={"placeholder": "Enter your password"}
    )

    # Confirm password field - must match the password field
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message='Passwords must match')  # Must equal the 'password' field
        ],
        render_kw={"placeholder": "Confirm your password"}
    )

    # Submit button
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    """
    Login form for existing users
    """
    
    # Email field
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address")
        ],
        render_kw={"placeholder": "Enter your email address"}
    )

    # Password field
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required")
        ],
        render_kw={"placeholder": "Enter your password"}
    )

    # Submit button
    submit = SubmitField('Sign In')