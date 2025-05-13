from lib.user_repository import *

def test_get_all_users(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    assert repository.all() == [
        User(1,'sashaparkes', 'mypassword1234', 'sashaparkes@email.com'),
        User(2,'jamesdismore', 'mypassword54321', 'jamesdismore@email.com')
    ]

def test_get_by_id(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    assert repository.find_by_id(1) == User(1,'sashaparkes', 'mypassword1234', 'sashaparkes@email.com')
    assert repository.find_by_id(2) == User(2,'jamesdismore', 'mypassword54321', 'jamesdismore@email.com')