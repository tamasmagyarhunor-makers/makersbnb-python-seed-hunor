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
We can render the home page
"""
def test_get_homepage(page, test_web_address):
    page.goto(f"http://{test_web_address}/home_page")
    h3_tag = page.locator("h3")
    expect(h3_tag).to_have_text("Build Bootstrap with Webpack")