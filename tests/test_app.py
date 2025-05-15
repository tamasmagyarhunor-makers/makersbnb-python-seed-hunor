import re
from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User

"""
1. When page is called, space names are displayed
"""
def test_get_spaces(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql") 
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

"""
2. When user is not logged in, sign in buttons
appear on screen
"""
def test_logged_out_appearance(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql") 
    page.goto(f"http://{test_web_address}/home_page")
    buttons = page.locator("button")
    expect(buttons).to_have_text([
        "Sign Up",
        "Log In",
        "Your Account"
    ])

"""
3. When user IS logged in, sign in buttons do not
appear and are replaced with logout button
"""
def test_logged_in_appearance(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql") 
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "sashaparkes@email.com")
    page.fill("input[name='password']", "mypassword1234")
    page.click("input[type='submit']")
    page.click("#home_button")
    buttons = page.locator("button")
    expect(buttons).to_have_text([
        "Your Account",
        "Logout"
    ])

"""
4. When Space info is being rendered, host email address is pulled
from user table
"""

def test_get_host_email(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/home_page")
    host_email_tag = page.locator("#host_email")
    expect(host_email_tag).to_have_text([
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com'])

"""
5. Sign up page renders
"""
def test_get_sign_up_page(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/sign_up")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text("Sign Up")

"""
6. When user clicks sign up button on home, they are 
redirected to sign up page
"""
def test_signup_button_works(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/home_page")
    page.click("button.signup")
    expect(page).to_have_url(f"http://{test_web_address}/sign_up")


"""
7
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
8
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
9
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
10
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
    expect(h2_tag).to_have_text("Sign Up")

"""
11
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
12
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

"""
13
login page renders
"""
def test_get_login_page(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/login")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text("Login")

"""
14
When user clicks login button on home, they are 
redirected to login page
"""
def test_login_button_works(page, test_web_address, db_connection):
    page.goto(f"http://{test_web_address}/home_page")
    page.click("button.login")
    expect(page).to_have_url(f"http://{test_web_address}/login")

"""
15
When user inputs email and password that match what is on
database, redirection to user home
"""
def test_successful_signin(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "sashaparkes@email.com")
    page.fill("input[name='password']", "mypassword1234")
    page.click("input[type='submit']")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Your MakersBnb Account")

"""
16
When user inputs email and password that don't match what is on
database, error appears
"""
def test_bad_signin(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "testbad@email.com")
    page.fill("input[name='password']", "badpass")
    page.click("input[type='submit']")
    error_msg = page.locator("#error_message")
    expect(error_msg).to_have_text("Invalid email or password")

"""
17
If a user has left any fields blank, error message
prompting them to not leave any fields blank once they
have clicked the button
"""
def test_login_empty_fail_message(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "")
    page.fill("input[name='password']", "")
    page.click("input[type='submit']")
    error_msg = page.locator("#error_message")
    expect(error_msg).to_have_text("Please fill in all the fields")

"""
18
When a user clicks logged out,
they are logged out , returned to login page
and session is cleared
"""
def test_logout_clears_session(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "sashaparkes@email.com")
    page.fill("input[name='password']", "mypassword1234")
    page.click("input[type='submit']")
    page.click("button.logout")
    page.goto(f"http://{test_web_address}/userhome")
    expect(page).to_have_url(f"http://{test_web_address}/login")

"""
19
If logged in, clicking your account should
direct to user_home
"""
def test_account_button_to_home_logged_in(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email_address']", "sashaparkes@email.com")
    page.fill("input[name='password']", "mypassword1234")
    page.click("input[type='submit']")
    page.click("#home_button")
    page.click("#userhome_button")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Your MakersBnb Account")

"""
20
if not logged in, clicking your account
should direct to login
"""
def test_account_button_to_home_logged_out(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/home_page")

    page.click("#userhome_button")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Login")

"""
21
User can create new spaces and they are added to the database
"""

def test_create_new_space_post_method(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/home_page/add-space")
    
    page.fill("input[name='name']", "Test Space")
    page.fill("textarea[name='description']", "This is a test space")
    page.fill("input[name='price_per_night']", "100")
    
    page.click("input[type='submit']")
    
    expect(page).to_have_url(re.compile(r"home_page/\d+"))
    
    expect(page.locator("body")).to_contain_text("Test Space")

