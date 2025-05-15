from lib.space import Space

class SpaceRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        return [
            Space(row['id'],row['space_name'],row['spaces_description'],row['price_per_night'],row['available_from_date'],row['available_to_date'],row['user_id']) for row in rows
        ]

    def create(self, space):
        rows = self._connection.execute('INSERT INTO spaces (space_name, spaces_description, price_per_night, available_from_date, available_to_date, user_id ) VALUES ( %s, %s, %s, %s, %s, %s )', 
                                        [space.space_name, space.spaces_description, space.price_per_night, space.available_from_date, space.available_to_date, space.user_id])
        return None
    
    # def find(self, id):
    #     rows = self._connection.execute('SELECT * FROM spaces WHERE id = %s', [ id ])
    #     row = rows[0]
    #     return Space(row['id'],row['space_name'],row['spaces_description'],row['price_per_night'],row['available_from_date'],row['available_to_date'],row['user_id'])

    # def find_by_name(self, space_name):
    #     rows = self._connection.execute('SELECT * FROM spaces WHERE space_name = %s', [ space_name ])
    #     row = rows[0]
    #     return Space(row['id'],row['space_name'],row['spaces_description'],row['price_per_night'],row['available_from_date'],row['available_to_date'],row['user_id'])

    # def delete(self,id):
    #     rows = self._connection.execute('DELETE FROM spaces WHERE id = %s', [ id ])
    #     return None