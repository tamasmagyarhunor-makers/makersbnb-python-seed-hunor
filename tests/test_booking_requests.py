from lib.booking_requests import BookingRequest

def test_booking_constructs():
    booking_request = BookingRequest(1,'2025-01-01','2026-01-01',1,1)

    assert booking_request.id == 1
    assert booking_request.start_date == '2025-01-01'
    assert booking_request.end_date == '2026-01-01'
    assert booking_request.space_id == 1
    assert booking_request.user_id == 1

def test_booking_formatting():
    booking_request = BookingRequest(1,'2025-01-01','2026-01-01',1,1)

    assert str(booking_request) == 'Booking Request(1, 2025-01-01, 2026-01-01, 1, 1)'

def test_bookings_are_equal():
    booking1 = BookingRequest(1,'2025-01-01','2026-01-01',1,1)
    booking2 = BookingRequest(1,'2025-01-01','2026-01-01',1,1)
    booking3 = BookingRequest(2,'2025-01-01','2026-01-01',1,1)

    assert booking1 == booking2
    assert booking1 != booking3