import re
from playwright.sync_api import Page, expect

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

"""
When Space info is being rendered, host email address is pulled
from user table
"""

def test_get_host_email(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/home_page")
    host_email_tag = page.locator(".host_email")
    expect(host_email_tag).to_have_text([
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com'])

"""
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