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

"""
When I call GET /spaces
I get a list of all the spaces
"""

def test_get_spaces(db_connection, test_web_address, page):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("All Spaces")

    # assert response.status_code == 200
    # assert "<h1>All Spaces</h1>" in html
    # assert "Cozy london flat" in html
    # assert "£85.0" in html