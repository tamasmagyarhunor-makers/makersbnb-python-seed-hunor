from lib.space import Space

class SpaceRepository():

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []
        for row in rows:
            item = Space(row["id"], row["name"], row["description"], row['price_per_night'], row['user_id'])
            spaces.append(item)
        return spaces

    def create(self, space):
        self._connection.execute(
            'INSERT INTO spaces (name, description, price_per_night, user_id) VALUES (%s, %s, %s, %s)',
            [space.name, space.description, space.price_per_night, space.user_id]
        )

