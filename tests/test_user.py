from lib.user import *

def test_user_constructs():
    user = User(1,'Johnnyboy','john123','john@gmail.com')

    assert user.id == 1
    assert user.username == 'Johnnyboy'
    assert user.password == 'john123'
    assert user.email == 'john@gmail.com'

def test_user_format():
    user = User(1,'Johnnyboy','john123','john@gmail.com')
    assert str(user)=='User(1, Johnnyboy, john123, john@gmail.com)'

def test_users_are_equal():
    user1 = User(1,'Johnnyboy','john123','john@gmail.com')
    user2 = User(1,'Johnnyboy','john123','john@gmail.com')
    user3 = User(1,'Johnnydfdboy','joddhn123','johnd@gmail.com')

    assert user1 == user2
    assert user1 != user3