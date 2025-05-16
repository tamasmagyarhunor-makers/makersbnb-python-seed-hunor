from lib.booking import Booking
from lib.space_repository import *

class BookingRepository:
    def __init__(self,connection):
        self._connection = connection

    def find_by_space_id(self,id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE space_id = %s',[id])

        results = []

        for row in rows:
            results.append(Booking(row['id'],row['start_date'],row['end_date'],row['space_id'],row['user_id']))
        
        return results
    
    def add_booking(self,start_date,end_date,space_id,user_id):
        spacerepo = SpaceRepository(self._connection)
        check = spacerepo.booking_check(space_id,start_date,end_date)

        if check != 'safe':
            return check

        self._connection.execute('INSERT INTO bookings (start_date,end_date,space_id,user_id) VALUES (%s,%s,%s,%s)',[start_date,end_date,space_id,user_id])