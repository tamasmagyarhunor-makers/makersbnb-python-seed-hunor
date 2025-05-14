from lib.availability_range import AvailabilityRange

def test_availability_contructs():
    availrange = AvailabilityRange(1,'2025-01-01','2026-01-01',1)

    assert availrange.id == 1
    assert availrange.start_date == '2025-01-01'
    assert availrange.end_date == '2026-01-01'
    assert availrange.space_id == 1

def test_availability_formatting():
    availrange = AvailabilityRange(1,'2025-01-01','2026-01-01',1)

    assert str(availrange) == 'AvailableRange(1, 2025-01-01, 2026-01-01, 1)'

def test_availability_equal():
    availrange1 = AvailabilityRange(1,'2025-01-01','2026-01-01',1)
    availrange2 = AvailabilityRange(1,'2025-01-01','2026-01-01',1)
    availrange3 = AvailabilityRange(2,'2025-01-01','2026-01-01',1)

    assert availrange1 == availrange2
    assert availrange1 != availrange3