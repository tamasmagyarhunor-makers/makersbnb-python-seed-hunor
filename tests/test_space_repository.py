from lib.space_repository import SpaceRepository
from lib.space import Space

"""
When we call spacerepository#all
We get a list of all the spaces
"""

def test_get_all_spaces(db_connection):
    
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
    Space(1, 'Cozy london flat', 'A beautiful 1-bedroom flat in central london', 85.00),
    Space(2, 'Garden studio', 'Peaceful studio with private garden access', 65.00),
    Space(3, 'Modern Apartment', 'Stylish 2-bedroom apartment near the tube', 120.00)
    ]