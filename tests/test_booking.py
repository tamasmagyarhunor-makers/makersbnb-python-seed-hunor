from lib.booking import Booking
from datetime import date

def test_booking_creation():
    booking = Booking(1, 2, 3, date(2025,8,1),'Requested')
    assert booking.id == 1
    assert booking.user_id == 2
    assert booking.space_id == 3
    assert booking.booking_date == date(2025,8,1)
    assert booking.status == 'Requested'

def test_string_representaiton():
    booking = Booking(1, 2, 3, date(2025,8,1),'Requested')
    assert str(booking) == "Booking(1, 2, 3, 2025-08-01, Requested)"

def test_equality():
    booking1 = Booking(1, 2, 3, date(2025,8,1),'Requested')
    booking2 = Booking(1, 2, 3, date(2025,8,1),'Requested')
    assert booking1 == booking2