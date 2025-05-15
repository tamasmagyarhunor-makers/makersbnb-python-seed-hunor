from lib.user_repository import UserRepository
from lib.user import User

"""
Test get all users
"""
def test_user_repository_all(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = UserRepository(db_connection)
    assert repository.all() == [
        User(1, 'Bridget', 'qwerty', 'bridget@example.com', '07402498078'),
        User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321')
    ]

"""
Test add in a user
"""
def test_create_user(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = UserRepository(db_connection)
    user = User(None, "Tim", '098765', "tim@example.com", "0118118118118")
    repository.create(user)
    result = repository.all()
    assert repository.all() == [
        User(1, 'Bridget', 'qwerty', 'bridget@example.com', '07402498078'),
        User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321'),
        User(3, 'Tim', '098765', 'tim@example.com', '0118118118118')
    ]

"""
Test finding a user by id
"""
def test_finding_a_user_by_id(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = UserRepository(db_connection)
    user = repository.find(2)
    assert user == User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321')

"""
Test finding a user by email
"""
def test_finding_a_user_by_email(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = UserRepository(db_connection)
    user = repository.find_by_email('hannah@example.com')
    assert user == User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321')

"""
Test delete a user
"""
def test_delete_user(db_connection):
    db_connection.seed("seeds/makersbnb_database.sql")

    repository = UserRepository(db_connection)
    user = repository.delete(1)
    assert repository.all() == [
        User(2, 'Hannah', '123456', 'hannah@example.com', '07987654321')
    ]

