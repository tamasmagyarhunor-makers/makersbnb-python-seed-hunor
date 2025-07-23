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
Get all the users
"""
def test_get_users(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

    # We load a virtual browser and navigate to the /books page
    page.goto(f"http://{test_web_address}/users")

    # We look at all the <li> tags
    list_items = page.locator("li")

    # We assert that it has the users in it
    expect(list_items).to_have_text([
        "Alice (alice@example.com)",
        "Bob (bob@example.com)"
    ])


"""
Get a single user
"""
def test_get_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")

    # We visit the books page
    page.goto(f"http://{test_web_address}/users")

    # Click the link with the text 'Name: Alice Email: alice@example.com'
    page.click("text=Alice (alice@example.com)")

    # The virtual browser acts just like a normal browser and goes to the next
    # page without us having to tell it to.

    # Then we look for specific test classes that we have put into the HTML
    # as targets for our tests to look for. This one is called `t-title`.
    # You can see it in `templates/books/show.html`
    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: Alice")

    # We do the same for the author name
    author_element = page.locator(".t-email")
    expect(author_element).to_have_text("Email: alice@example.com")


"""
When we create a new user
We see it in the users index
"""
def test_create_user(db_connection, page, test_web_address):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/users")

    # This time we click the link with the text 'Add a new user'
    page.click("text=Add a new user")

    # Then we fill out the field with the name attribute 'name'
    page.fill("input[name='name']", "Charlie")

    # And the field with the name attribute 'email'
    page.fill("input[name='email']", "charlie@example.com")

    # Finally we click the button with the text 'Create User'
    page.click("text=Create User")

    # Just as before, the virtual browser acts just like a normal browser and
    # goes to the next page without us having to tell it to.

    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: Charlie")

    author_element = page.locator(".t-email")
    expect(author_element).to_have_text("Email: charlie@example.com")