from lib.space import Space

"""
Test if class object constructs
"""
def test_space_constructs():
    space = Space(1, "Bee Hive", "Yellow Room", 17.99, '2025-05-15', '2025-05-31', 2)
    assert space.id == 1
    assert space.space_name == "Bee Hive"
    assert space.spaces_description == "Yellow Room"
    assert space.price_per_night == 17.99
    assert space.available_from_date == '2025-05-15'
    assert space.available_to_date == '2025-05-31'
    assert space.user_id == 2


"""
# Test that space object formats nicely
# """

def test_space_object_formats_nicely():
    space = Space(1, "Bee Hive", "Yellow Room", 17.99, '2025-05-15', '2025-05-31', 2)
    assert str(space) == "Space(1, Bee Hive, Yellow Room, 17.99, 2025-05-15, 2025-05-31, 2)"


"""
Test that space objects are equal
"""

def test_space_objects_are_equal():
    space_1 = Space(1, "Bee Hive", "Yellow Room", 17.99, '2025-05-15', '2025-05-31', 2)
    space_2 = Space(1, "Bee Hive", "Yellow Room", 17.99, '2025-05-15', '2025-05-31', 2)
    assert space_1 == space_2