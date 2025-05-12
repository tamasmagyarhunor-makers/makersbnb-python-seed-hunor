from lib.user import *

def test_user_constructs():
    user = User(1,'Johnnyboy','john123','john@gmail.com')

    assert user.id == 1
    assert user.username == 'Johnnyboy'
    assert user.password == 'john123'
    assert user.email == 'john@gmail.com'