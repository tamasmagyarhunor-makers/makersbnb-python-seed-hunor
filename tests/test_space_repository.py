from lib.space_repository import SpaceRepository
from lib.space import Space
import datetime

"""
Test get all spaces
"""
def test_space_repository_all(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = SpaceRepository(db_connection)
    assert repository.all() == [
        Space(1, 'Bee Hive', 'A peaceful hexagonal room', 85, datetime.date(2025,7,1), datetime.date(2025,7,12), 2),
        Space(2, 'Ant farm', 'Bite-sized luxury pod', 77, datetime.date(2025,11,6), datetime.date(2025,11,20), 1),
        Space(3, 'Ladybug Residence', 'Luxury spots available nightly', 99, datetime.date(2025,8,12), datetime.date(2025,8,31), 1)
        ]

"""
Test add in a space
"""
def test_create_space(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")
    repository = SpaceRepository(db_connection)
    space = Space(None, "Butterfly", "Colourful room", 18, '2025-10-02', '2025-10-15', 2)
    repository.create(space)
    result = repository.all()
    print(type(result[0].available_from_date))
    print(type(space.available_from_date))
    assert result == [
        Space(1, 'Bee Hive', 'A peaceful hexagonal room', 85, datetime.date(2025,7,1), datetime.date(2025,7,12), 2),
        Space(2, 'Ant farm', 'Bite-sized luxury pod', 77, datetime.date(2025,11,6), datetime.date(2025,11,20), 1),
        Space(3, 'Ladybug Residence', 'Luxury spots available nightly', 99, datetime.date(2025,8,12), datetime.date(2025,8,31), 1),
        Space(4, 'Butterfly', "Colourful room", 18, datetime.date(2025,10,2), datetime.date(2025,10,15), 2)
    ]

"""
Test finding a space by id
"""
def test_finding_a_space_by_id(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = SpaceRepository(db_connection)
    space = repository.find(2)
    assert space == Space(2, 'Ant farm', 'Bite-sized luxury pod', 77, datetime.date(2025,11,6), datetime.date(2025,11,20), 1)

"""
Test finding a space by user id
"""
def test_finding_a_space_by_user_id(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = SpaceRepository(db_connection)
    space = repository.find_by_user(1)
    assert space == [
        Space(2, 'Ant farm', 'Bite-sized luxury pod', 77, datetime.date(2025,11,6), datetime.date(2025,11,20), 1),
        Space(3, 'Ladybug Residence', 'Luxury spots available nightly', 99, datetime.date(2025,8,12), datetime.date(2025,8,31), 1)
        ]


"""
Test finding a space by name
"""
def test_finding_a_space_by_name(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = SpaceRepository(db_connection)
    space = repository.find_by_name('Bee Hive')
    assert space == Space(1, 'Bee Hive', 'A peaceful hexagonal room', 85, datetime.date(2025,7,1), datetime.date(2025,7,12), 2)

"""
Test delete a space
"""
def test_delete_space(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = SpaceRepository(db_connection)
    user = repository.delete(3)
    assert repository.all() == [
        Space(1, 'Bee Hive', 'A peaceful hexagonal room', 85, datetime.date(2025,7,1), datetime.date(2025,7,12), 2),
        Space(2, 'Ant farm', 'Bite-sized luxury pod', 77, datetime.date(2025,11,6), datetime.date(2025,11,20), 1)
