from lib.space import Space
from lib.availability_range import AvailabilityRange

class SpaceRepository():
    def __init__(self,connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT \
            spaces.*, users.id AS user_id, \
            users.email_address AS host_email \
            FROM spaces \
            JOIN users ON spaces.host_id = users.id')
        spaces = []
        for row in rows:
            space = Space(row['id'],
                        row['name'],
                        row['description'],
                        row['price_per_night'],
                        row['host_id'])
            space.host_email = row['host_email']
            spaces.append(space)

        return spaces

        
    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * from spaces WHERE id = %s',[id])
        row = rows[0]

        return Space(row['id'],row['name'],row['description'],row['price_per_night'],row['host_id'])
    
    def create(self,name,description,price_per_night,host_id):
        self._connection.execute('INSERT INTO spaces (name,description,price_per_night,host_id) VALUES (%s,%s,%s,%s)',[name,description,price_per_night,host_id])

    def update(self,id,key,new_value):
        if key == 'name':
            self._connection.execute("UPDATE spaces SET name = %s WHERE id = %s",[new_value,id])
        if key == 'description':
            self._connection.execute("UPDATE spaces SET description = %s WHERE id = %s",[new_value,id])
        if key == 'price_per_night':
            self._connection.execute("UPDATE spaces SET price_per_night = %s WHERE id = %s",[new_value,id])
        if key == 'host_id':
            self._connection.execute("UPDATE spaces SET host_id = %s WHERE id = %s",[new_value,id])

        else:
            return 'Invalid Key'
        
    def delete(self,id):
        self._connection.execute('DELETE FROM spaces WHERE id = %s',[id])

    def available_days_by_id(self,id):
        available_days_string = []
        avail_rows = self._connection.execute('SELECT * from availability_ranges WHERE space_id = %s',[id])

        for row in avail_rows:
            avail_range = AvailabilityRange(row['id'],row['start_date'],row['end_date'],row['space_id'])
            avail_days = avail_range.available_days()
            for day in avail_days:
                available_days_string.append(day)
        return available_days_string
