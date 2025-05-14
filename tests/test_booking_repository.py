from lib.booking import Booking
from lib.booking_repository import BookingRepository
from datetime import date

def test_list_all(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.all() == [
        Booking(1, 1, 1, date(2025,6,1), 'Requested'),
        Booking(2, 2, 2, date(2025,7,1), 'Booked'),
        Booking(3, 2, 2, date(2025,8,1), 'Rejected')
    ]

def test_find_booking_by_id(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find(1) == Booking(1, 1, 1, date(2025,6,1), 'Requested')

def test_find_booking_by_id_not_found(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find(99) == None

def test_add_booking(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    repository.add(Booking(None, 1, 1, date(2025,9,1), 'Booked'))

    assert repository.find(4) == Booking(4, 1, 1, date(2025,9,1), 'Booked')

def test_update_status(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)
    
    assert repository.find(1) == Booking(1, 1, 1, date(2025,6,1), 'Requested')
    repository.update_status(1,'Booked')
    assert repository.find(1) == Booking(1, 1, 1, date(2025,6,1), 'Booked')

def test_find_bookings_for_space(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_space(2) == [
        Booking(2, 2, 2, date(2025,7,1), 'Booked'),
        Booking(3, 2, 2, date(2025,8,1), 'Rejected')
    ]

def test_find_bookings_for_space_empty(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_space(99) == [ ]