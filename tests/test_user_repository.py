from lib.user_repository import *
from lib.user import *


"""
When we call UserRepository#all
We get a list of User objects reflecting the seed data.
"""
def test_user_repo_starts_empty(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/makersbnb.sql") # Seed our database with some test data
    repository = UserRepository(db_connection) # Create a new ArtistRepository
    user = repository.all() # Get all artists
    assert user == [
        User(1, 'Yahya', 'yahya@makers.com', 'Blahblah1!', '012345678901'),
        User(2, 'Pat', 'pat@makers.com', 'Blahblah2!', '012345678902')
    ]

# """
# When we call UserRepository#all
# We get a list of User objects reflecting the seed data.
# """
# def test_user_repo_starts_all(db_connection):
#     db_connection.seed("seeds/makersbnb.sql") 
#     repository = UserRepository(db_connection) 
#     user = repository.all() 

#     assert user == [
#         User('Yahya', 'yahya@makers.com', 'Blahblah1!', '012345678901'),
#         User('Pat', 'pat@makers.com', 'Blahblah2!', '012345678902')
#     ]

"""
When we call UserRepository#create
We get a new record in the database.
"""

def test_create_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)

    new_user = User(None, 'Peter', 'peter@makers.com', 'Blahblah3!', '12345678903')
    repository.create(new_user)
    result = repository.all()
    user = result[-1]
    assert user.name == 'Peter'
    assert user.email == 'peter@makers.com'
    assert user.password == 'Blahblah3!'
    assert user.phone_number == '12345678903'