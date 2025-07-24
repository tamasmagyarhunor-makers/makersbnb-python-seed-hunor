from playwright.sync_api import Page, expect
import pytest  # Add this import if not already there


@pytest.fixture
def logged_in_session(db_connection, page, test_web_address):
    """Fixture that logs in a user and returns the page"""
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "password1")
    page.click("input[type='submit']")
    return page


"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look at the <p> tag
    p_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(p_tag).to_have_text("This is the homepage.")



"""
Get all the users
"""
def test_get_users(logged_in_session, test_web_address):
    page = logged_in_session
    # We load a virtual browser and navigate to the /books page
    page.goto(f"http://{test_web_address}/users")

    # We look at all the <li> tags
    list_items = page.locator("li")

    # We assert that it has the users in it
    expect(list_items).to_have_text([
        "Alice (alice@example.com)",
        "Bob (bob@example.com)"
    ])


"""
Get a single user
"""
def test_get_user(logged_in_session, test_web_address):  
    page = logged_in_session  

    # We visit the books page
    page.goto(f"http://{test_web_address}/users")

    # Click the link with the text 'Name: Alice Email: alice@example.com'
    page.click("text=Alice (alice@example.com)")

    # The virtual browser acts just like a normal browser and goes to the next
    # page without us having to tell it to.

    # Then we look for specific test classes that we have put into the HTML
    # as targets for our tests to look for. This one is called `t-title`.
    # You can see it in `templates/books/show.html`
    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: Alice")

    # We do the same for the author name
    author_element = page.locator(".t-email")
    expect(author_element).to_have_text("Email: alice@example.com")


"""
When we register a new user (create a new user)
We see their profile page
"""
def test_register_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Navigate directly to the registration page
    page.goto(f"http://{test_web_address}/register")

    # Fill out the registration form
    page.fill("input[name='name']", "Charlie Brown")
    page.fill("input[name='email']", "charlie@example.com")
    page.fill("input[name='password']", "password123")
    page.fill("input[name='confirm_password']", "password123")

    # Submit the form
    page.click("input[type='submit']")


"""
We can render the login page
"""
def test_get_login_page(page, test_web_address):
    # Navigate to the login page
    page.goto(f"http://{test_web_address}/login")

    # Check that we can see the login form
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign In")

    # Check that form fields are present
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("input[type='submit']")).to_be_visible()


"""
When we login with valid credentials
We are redirected to the user's profile page
"""
def test_login_valid_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Navigate to the login page
    page.goto(f"http://{test_web_address}/login")

    # Fill out the login form with valid credentials (from seed data)
    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "password1")

    # Submit the form
    page.click("input[type='submit']")

    # Should be redirected to Alice's profile page
    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: Alice")

    email_element = page.locator(".t-email")
    expect(email_element).to_have_text("Email: alice@example.com")


"""
When we login with invalid email
We see an error message
"""
def test_login_invalid_email(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Navigate to the login page
    page.goto(f"http://{test_web_address}/login")

    # Fill out the login form with non-existent email
    page.fill("input[name='email']", "nonexistent@example.com")
    page.fill("input[name='password']", "password1")

    # Submit the form
    page.click("input[type='submit']")

    # Should stay on login page and show error
    expect(page.locator("h1")).to_have_text("Sign In")
    
    # Should show error message
    error_text = page.locator("text=Invalid email or password")
    expect(error_text).to_be_visible()


"""
When we login with wrong password
We see an error message
"""
def test_login_wrong_password(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Navigate to the login page
    page.goto(f"http://{test_web_address}/login")

    # Fill out the login form with wrong password
    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "wrongpassword")

    # Submit the form
    page.click("input[type='submit']")

    # Should stay on login page and show error
    expect(page.locator("h1")).to_have_text("Sign In")
    
    # Should show error message
    error_text = page.locator("text=Invalid email or password")
    expect(error_text).to_be_visible()


"""
Login form shows validation errors for invalid email format
"""
def test_login_invalid_email_format(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Navigate to the login page
    page.goto(f"http://{test_web_address}/login")

    # Fill out the form with invalid email format
    page.fill("input[name='email']", "not-an-email")
    page.fill("input[name='password']", "password123")

    # Submit the form
    page.click("input[type='submit']")

    # Should stay on login page and show validation error
    expect(page.locator("h1")).to_have_text("Sign In")
    
    # Should show email validation error
    error_text = page.locator("text=Please enter a valid email address")
    expect(error_text).to_be_visible()

"""
When I logout
the user is logged out and redirected to login page 
"""
def test_logout_redirects_to_login(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

    # Step 1: Log in first
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "password1")
    page.click("input[type='submit']")

    # Step 2: Go to /logout
    page.goto(f"http://{test_web_address}/logout")

    # Step 3: You should be redirected to the login page
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign In")

    # Optionally check form is visible again
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()

def test_logout_redirects_to_login(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

    # Step 1: Log in first
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "password1")
    page.click("input[type='submit']")

    # Step 2: Go to /logout
    page.goto(f"http://{test_web_address}/logout")

    # Step 3: You should be redirected to the login page
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign In")

    # Optionally check form is visible again
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()

"""
A login is required to visit a user's profile
"""
def test_protected_profile_requires_login(page, test_web_address):
    # Try to visit a user's profile without logging in
    page.goto(f"http://{test_web_address}/users/1")

    # You should get redirected to the login page
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign In")

"""
When I try to access a user profile without logging in
I am redirected to the login page
"""
def test_login_required_for_user_profile(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    
    # Try to directly access the protected user profile
    page.goto(f"http://{test_web_address}/users/1")

    # Expect to be redirected to the login page
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign In")

    # assert email/password inputs are visible
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()

"""
When I call GET /spaces
I get a list of all the spaces
"""

def test_get_spaces(logged_in_session, test_web_address):  
    page = logged_in_session  
    page.goto(f"http://{test_web_address}/spaces")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("All Spaces")

def test_listings(logged_in_session, test_web_address):  
    page = logged_in_session  
    page.goto(f"http://{test_web_address}/spaces")
    first_listing = page.locator(".listing_1")
    heading = first_listing.locator("h5")
    description = first_listing.locator("p")
    expect(heading).to_have_text("Cozy london flat")
    expect(description).to_have_text("A beautiful 1-bedroom flat in central london")
    div_tag = page.locator("div")
    expect(div_tag).to_have_count(3)


    # assert response.status_code == 200
    # assert "<h1>All Spaces</h1>" in html
    # assert "Cozy london flat" in html
    # assert "£85.0" in html

