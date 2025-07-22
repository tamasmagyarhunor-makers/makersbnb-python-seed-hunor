from lib.user_repository import UserRepository
from lib.user import User

"""
When we call UserRepository#all
We get a list of User objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    users = repository.all()

    assert users == [
        User(1, "Alice", "alice@example.com", "password1"),
        User(2, "Bob", "bob@example.com", "password2"),
    ]

"""
When we call UserRepository#find
We get a single User object reflecting the seed data
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    user = repository.find(1)
    assert user == User(1, "Alice", "alcie@example.com", "password1")

"""
When we call UserRepository#create
We get a new record in the database.
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)
    created_user = repository.create(User(None, "Charlie", "charlie@example.com", "password3"))
    assert created_user == User


"""
When we call UserRepository#delete
We remove a record from the database.
"""