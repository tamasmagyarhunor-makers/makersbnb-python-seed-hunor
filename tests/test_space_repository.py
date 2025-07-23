from lib.space_repository import SpaceRepository
from lib.space import Space

"""
When we call spacerepository#all
We get a list of all the spaces
"""

def test_get_all_spaces(db_connection):
    db_connection.seed('seeds/makers_bnb.sql')
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
    Space(1, 'Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00, 1),
    Space(2, 'Garden studio', 'Peaceful studio with private garden access', 65.00, 1),
    Space(3, 'Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00, 2)
    ]
    
"""
When we call SpaceRepository#create  
We get a new record in the database 
"""

def test_create_space(db_connection):
    db_connection.seed('seeds/makers_bnb.sql')
    repository = SpaceRepository(db_connection)
    
    space = Space(None, "Test Name", "Test Description", 100.0, 2)
    repository.create(space)
    assert repository.all() == [
    Space(1, 'Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00, 1),
    Space(2, 'Garden studio', 'Peaceful studio with private garden access', 65.00, 1),
    Space(3, 'Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00, 2),
    Space(4, "Test Name", "Test Description", 100.0, 2)
    ]