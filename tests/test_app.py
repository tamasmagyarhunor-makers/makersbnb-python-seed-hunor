from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_list_a_space(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/spaces/new")

    # We look at the <p> tag
    h_tag = page.locator("h1")

    # We assert that it has the text "This is the homepage."
    expect(h_tag).to_have_text("List a space")

    


def test_new_spaces_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/spaces/new")

    form = page.locator("form[action='/spaces/new']")
    assert form.is_visible()

    name_label = page.locator("#name")
    assert name_label.is_visible()

    price_label = page.locator("#price_per_night")
    assert price_label.is_visible()

    available_from_label = page.locator("#available_from")
    assert available_from_label.is_visible()

    available_to_label = page.locator("#available_to")
    assert available_to_label.is_visible()

    submit_button = page.locator("button[type='submit']")
    assert submit_button.is_visible()

    # submit_button = page.locator("submit")
    # assert submit_button.is_visible()