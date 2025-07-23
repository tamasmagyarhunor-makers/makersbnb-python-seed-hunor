from lib.space import Space

"""
Space constructs with id, name, description and price_per_night
"""

def test_space_constructs():
    space = Space(1, 'Test Space', 'Test Description', 100.00, 2)
    assert space.id == 1
    assert space.name == 'Test Space'
    assert space.description == 'Test Description'
    assert space.price_per_night == 100.00
    assert space.user_id == 2

"""
We can format spaces to strings
"""
def test_spaces_format():
    space = Space(1, 'Test Name', 'Test Description', 100.0, 2)
    assert str(space) == 'Space(1, Test Name, Test Description, 100.0, 2)'

def test_spaces_are_equal():
    space1 = Space(1, 'Test Name', 'Test Description', 100.0, 2)
    space2 = Space(1, 'Test Name', 'Test Description', 100.0, 2)
    assert space1 == space2