from lib.space_repository import SpaceRepository
from lib.space import Space

"""
When we call Albumrepository#all
We get a list of all the albums
"""

def test_get_all_albums(db_connection):
    # db_connection.seed("seeds/record_store.sql")
    repository = AlbumRepository(db_connection)
    assert repository.all() == [
        Album(1, "Black", 1991, 1)
    ]