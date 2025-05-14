from lib.user import User

"""
Test if class object constructs
"""

def test_user_constructs():
    user = User(3, "Tim", "tim@example.com", "07118118118")
    assert user.id == 3
    assert user.user_name == "Tim"
    assert user.email == "tim@example.com"
    assert user.phone == "07118118118"

"""
Test that user object formats nicely
"""

def test_user_object_formats_nicely():
    user = User(3, "Tim", "tim@example.com", "07118118118")
    assert str(user) == "User(3, Tim, tim@example.com, 07118118118)"

"""
Test that user objects are equal
"""

def test_user_objects_are_equal():
    user_1 = User(3, "Tim", "tim@example.com", "07118118118")
    user_2 = User(3, "Tim", "tim@example.com", "07118118118")
    assert user_1 == user_2
