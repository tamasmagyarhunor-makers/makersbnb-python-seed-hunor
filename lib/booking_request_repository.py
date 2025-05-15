from lib.booking_requests import BookingRequest
from lib.space_repository import SpaceRepository

class BookingRequestRepository:
    def __init__(self,connection):
        self._connection = connection

    def find_by_space_id(self,id):
        rows = self._connection.execute('SELECT * FROM booking_requests WHERE space_id = %s',[id])

        results = []

        for row in rows:
            results.append(BookingRequest(row['id'],row['start_date'],row['end_date'],row['space_id'],row['user_id']))
        
        return results

    def add_booking_request(self,start_date,end_date,space_id,user_id):
        spacerepo = SpaceRepository(self._connection)
        check = spacerepo.booking_check(space_id,start_date,end_date)

        if check != 'safe':
            return check

        self._connection.execute('INSERT INTO booking_requests (start_date,end_date,space_id,user_id) VALUES (%s,%s,%s,%s)',[start_date,end_date,space_id,user_id])

    def delete_by_id(self,id):
        self._connection.execute('DELETE FROM booking_requests WHERE id = %s',[id])