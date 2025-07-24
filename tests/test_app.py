from playwright.sync_api import Page, expect

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
Get all the availabilities
"""
def test_get_availabilities(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

    # We load a virtual browser and navigate to the /books page
    page.goto(f"http://{test_web_address}/spaces/availability")

    # We look at all the <li> tags
    list_items = page.locator("li")

    # We assert that it has the avais in it
    expect(list_items).to_have_text([
        "Space 1: 2025-07-24 to 2025-08-24",
        "Space 1: 2025-09-30 to 2025-12-20",
        "Space 2: 2025-07-24 to 2025-09-30",
        "Space 3: 2025-07-24 to 2025-12-31"
    ])

"""
When we create a new availability
We see it in the availability index
"""
def test_create_availability(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces/availability")

    # add a new availability
    page.click("text=Add a new availability")

    page.fill("input[name='space_id']", "2")
    page.fill("input[name='available_from']", "2025-10-10")
    page.fill("input[name='available_to']", "2025-11-11")


    # Finally we click the button with the text 'Create Book'
    page.click("text=Create Availability")

    # Just as before, the virtual browser acts just like a normal browser and
    # goes to the next page without us having to tell it to.

    space_id_element = page.locator(".t-space-id")
    expect(space_id_element).to_have_text("Space ID: 2")

    from_element = page.locator(".t-available-from")
    expect(from_element).to_have_text("Available from: 2025-10-10")

    to_element = page.locator(".t-available-to")
    expect(to_element).to_have_text("Available to: 2025-11-11")


    
"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/index")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("Find your perfect space or list your own")


"""
Get all the users
"""
def test_get_users(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

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
def test_get_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

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

    # Check we're redirected to the user's profile
    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: Charlie Brown")

    email_element = page.locator(".t-email")
    expect(email_element).to_have_text("Email: charlie@example.com")

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
When I call GET /spaces
I get a list of all the spaces
"""

def test_get_spaces(db_connection, test_web_address, page):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("All Spaces")

def test_listings(db_connection, test_web_address, page):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    first_listing = page.locator(".listing_1")
    heading = first_listing.locator("h5")
    description = first_listing.locator("p")
    expect(heading).to_have_text("Cozy london flat")
    expect(description).to_have_text("A beautiful 1-bedroom flat in central london")
    div_tag = page.locator("div")
    expect(div_tag).to_have_count(3)

def test_create_space(db_connection, test_web_address, page):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces/new")
    # Fill out the form with invalid email format
    page.fill("input[name='name']", "Not Cozy")
    page.fill("input[name='description']", "Description")
    page.fill("input[name='price_per_night']", "30000.00")
    page.fill("input[name='user_id']", "2")
    
    # Submit the form
    page.click("input[type='submit']")
    
    new_listing = page.locator(".listing_4")
    heading = new_listing.locator("h5")
    description = new_listing.locator("p")
    expect(heading).to_have_text("Not Cozy")
    expect(description).to_have_text("Description")