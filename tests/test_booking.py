from lib.booking import Booking
import datetime


def test_booking_initialisation():
    booking = Booking(1, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10))

    assert booking.id == 1
    assert booking.user_id == 2
    assert booking.space_id == 3
    assert booking.start_date == datetime.date(2025, 1, 1)
    assert booking.end_date == datetime.date(2025, 1, 10)
    assert booking.status == 'pending'

def test_identical_bookings_are_equal():
    first_booking = Booking(1, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10), 'pending')
    second_booking = Booking(1, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10), 'pending')    
    assert first_booking == second_booking
    
    different_status_booking = Booking(1, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10), 'confirmed')
    assert first_booking != different_status_booking

    different_booking = Booking(10, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10), 'pending')
    assert first_booking != different_booking

def test_booking_string_representation():
    booking = Booking(1, 2, 3, datetime.date(2025, 1, 1), datetime.date(2025, 1, 10), 'pending')
    expected = "Booking(1, 2, 3, 2025-01-01, 2025-01-10, 'pending')"

    assert str(booking) == expected



