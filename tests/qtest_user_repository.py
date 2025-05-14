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

def test_create_user(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)
    repository.create('johndoe','johnspassword','johndoe@email.com')

    assert repository.find_by_id(3) == User(3,'johndoe','johnspassword','johndoe@email.com')

def test_delete_user(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    repository.delete(1)

    assert repository.all() == [
        User(2,'jamesdismore', 'mypassword54321', 'jamesdismore@email.com')
    ]

def test_update_user(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    repository.update(1,'password','superpassword1234')

    assert repository.find_by_id(1) == User(1,'sashaparkes', 'superpassword1234', 'sashaparkes@email.com')
    assert repository.all() == [
        User(2,'jamesdismore', 'mypassword54321', 'jamesdismore@email.com'),
        User(1,'sashaparkes', 'superpassword1234', 'sashaparkes@email.com')
    ]