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
    
    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * from users WHERE id = %s',[id])
        row = rows[0]

        return User(row['id'],row['username'],row['password'],row['email_address'])
    
    def create(self,username,password,email_address):
        self._connection.execute('INSERT INTO users (username,password,email_address) VALUES (%s,%s,%s)',[username,password,email_address])

    def delete(self,id):
        self._connection.execute('DELETE FROM users WHERE id = %s',[id])