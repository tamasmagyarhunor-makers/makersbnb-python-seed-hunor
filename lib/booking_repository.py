from lib.booking import Booking

# todo
# what else is needed here for MVP?


class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_all_bookings(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        bookings = []

        for row in rows:
            item = Booking(row['id'], row['user_id'], row['space_id'], row['start_date'], row['end_date'], row['status'])
            bookings.append(item)
        return bookings
    
    def make_booking(self, new_booking):
        self._connection.execute(
            'INSERT INTO bookings (user_id, space_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)',
            [new_booking.user_id, new_booking.space_id, new_booking.start_date, new_booking.end_date, new_booking.status]
        )


    def get_booking_by_booking_id(self, booking_id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [booking_id])
        
        if not rows:
            return None
        row = rows[0]
        return Booking(row['id'], row['user_id'], row['space_id'], row['start_date'], row['end_date'], row['status'])


