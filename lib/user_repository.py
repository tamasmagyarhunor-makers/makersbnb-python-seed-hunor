from lib.user import User
from lib.password_hashing_and_validation import *

class UserRepository:
    def __init__(self,connection):
        self._connection = connection


    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:

            item = User(row['id'],
                        row['name'],
                        row['password'],
                        row['email_address'])

            users.append(item)

        return users
    

    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * from users WHERE id = %s',[id])
        row = rows[0]

        return User(row['id'],row['name'],row['password'],row['email_address'])
    
    #find by email function for log in page
    def find_by_email(self, email_address):
        rows = self._connection.execute('SELECT * from users WHERE email_address = %s',[email_address])
        
        if not rows:
            return None
        row = rows[0]

        return User(row['id'],row['name'],row['password'],row['email_address'])
    

    def create(self, new_user):
        print(new_user.password)
        hashed_password = hash_password(new_user.password)
        print(hashed_password)
        string_hash = hashed_password.decode('utf-8')
        rows = self._connection.execute('INSERT INTO users (name,password,email_address) VALUES (%s,%s,%s) RETURNING id',
                                [new_user.name,
                                string_hash,
                                new_user.email_address])
        row = rows[0]
        new_user.id = row['id']
        return new_user


    def delete(self, id):
        self._connection.execute('DELETE FROM users WHERE id = %s',[id])


    def update(self, id, key, new_value):

        
        if key == 'password':
            hashed_password = hash_password(new_value)
            self._connection.execute("UPDATE users SET password = %s WHERE id = %s",[hashed_password,id])
        if key == 'email_address':
            self._connection.execute("UPDATE users SET email_address = %s WHERE id = %s",[new_value,id])

        else:
            return 'Invalid Key'
        

