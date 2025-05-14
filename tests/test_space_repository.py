from lib.space_repository import SpaceRepository
from lib.space import Space

"""
Test get all SPACES
"""
# def test_space_repository_all(db_connection):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     repository = SpaceRepository(db_connection)
#     assert repository.all() == [
#         Space(1, 'Bee Hive', 'A peaceful hexagonal room', 85.50, '2025-07-01', '2025-07-12', 2),
#         Space(2, 'Ant farm', 'Bite-sized luxury pod', 77.25, '2025-11-06', '2025-11-20', 1),
#         Space(3, 'Ladybug Residence', 'Luxury spots available nightly', 99.99, '2025-08-12', '2025-08-31', 1)
#     ]

# """
# Test add in a user
# """
# def test_create_user(db_connection):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     repository = UserRepository(db_connection)
#     user = User(None, "Tim", "tim@example.com", "0118118118118")
#     repository.create(user)
#     result = repository.all()
#     assert repository.all() == [
#         User(1, 'Bridget', 'bridget@example.com', '07402498078'),
#         User(2, 'Hannah', 'hannah@example.com', '07987654321'),
#         User(3, 'Tim', 'tim@example.com', '0118118118118')
#     ]

# """
# Test finding a user by id
# """
# def test_finding_a_user_by_id(db_connection):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     repository = UserRepository(db_connection)
#     user = repository.find(2)
#     assert user == User(2, 'Hannah', 'hannah@example.com', '07987654321')

# """
# Test finding a user by email
# """
# def test_finding_a_user_by_email(db_connection):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     repository = UserRepository(db_connection)
#     user = repository.find_by_email('hannah@example.com')
#     assert user == User(2, 'Hannah', 'hannah@example.com', '07987654321')

# """
# Test delete a user
# """
# def test_delete_user(db_connection):
#     db_connection.seed("seeds/makersbnb_database.sql")

#     repository = UserRepository(db_connection)
#     user = repository.delete(1)
#     assert repository.all() == [
#         User(2, 'Hannah', 'hannah@example.com', '07987654321')
#     ]

