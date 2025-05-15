from playwright.sync_api import Page, expect
from lib.user import User
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.booking_repository import BookingRepository
from datetime import date

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

def test_create_user_route(page, test_web_address, db_connection):

    db_connection.seed("seeds/makersbnb_database.sql")

    page.goto(f"http://{test_web_address}/index")

    page.fill("input[name=user_name]", "Trudie")
    page.fill("input[name=password]", "abcdef")
    page.fill("input[name=email]", "trudie@example.com")
    page.fill("input[name=phone]", "018118181")
    page.click("button[type=submit]")

    repository = UserRepository(db_connection)
    # result = repository.all()
    assert repository.all() == [
        User(1, 'Bridget', 'qwerty', 'bridget@example.com', '07402498078'),
        User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321'),
        User(3, 'Trudie', 'abcdef', 'trudie@example.com', '018118181')
    ]

    title_element = page.locator(".mb-4")
    expect(title_element).to_have_text("Log in to Makers BnB")


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

    submit_button = page.locator("button[type='submit']")
    assert submit_button.is_visible()

    # submit_button = page.locator("submit")
    # assert submit_button.is_visible()


    
def test_login_page_exists(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    form = page.locator("form[action='/login']")
    assert form.is_visible()

    title = page.locator("h1.mb-4")
    assert title.is_visible()
    assert title.text_content() == "Log in to Makers BnB"

    username_field = page.locator("div.mb-3", has_text="Username")
    assert username_field.is_visible()

    password_field = page.locator("div.mb-3", has_text="password")
    assert password_field.is_visible()

    # submit_button = page.locator("form[action='/login'] button[type='submit']")
    # assert submit_button.is_visible()
    
def test_request_a_space_no_existing_bookings(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    test_space_id = 3

    # Log in
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=user_name]", "bridget@example.com")
    page.fill("input[name=password]", "qwerty")
    page.click("input[type=submit]")

    # Now we can go
    page.goto(f"http://{test_web_address}/spaces/request/{test_space_id}")
    page.fill("input[name=requested_date]", "2025-08-13")
    page.click("input[type=submit]")

    repository = BookingRepository(db_connection)
    result = repository.find(test_space_id)
    assert repository.find_for_space(test_space_id) == [
        Booking(4, 1, test_space_id, date(2025,8,13),'Requested')
    ]

    # this should be the results page
    space_name = page.locator("span.space_name")
    expect(space_name).to_contain_text("Ladybug Residence")
    booking_date = page.locator("span.booking_date")
    expect(booking_date).to_contain_text("13 August 2025")

def test_request_a_space_with_existing_bookings(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    test_space_id = 2

    # Log in
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=user_name]", "bridget@example.com")
    page.fill("input[name=password]", "qwerty")
    page.click("input[type=submit]")

    page.goto(f"http://{test_web_address}/spaces/request/{test_space_id}")

    booking_status_title = page.locator("h3.bookings_status_title")
    assert booking_status_title.is_visible()

    bookings = page.locator("p.booking_status")
    repository = BookingRepository(db_connection)
    db_bookings = repository.find_for_space(test_space_id)

    for i in range(0, len(db_bookings), 1):
        expect(bookings.nth(i)).to_have_text(f"Date: {str(db_bookings[i].booking_date)}, Status: {db_bookings[i].status}")

def test_show_my_requests(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    test_user_id = 1

    # Log in
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=user_name]", "bridget@example.com")
    page.fill("input[name=password]", "qwerty")
    page.click("input[type=submit]")

    page.goto(f"http://{test_web_address}/requests")

    bookings = page.locator("span.booking_status")
    repository = BookingRepository(db_connection)
    db_bookings = repository.find_for_user(test_user_id)

    for i in range(0, len(db_bookings), 1):
        expect(bookings.nth(i)).to_have_text(f"Date: {str(db_bookings[i].booking_date)}, Status: {db_bookings[i].status}")

# def test_show_booking_made(page, test_web_address):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     test_booking_id = 1

#     page.goto(f"http://{test_web_address}/requests?{test_booking_id}")

def test_post_new_space(db_connection, web_client):
    """
    Create a new space
    """
    db_connection.seed("seeds/makersbnb_database.sql")
    response = web_client.post('/spaces/new', data={'space_name': 'Butternut', 'spaces_description': 'Green room', 'price_per_night': 28, 'available_from_date': '2025-11-02', 'available_to_date': '2025-11-15', 'user_id': 2})
    assert response.status_code == 200
    assert response.data.decode('utf-8') == ''
