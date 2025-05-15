from lib.booking import Booking
from lib.booking_repository import BookingRepository
from datetime import date

def test_list_all(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.all() == [
        Booking(1, 1, 1, date(2025,7,5), 'Requested'),
        Booking(2, 2, 2, date(2025,11,10), 'Booked'),
        Booking(3, 2, 2, date(2025,11,12), 'Rejected')
    ]

def test_find_booking_by_id(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find(1) == Booking(1, 1, 1, date(2025,7,5), 'Requested')

def test_find_booking_by_id_not_found(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find(99) == None

def test_create_booking(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    repository.create(Booking(None, 1, 1, date(2025,9,1), 'Booked'))

    assert repository.find(4) == Booking(4, 1, 1, date(2025,9,1), 'Booked')

def test_update_status(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)
    
    assert repository.find(1) == Booking(1, 1, 1, date(2025,7,5), 'Requested')
    repository.update_status(1,'Booked')
    assert repository.find(1) == Booking(1, 1, 1, date(2025,7,5), 'Booked')

def test_find_bookings_for_space(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_space(2) == [
        Booking(2, 2, 2, date(2025,11,10), 'Booked'),
        Booking(3, 2, 2, date(2025,11,12), 'Rejected')
    ]

def test_find_bookings_for_space_empty(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_space(99) == [ ]

def test_find_bookings_made_by_user(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_user(1) == [
        Booking(1, 1, 1, date(2025,7,5), 'Requested')
    ]

def test_find_bookings_listed_by_user(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = BookingRepository(db_connection)

    assert repository.find_for_users_spaces(1) == [
        Booking(2, 2, 2, date(2025,11,10), 'Booked'),
        Booking(3, 2, 2, date(2025,11,12), 'Rejected')
    ]