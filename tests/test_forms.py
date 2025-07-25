from lib.forms import RegistrationForm, SpaceForm
import pytest
from app import app

@pytest.fixture(autouse=True)
def app_context():
    """
    Pytest fixture - automatically provides Flask application context (solves RuntimeError: Working outside of application context bug )
    autouse=True means this runs automatically for every test in this file (DRY code - instead off adding context to each test)
    """
    with app.app_context():  # Application context (access to app.config)
        with app.test_request_context():  # Request context (simulates web request) --> needed for  RuntimeError: Working outside of request context bug.
            yield  # This is where the test runs
    # Both contexts automatically close after the test


"""
Test that RegistrationForm validates correctly with valid data
"""

def test_registration_form_valid_data():
    # create form data (simulating user exp when interacting with a web form)
    form_data = {
        "name": "John Doe",  
        "email": "test@example.com",
        "password": "password123",
        "confirm_password": "password123",
    }
    # Create the form with our test data
    form = RegistrationForm(data=form_data)
    
    # CSRF enabled by default in FLask-WTF - to avoid unit test errors - Manually setting a valid CSRF token as not testing CSRF functionality in form_data
    form.csrf_token.data = form.csrf_token.current_token
    
    # The form should be valid
    assert form.validate() == True
    
    # Check that we can access the data
    assert form.name.data == 'John Doe'
    assert form.email.data == 'test@example.com'
    assert form.password.data == 'password123'

"""
Test that RegistrationForm rejects invalid email
"""
def test_registration_form_invalid_email():
    form_data = {
        'name': 'John Doe',
        'email': 'not-an-email',  # Invalid email format
        'password': 'password123',
        'confirm_password': 'password123',
    }
    
    form = RegistrationForm(data=form_data)
    form.csrf_token.data = form.csrf_token.current_token
    
    # Form should be invalid
    assert form.validate() == False
    # print(form.email.errors)

    # Should have an error on the email field
    assert 'Please enter a valid email address' in form.email.errors

"""
Test that RegistrationForm rejects mismatched passwords
"""
def test_registration_form_password_mismatch():
    form_data = {
        'name': 'John Doe',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'different_password',  # Passwords don't match
    }
    
    form = RegistrationForm(data=form_data)
    form.csrf_token.data = form.csrf_token.current_token
    
    # Form should be invalid
    assert form.validate() == False
    
    # Should have an error on the confirm_password field
    assert 'Passwords must match' in form.confirm_password.errors

"""
Test that RegistrationForm rejects missing name
"""

def test_registration_form_missing_name():
    form_data = {
        'name': '',  # Empty name
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }
    
    form = RegistrationForm(data=form_data)
    form.csrf_token.data = form.csrf_token.current_token
    
    # Form should be invalid
    assert form.validate() == False
    
    # Should have an error on the name field
    assert 'Name is required' in form.name.errors

def test_new_space_form():
    # create space form data (simulating user exp when interacting with a web form)
    form_data = {
        "name": "Cozy london flat",  
        "description": "A beautiful 1-bedroom flat in central london",
        "price_per_night": 85.00,
    }
    # Create the form with our test data
    form = SpaceForm(data=form_data)
    
    # CSRF enabled by default in FLask-WTF - to avoid unit test errors - Manually setting a valid CSRF token as not testing CSRF functionality in form_data
    form.csrf_token.data = form.csrf_token.current_token
    
    # The form should be valid
    assert form.validate() == True
    
    # Check that we can access the data
    assert form.name.data == "Cozy london flat"
    assert form.description.data == "A beautiful 1-bedroom flat in central london"
    assert form.price_per_night.data == 85.00
