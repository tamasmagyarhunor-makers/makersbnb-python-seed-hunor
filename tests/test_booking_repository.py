from lib.booking import Booking
from lib.booking_repository import BookingRepository
import datetime

def test_get_all_bookings(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)

    retrieved_bookings = repository.get_all_bookings()
    assert retrieved_bookings == [
        Booking(1, 1, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 5), 'confirmed'),
        Booking(2, 2, 1, datetime.date(2025, 9, 10), datetime.date(2025, 9, 15), 'confirmed')
    ]

def test_make_booking(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)

    new_booking = Booking(None, 1, 2, datetime.date(2026, 3, 1), datetime.date(2026, 3, 10))
    repository.make_booking(new_booking)

    assert repository.get_all_bookings() == [
        Booking(1, 1, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 5), 'confirmed'),
        Booking(2, 2, 1, datetime.date(2025, 9, 10), datetime.date(2025, 9, 15), 'confirmed'),
        Booking(3, 1, 2, datetime.date(2026, 3, 1), datetime.date(2026, 3, 10), 'pending')
    ]

def test_get_booking_by_booking_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)
    assert repository.get_booking_by_booking_id(1) == Booking(1, 1, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 5), 'confirmed')
