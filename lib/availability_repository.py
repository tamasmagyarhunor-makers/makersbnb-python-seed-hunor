from datetime import date
from lib.availability import *

class AvailabilityRepository():

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM availabilities')
        availabilities = []
        for row in rows:
            item = Availability(row["id"], row["space_id"], row["available_from"], row["available_to"])
            availabilities.append(item)
        return availabilities

    def create(self, availability):
        # This returns a list of dicts, e.g. [{'id': 5}]
        rows = self._connection.execute(
            'INSERT INTO availabilities (space_id, available_from, available_to) '
            'VALUES (%s, %s, %s) RETURNING id;',
            [availability.space_id, availability.available_from, availability.available_to]
        )
        new_id = rows[0]['id']
        availability.id = new_id
        return availability

    def find(self, space_id):
        rows = self._connection.execute('SELECT * from availabilities WHERE space_id = %s', [space_id])
        return [
        Availability(row["id"], row["space_id"], row["available_from"], row["available_to"])
        for row in rows
        ]
    
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * from availabilities WHERE id = %s', [id])
        return [
        Availability(row["id"], row["space_id"], row["available_from"], row["available_to"])
        for row in rows
        ]