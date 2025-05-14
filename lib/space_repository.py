from lib.space import Space

class SpaceRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        return [
            Space(row['id'],row['space_name'],row['spaces_description'],row['price_per_night'],row['available_from_date'],row['available_to_date'],row['user_id']) for row in rows
        ]


        

    # def create(self, user):
    #     rows = self._connection.execute('INSERT INTO users ( user_name, email, phone ) VALUES ( %s, %s, %s )', [ user.user_name, user.email, user.phone ] )
    #     return None
    
    # def find(self, id):
    #     rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [ id ])
    #     row = rows[0]
    #     return User(row['id'],row['user_name'],row['email'],row['phone'])

    # def find_by_email(self, email):
    #     rows = self._connection.execute('SELECT * FROM users WHERE email = %s', [ email ])
    #     row = rows[0]
    #     return User(row['id'],row['user_name'],row['email'],row['phone'])

    # def delete(self,id):
    #     rows = self._connection.execute('DELETE FROM users WHERE id = %s', [ id ])
    #     return None