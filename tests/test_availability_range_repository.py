from lib.availability_range_repository import AvailabilityRange, AvailabilityRangeRepository


def test_get_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = AvailabilityRangeRepository(db_connection)

    assert repository.find_by_id(1) == AvailabilityRange(1,'2025-01-01','2026-01-01',1)
    assert repository.find_by_id(2) == AvailabilityRange(2,'2025-01-01','2026-01-01',2)

def test_get_by_space_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = AvailabilityRangeRepository(db_connection)

    assert repository.find_by_space_id(1) == [AvailabilityRange(1,'2025-01-01','2026-01-01',1)]

def test_add_available_range(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = AvailabilityRangeRepository(db_connection)

    repository.add_range('2025-10-01','2025-11-01',1)

    repository.find_by_space_id(1) == [
        AvailabilityRange(1,'2025-01-01','2026-01-01',1),
        AvailabilityRange(4,'2025-10-01','2025-11-01',1)
    ]

