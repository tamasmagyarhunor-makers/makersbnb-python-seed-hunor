from playwright.sync_api import Page, expect
from lib.user import User
from lib.user_repository import UserRepository

# Tests for your routes go here

"""
We can render the index page
"""
# def test_get_index(page, test_web_address):
#     # We load a virtual browser and navigate to the /index page
#     page.goto(f"http://{test_web_address}/index")

#     # We look at the <p> tag
#     p_tag = page.locator("p")

#     # We assert that it has the text "This is the homepage."
#     expect(p_tag).to_have_text("This is the homepage.")

"""
We can create a new user and it gets reflected in the data
"""
def test_create_user(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    page.goto(f"http://{test_web_address}/index")

    page.fill("input[name=user_name]", "Trudie")
    page.fill("input[name=password]", "abcdef")
    page.fill("input[name=email]", "trudie@example.com")
    page.fill("input[name=phone]", "018118181")
    page.click("input[type=submit]")

    repository = UserRepository(db_connection)
    result = repository.all()
    assert repository.all() == [
        User(1, 'Bridget', 'bridget@example.com', '07402498078'),
        User(2, 'Hannah', 'hannah@example.com', '07987654321'),
        User(3, 'Trudie', 'trudie@example.com', '018118181')
    ]


