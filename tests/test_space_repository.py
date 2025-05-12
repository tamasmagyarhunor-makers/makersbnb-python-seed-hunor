from lib.space import *
from lib.space_repository import *

def test_get_all_spaces(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
        Space(1,'The Barn','Converted barn set in a rural location', 65, 1)
    ]