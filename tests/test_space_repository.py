from lib.space import *
from lib.space_repository import *

def test_get_all_spaces(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
        Space(1,'The Barn','Converted barn set in a rural location', 65, 1),
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 2),
        Space(3,'The Hut', 'Rustic shepherds hut with its own hot tub', 55, 2),
        Space(4,'The Cottage', 'Cosy cottage with riverside views', 120, 1),
        Space(5,'The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 1),
        Space(6,'The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 2)
    ]

def test_get_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.find_by_id(1) == Space(1,'The Barn', 'Converted barn set in a rural location', 65, 1)
    assert repository.find_by_id(2) == Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 2)

def test_create_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)
    new_space = Space(None, 'The Manor','A fancy manor house', 100, 2)
    repository.create(new_space)

    assert repository.find_by_id(7) == Space(7,'The Manor','A fancy manor house',100,2)

def test_delete_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    repository.delete(1)

    assert repository.all() == [
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 2),
        Space(3,'The Hut', 'Rustic shepherds hut with its own hot tub', 55, 2),
        Space(4,'The Cottage', 'Cosy cottage with riverside views', 120, 1),
        Space(5,'The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 1),
        Space(6,'The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 2)
    ]

def test_update_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)
    repository.update(1,'price_per_night',90)

    assert repository.find_by_id(1) == Space(1,'The Barn','Converted barn set in a rural location', 90, 1)

    assert repository.update(1,'dffsf',60) == 'Invalid Key'

def test_get_available_days_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.available_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-03','2025-01-04',
                                                    '2025-01-05','2025-01-06','2025-01-07']
    
def test_get_booked_days_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.booked_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-04',
                                                    '2025-01-05','2025-01-06']

def test_date_range_available_and_unbooked_by_space_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.booking_check(1,'2025-01-01','2025-01-05') == 'safe'
    assert repository.booking_check(1,'2025-01-01','2026-01-10') == 'not available'
    assert repository.booking_check(1,'2025-09-30','2025-10-01') == 'already booked'
