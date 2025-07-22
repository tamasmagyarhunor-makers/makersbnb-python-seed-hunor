from lib.user import User

"""
User constructs with an id, name, email and password
"""
def test_user_constructs():
    user = User(1, "Alice", "alice@example.com" , "password1" )
    assert user.id == 1 
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.password == "password1"

"""
We can format users to strings nicely
"""
def test_users_formats_nicely():
    user = User(1,"Alice", "alice@example.com" , "password1" )
    assert str(user) == "User(1, Alice, alice@example.com)"

"""
We can compare two identical users
And have them be equal
"""
def test_users_are_equal():
    user1 = User(1,"Alice", "alice@example.com" , "password1" )
    user2 = User(1,"Alice", "alice@example.com" , "password1" )
    assert user1 == user2

# Leave for later for added complexity

"""
We can assess a user for validity
"""

"""
We can generate errors for an invalid user
"""