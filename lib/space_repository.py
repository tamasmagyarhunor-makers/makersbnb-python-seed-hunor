from lib.space import Space

class SpaceRepository:
    def __init__(self, _connection):
        self._connection = _connection

    def list_spaces(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []

        for row in rows:
            item = Space(row['space_id'], row['name'], row['description'], row['price_per_night'], row['user_id'])
            spaces.append(item)
        return spaces

    def add_space(self, space):
        self._connection.execute(
            'INSERT INTO spaces (name, description, price_per_night, user_id) VALUES (%s, %s, %s, %s)',
            [space.name, space.description, space.price_per_night, space.user_id])
        return None

    # def find(self, space_id):
    #     rows = self._connection.execute(
    #         'SELECT * from spaces WHERE space_id = %s', [space_id])
    #     row = rows[0]
    #     return Space(row["space_id"], row["name"], row["description"], row["price_per_night"], row["user_id"])