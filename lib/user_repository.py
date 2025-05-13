from lib.user import User

class UserRepository:
    def __init__(self,connection):
        self._connection = connection
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row['id'],row['username'],row['password'],row['email_address'])
            users.append(item)

        return users