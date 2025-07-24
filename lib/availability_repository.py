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
        self._connection.execute(
            'INSERT INTO availabilities (space_id, available_from, available_to) VALUES (%s, %s, %s)',
            [availability.space_id, availability.available_from, availability.available_to]
        )
    
    def find(self, space_id):
        rows = self._connection.execute('SELECT * from availabilities WHERE space_id = %s', [space_id])
        return [
        Availability(row["id"], row["space_id"], row["available_from"], row["available_to"])
        for row in rows
        ]