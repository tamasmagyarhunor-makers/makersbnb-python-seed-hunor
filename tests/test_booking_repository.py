from lib.booking_repository import *

def test_get_bookings_by_space_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = BookingRepository(db_connection)
    
    assert repository.find_by_space_id(3) == [
        Booking(3,'2025-01-01','2025-01-02',3,1),
        Booking(4,'2025-01-04','2025-01-06',3,1)
    ]

def test_add_booking_to_space(db_connection):

    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = BookingRepository(db_connection)

    repository.add_booking('2025-06-01','2025-06-07',1,1)

    assert repository.find_by_space_id(1) == [
        Booking(1,'2025-10-01','2025-10-02',1,2),
        Booking(5,'2025-06-01','2025-06-07',1,1)
    ]