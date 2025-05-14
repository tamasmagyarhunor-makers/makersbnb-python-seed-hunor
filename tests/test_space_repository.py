from lib.space_repository import SpaceRepository
from lib.space import Space

"""
When we call SpaceRepository #list_spaces
We get a list of Space objects reflecting the seed data.
"""
def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    spaces = repository.list_spaces()

    assert spaces == [
        Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1),
        Space(2, 'Urban Loft', 'Sleek apartment in downtown.', 150, 2),
        Space(3, 'Beach Bungalow', 'Sunny spot by the sea.', 200, 3),
        Space(4, 'Mountain Retreat', 'Quiet escape in the hills.', 180, 4),
        Space(5, 'Modern Studio', 'Compact yet luxurious.', 120, 5)
    ]

"""
When we call SpaceRepository #add_space
And then call #list_spaces
We get a list of spaces with the new space included
"""

def test_add_space(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    new_space = Space(None, 'Cardboard Box', 'Back to basics, no ensuite.', 10000, 1)
    repository.add_space(new_space)
    
    spaces = repository.list_spaces()

    assert spaces == [
        Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1),
        Space(2, 'Urban Loft', 'Sleek apartment in downtown.', 150, 2),
        Space(3, 'Beach Bungalow', 'Sunny spot by the sea.', 200, 3),
        Space(4, 'Mountain Retreat', 'Quiet escape in the hills.', 180, 4),
        Space(5, 'Modern Studio', 'Compact yet luxurious.', 120, 5),
        Space(6, 'Cardboard Box', 'Back to basics, no ensuite.', 10000, 1)
    ]