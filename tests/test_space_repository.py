from lib.space import *
from lib.space_repository import *

def test_get_all_spaces(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
        Space(1,'The Barn','Converted barn set in a rural location', 65, 1),
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 1),
        Space(3,'The Hut', 'Rustic shepherds hut with its own hot tub', 55, 1),
        Space(4,'The Cottage', 'Cosy cottage with riverside views', 120, 1),
        Space(5,'The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 1),
        Space(6,'The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 1)
    ]