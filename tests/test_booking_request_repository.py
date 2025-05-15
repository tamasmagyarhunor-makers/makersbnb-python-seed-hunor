from lib.booking_request_repository import *

def test_get_bookings_by_space_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = BookingRequestRepository(db_connection)
    
    assert repository.find_by_space_id(1) == [
        BookingRequest(1,'2025-11-05','2025-11-06',1,2)
    ]

def test_add_booking_request_to_space(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = BookingRequestRepository(db_connection)

    repository.add_booking_request('2025-06-01','2025-06-07',1,1)

    assert repository.find_by_space_id(1) == [
        BookingRequest(1,'2025-11-05','2025-11-06',1,2),
        BookingRequest(3,'2025-06-01','2025-06-07',1,1)
    ]

def test_delete_booking_request_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = BookingRequestRepository(db_connection)

    repository.delete_by_id(1)

    assert repository.find_by_space_id(1) == []

    repository.add_booking_request('2025-06-01','2025-06-07',1,1)

    assert repository.find_by_space_id(1) == [
        BookingRequest(3,'2025-06-01','2025-06-07',1,1)
    ]