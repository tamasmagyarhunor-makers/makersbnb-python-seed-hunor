from lib.user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * FROM users')
        return [
            User(row['id'],row['user_name'], row['password'], row['email'],row['phone']) for row in rows
        ]

    def create(self, user):
        rows = self._connection.execute('INSERT INTO users ( user_name, password, email, phone ) VALUES ( %s, %s, %s, %s )', [ user.user_name, user.password, user.email, user.phone ] )
        return None
    
    def find(self, id):
        rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [ id ])
        row = rows[0]
        return User(row['id'],row['user_name'], row['password'], row['email'],row['phone'])

    def find_by_email(self, email):
        rows = self._connection.execute('SELECT * FROM users WHERE email = %s', [ email ])
        row = rows[0]
        return User(row['id'],row['user_name'], row['password'], row['email'],row['phone'])

    def delete(self,id):
        rows = self._connection.execute('DELETE FROM users WHERE id = %s', [ id ])
        return None