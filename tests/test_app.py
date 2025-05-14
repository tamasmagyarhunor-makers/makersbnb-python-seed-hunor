from playwright.sync_api import Page, expect

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

"""
When Space info is being rendered, host email address is pulled
from user table
"""

def test_get_host_email(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    page.goto(f"http://{test_web_address}/home_page")
    h6_tag = page.locator("h6")
    expect(h6_tag).to_have_text([
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: jamesdismore@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: sashaparkes@email.com',
        'Contact: jamesdismore@email.com'])