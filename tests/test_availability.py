from datetime import date
from lib.availability import *

"""
User constructs with an id, space_id, available_from, available_to)
"""
def test_availability_constructs():
    availability = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    assert availability.id == 1 
    assert availability.space_id == 1
    assert availability.available_from == date(2025, 7, 24)
    assert availability.available_to == date(2025, 8, 24)

"""
We can format availability to strings nicely
"""
def test_availability_formats_nicely():
    availability = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    assert str(availability) == "Availability(1, 1, 2025-07-24, 2025-08-24)"
"""
We can compare two identical availabilities
And have them be equal
"""
def test_users_are_equal():
    availability1 = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    availability2 = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    assert availability1 == availability2

"""
given a booking within the range, return ture
"""
def test_is_date_in_range_returns_true():
    availability = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    assert availability.is_date_in_range(date(2025, 8, 1), date(2025, 8, 15)) == True

"""
given a booking NOT in the range, return false
"""
def test_is_date_in_range_returns_false():
    availability = Availability(1, 1, date(2025, 7, 24), date(2025, 8, 24))
    assert availability.is_date_in_range(date(2025, 8, 1), date(2025, 8, 30)) == False