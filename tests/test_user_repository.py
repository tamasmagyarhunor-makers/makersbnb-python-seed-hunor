from lib.user_repository import *

def test_get_all_users(db_connection):
    db_connection.seed('seeds/makersbnb_seed.sql')
    repository = UserRepository(db_connection)

    assert repository.all() == [
        User(1,'sashaparkes', 'mypassword1234', 'sashaparkes@email.com')
    ]