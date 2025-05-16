from lib.user_repository import *

def test_password_stuff(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    repository.create(User(1,'Test','testpw','test@email.com'))

    user = repository.find_by_id(3)
    print(user)

    assert 1 == 2

