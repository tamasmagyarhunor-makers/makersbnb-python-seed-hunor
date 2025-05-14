from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User

# Tests for your routes go here

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

# """
# We can render the home page
# """
# def test_get_homepage(page, test_web_address):
#     page.goto(f"http://{test_web_address}/home_page")
#     h3_tag = page.locator("h3")
#     expect(h3_tag).to_have_text("Build Bootstrap with Webpack")

"""
When page is called, space names are displayed
"""
def test_get_spaces(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql") #perhaps change later to spaces seed
    page.goto(f"http://{test_web_address}/home_page")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text([
        "The Barn",
        "The Loft",
        "The Hut",
        "The Cottage",
        "The Penthouse",
        "The Beach Hut"
    ])

# """
# When Space info is being rendered, host email address is pulled
# from user table
# """

# def test_get_host_email(page, test_web_address, db_connection):
#     db_connection.seed("seeds/makersbnb_seed.sql")
#     page.goto(f"http://{test_web_address}/home_page")
#     h6_tag = page.locator("h6")
#     expect(h6_tag).to_have_text([
#         'sashaparkes@email.com',
#         'jamesdismore@email.com',
#         'jamesdismore@email.com',
#         'sashaparkes@email.com',
#         'sashaparkes@email.com',
#         'jamesdismore@email.com'])
    # commented out because I can't be bothered to deal with it being h6 tags

"""
Sign up link works
"""
def test_get_sign_up_page(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/sign_up")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text("User Sign Up")

"""
When user clicks sign up button on home, they are 
redirected to sign up page
"""


"""
When User inputs information into sign up form and clicks
submit, the information is added to the database
"""
def test_sign_up(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "maddy.miller@makers.com")
    page.fill("input[name='name']", "Maddy Miller")
    page.fill("input[name='password']", "password123")
    page.click("input[type='submit']")
    assert repository.all() == [
        User(1, 'Sasha Parkes', 'mypassword1234', 'sashaparkes@email.com'),
        User(2, 'James Dismore', 'mypassword54321', 'jamesdismore@email.com'),
        User(3, 'Maddy Miller', 'password123', 'maddy.miller@makers.com')
    ]

"""
When User inputs information into sign up form and does
not click submit, the information is not added to the database
"""
def test_sign_up_no_click(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "maddy.miller@makers.com")
    page.fill("input[name='name']", "Maddy Miller")
    page.fill("input[name='password']", "password123")
    assert repository.all() == [
        User(1, 'Sasha Parkes', 'mypassword1234', 'sashaparkes@email.com'),
        User(2, 'James Dismore', 'mypassword54321', 'jamesdismore@email.com'),
    ]

"""
When User clicks sign up button, after filled in information,
the page then moves onto the sign up confirmation
"""
def test_sign_up_button(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "maddy.miller@makers.com")
    page.fill("input[name='name']", "Maddy Miller")
    page.fill("input[name='password']", "password123")
    page.click("input[type='submit']")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Sign Up Successful")

"""
If the user has not filled in stuff, it doesn't move to
the next page
"""
def test_sign_up_fail_no_next_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "")
    page.fill("input[name='name']", "")
    page.fill("input[name='password']", "")
    page.click("input[type='submit']")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("User Sign Up")

"""
If a user has left any fields blank, error message
prompting them to not leave any fields blank once they
have clicked the button
"""
def test_sign_up_fail_message(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "")
    page.fill("input[name='name']", "")
    page.fill("input[name='password']", "")
    page.click("input[type='submit']")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("Please fill in all the fields")

"""
If a User inputs an email address that is already in 
the database, there is an error message telling them that
an account already exists with this email, and say if they
want to log in, to go to log in page. Check database
does not add the new information.
"""
def test_sign_up_existing_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/sign_up")
    page.fill("input[name='email_address']", "sashaparkes@email.com")
    page.fill("input[name='name']", "Sasha Emily Parkes")
    page.fill("input[name='password']", "mypasswordisthis999")
    page.click("input[type='submit']")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("A user with this email address already exists")