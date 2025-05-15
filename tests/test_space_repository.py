from lib.space import *
from lib.space_repository import *
from lib.availability_range_repository import *
from lib.booking_repository import *

def test_get_all_spaces(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.all() == [
        Space(1,'The Barn','Converted barn set in a rural location', 65, 'https://imgur.com/a/aRME8sh', 1),
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 'https://imgur.com/a/OiVgFYj', 2),
        Space(3,'The Hut', 'Rustic shepherds hut with its own hot tub', 55, 'https://imgur.com/a/PBYfKgT', 2),
        Space(4,'The Cottage', 'Cosy cottage with riverside views', 120, 'https://imgur.com/a/YKqKNdP', 1),
        Space(5,'The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 'https://imgur.com/a/nyASeEK', 1),
        Space(6,'The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 'https://imgur.com/a/RwyKpHF', 2)
    ]

def test_get_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.find_by_id(1) == Space(1,'The Barn','Converted barn set in a rural location', 65, 'https://imgur.com/a/aRME8sh', 1)
    assert repository.find_by_id(2) == Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 'https://imgur.com/a/OiVgFYj', 2)

def test_create_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)
    new_space = Space(None, 'The Manor','A fancy manor house', 100,'imagetesturl.url',2)
    repository.create(new_space)

    assert repository.find_by_id(7) == Space(7,'The Manor','A fancy manor house',100,'imagetesturl.url',2)

def test_delete_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    repository.delete(1)

    assert repository.all() == [
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 'https://imgur.com/a/OiVgFYj', 2),
        Space(3,'The Hut', 'Rustic shepherds hut with its own hot tub', 55, 'https://imgur.com/a/PBYfKgT', 2),
        Space(4,'The Cottage', 'Cosy cottage with riverside views', 120, 'https://imgur.com/a/YKqKNdP', 1),
        Space(5,'The Penthouse', 'Top floor luxury penthouse with breathtaking views', 160, 'https://imgur.com/a/nyASeEK', 1),
        Space(6,'The Beach Hut', 'Shoreline stay just footsteps from the seashore', 110, 'https://imgur.com/a/RwyKpHF', 2)
    ]

def test_update_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)
    repository.update(1,'price_per_night',90)

    assert repository.find_by_id(1) == Space(1,'The Barn','Converted barn set in a rural location', 90, 'https://imgur.com/a/aRME8sh', 1)

    assert repository.update(1,'dffsf',60) == 'Invalid Key'

def test_get_available_days_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.available_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-03','2025-01-04',
                                                    '2025-01-05','2025-01-06','2025-01-07']
    
    avail_repository = AvailabilityRangeRepository(db_connection)
    
    avail_repository.add_range('2025-02-01','2025-02-02',3)

    assert repository.available_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-03','2025-01-04',
                                                    '2025-01-05','2025-01-06','2025-01-07','2025-02-01','2025-02-02']
    
def test_get_booked_days_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.booked_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-04',
                                                    '2025-01-05','2025-01-06',]
    
    booking_repository = BookingRepository(db_connection)

    booking_repository.add_booking('2025-01-07','2025-01-07',3,1)


    assert repository.booked_days_by_id(3) == ['2025-01-01','2025-01-02','2025-01-04',
                                                    '2025-01-05','2025-01-06','2025-01-07']
    


def test_date_range_available_and_unbooked_by_space_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.booking_check(1,'2025-01-01','2025-01-05') == 'safe'
    assert repository.booking_check(1,'2025-01-01','2026-01-10') == 'not available'
    assert repository.booking_check(1,'2025-09-30','2025-10-01') == 'already booked'


def test_get_spaces_by_available_and_unbooked(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = SpaceRepository(db_connection)

    assert repository.get_available_unbooked_spaces('2025-01-06','2025-01-07') == [
        Space(1,'The Barn','Converted barn set in a rural location', 65, 'https://imgur.com/a/aRME8sh', 1),
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 'https://imgur.com/a/OiVgFYj', 2)
    ]

    assert repository.get_available_unbooked_spaces('2025-09-30','2025-10-02') == [
        Space(2,'The Loft', 'City centre loft space with great access to amenities', 95, 'https://imgur.com/a/OiVgFYj', 2)
    ]