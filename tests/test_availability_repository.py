from datetime import date
from lib.availability_repository import *
from lib.availability import *

"""
When we call AvailabilityRepository #all
We get a list of all the availabilities
"""

def test_get_all_availabilities(db_connection):
    db_connection.seed('seeds/makers_bnb.sql')
    repository = AvailabilityRepository(db_connection)

    assert repository.all() == [
    Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24)),
    Availability(2, 1, date(2025, 9, 30), date(2025, 12, 20)),
    Availability(3, 2, date(2025, 7, 24), date(2025, 9, 30)),
    Availability(4, 3, date(2025, 7, 24), date(2025, 12, 31))
    ]
    
"""
When we call AvailabilityRepository #create  
We get a new record in the database 
"""

def test_create_availability(db_connection):
    db_connection.seed('seeds/makers_bnb.sql')
    repository = AvailabilityRepository(db_connection)
    
    availability = Availability(None, 2, date(2025, 10, 10), date(2025, 11, 11))
    repository.create(availability)
    assert repository.all() == [
    Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24)),
    Availability(2, 1, date(2025, 9, 30), date(2025, 12, 20)),
    Availability(3, 2, date(2025, 7, 24), date(2025, 9, 30)),
    Availability(4, 3, date(2025, 7, 24), date(2025, 12, 31)),
    Availability(5, 2, date(2025, 10, 10), date(2025, 11, 11))
    ]

"""
When we call AvailabilityRepository #find
We get a single Availability object reflecting the seed data
"""
def test_get_availability_for_a_space(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = AvailabilityRepository(db_connection)

    availability = repository.find(1)
    assert availability == [
        Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24)),
        Availability(2, 1, date(2025, 9, 30), date(2025, 12, 20))
    ]