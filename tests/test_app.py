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


"""
We can render the 'list a space' page
"""

def test_get_list_a_space(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/spaces/new")

    # We look at the <p> tag
    h_tag = page.locator("h1")

    # We assert that it has the text "This is the homepage."
    expect(h_tag).to_have_text("Showcase Your Space")

"""
We can render the 'spaces' page
"""

def test_get_spaces(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/spaces")

    # We look at the <p> tag
    h_tag = page.locator("h1")

    # We assert that it has the text "This is the homepage."
    expect(h_tag).to_have_text("Reserve Exquisite Accommodation")

"""
We can see the form with all the required fields on the 'list a space' page
"""

def test_new_spaces_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/spaces/new")

    form = page.locator("form[action='/spaces/new']")
    assert form.is_visible()

    name_label = page.locator("#space_name")
    assert name_label.is_visible()

    price_label = page.locator("#price_per_night")
    assert price_label.is_visible()

    available_from_label = page.locator("#available_from_date")
    assert available_from_label.is_visible()

    available_to_label = page.locator("#available_to_date")
    assert available_to_label.is_visible()

def test_post_new_space(db_connection, web_client):
    """
    Create a new space
    """
    db_connection.seed("seeds/makersbnb_database.sql")
    response = web_client.post('/spaces/new', data={'space_name': 'Butternut', 'spaces_description': 'Green room', 'price_per_night': 28, 'available_from_date': '2025-11-02', 'available_to_date': '2025-11-15', 'user_id': 2})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == ''