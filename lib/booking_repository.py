from datetime import date
from lib.booking import Booking

class BookingRepository:
    def __init__(self,connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        return [ Booking(row['id'], row['user_id'], row['space_id'], row['booking_date'], row['status']) for row in rows ]
    
    def find(self, id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [ id ])

        if len(rows) == 0:
            return None

        row = rows[0]
        return Booking(row['id'], row['user_id'], row['space_id'], row['booking_date'], row['status'])
    
    def add(self,booking):
        self._connection.execute('INSERT INTO bookings ( user_id, space_id, booking_date, status ) VALUES ( %s, %s, %s, %s )', [ booking.user_id, booking.space_id, booking.booking_date, booking.status ])
    
    def update_status(self,id,status):
        self._connection.execute('UPDATE bookings SET status = %s WHERE id = %s', [ status, id ])
    
    def find_for_space(self,space):
        rows = self._connection.execute('SELECT * FROM bookings WHERE space_id = %s', [ space ])
        return [ Booking(row['id'], row['user_id'], row['space_id'], row['booking_date'], row['status']) for row in rows ]