from lib.user import User

class UserRepository:
    def __init__(self,connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row['id'],row['name'],row['password'],row['email_address'])
            users.append(item)

        return users
    
    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * from users WHERE id = %s',[id])
        row = rows[0]

        return User(row['id'],row['name'],row['password'],row['email_address'])
    
    def create(self,name,password,email_address):
        self._connection.execute('INSERT INTO users (name,password,email_address) VALUES (%s,%s,%s)',[name,password,email_address])

    def delete(self,id):
        self._connection.execute('DELETE FROM users WHERE id = %s',[id])

    def update(self,id,key,new_value):
        
        if key == 'password':
            self._connection.execute("UPDATE users SET password = %s WHERE id = %s",[new_value,id])
        if key == 'email_address':
            self._connection.execute("UPDATE users SET email_address = %s WHERE id = %s",[new_value,id])

        else:
            return 'Invalid Key'
        

