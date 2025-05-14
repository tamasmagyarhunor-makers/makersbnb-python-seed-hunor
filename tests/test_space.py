from lib.space import Space

"""
space constructs with an id, name, description, price per night and user id
"""
def test_space_constructs():
    space = Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1)
    assert space.space_id == 1
    assert space.name == 'Cozy Cabin'
    assert space.description == 'Rustic cabin in the forest.'
    assert space.price_per_night == 100
    assert space.user_id == 1

"""
We can format spaces to strings nicely
"""
def test_spaces_format_nicely():
    space = Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1)
    assert str(space) == "Space(1, Cozy Cabin, Rustic cabin in the forest., 100, 1)"

"""
We can compare two identical spaces
And have them be equal
"""
def test_spaces_are_equal():
    space1 = Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1)
    space2 = Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1)
    assert space1 == space2