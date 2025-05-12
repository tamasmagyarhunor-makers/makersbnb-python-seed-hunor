from lib.space import *
from lib.space_repository import *

def test_get_all_spaces(db_connection):
    #db_connection.seed('')
    repository = SpaceRepository(db_connection)

    assert repository.all() == []