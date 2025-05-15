from lib.space import Space
from lib.availability_range import AvailabilityRange
from lib.booking import Booking
import datetime, timedelta

class SpaceRepository():
    def __init__(self, connection):
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
                        row['image_url'],
                        row['host_id'])
            space.host_email = row['host_email']
            spaces.append(space)

        return spaces

        
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * from spaces WHERE id = %s',[id])
        row = rows[0]

        return Space(row['id'],row['name'],row['description'],row['price_per_night'], row['image_url'], row['host_id'])
    
    def create(self, new_space):
        rows = self._connection.execute('INSERT INTO spaces (name,description,price_per_night,image_url,host_id) VALUES (%s,%s,%s,%s,%s) RETURNING id',
                                [new_space.name,
                                new_space.description,
                                new_space.price_per_night,
                                new_space.image_url,
                                new_space.host_id])
        row = rows[0]
        new_space.id = row['id']
        return new_space

    def update(self, id, key, new_value):
        if key == 'name':
            self._connection.execute("UPDATE spaces SET name = %s WHERE id = %s",[new_value,id])
        if key == 'description':
            self._connection.execute("UPDATE spaces SET description = %s WHERE id = %s",[new_value,id])
        if key == 'price_per_night':
            self._connection.execute("UPDATE spaces SET price_per_night = %s WHERE id = %s",[new_value,id])
        if key == 'image_url':
            self._connection.execute("UPDATE spaces SET image_url = %s WHERE id = %s",[new_value,id])
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
    
    def booked_days_by_id(self,id):
        booked_days_string = []

        booked_rows = self._connection.execute('SELECT * from bookings WHERE space_id = %s',[id])
        print(booked_rows)
        for row in booked_rows:
            booked_range = Booking(row['id'],row['start_date'],row['end_date'],row['space_id'],row['user_id'])
            print(booked_range)
            booked_days = booked_range.booked_days()
            for day in booked_days:
                booked_days_string.append(day)
                print(booked_days_string)
        return booked_days_string
    
    def booking_check(self,space_id,start_date,end_date):
        start_datetime = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_date,'%Y-%m-%d')

        current_datetime = start_datetime

        diff_days = (end_datetime-start_datetime).days

        dayslist = []

        while (diff_days+1) > 0:
            dayslist.append(current_datetime)
            current_datetime += datetime.timedelta(days=1)
            diff_days -= 1

        test_days = []

        for day in dayslist:
            day_string = day.strftime('%Y-%m-%d')
            test_days.append(day_string)
        


        avail_days = self.available_days_by_id(space_id)

        for day in test_days:
            if day not in avail_days:
                return 'not available'
            
        booked_days = self.booked_days_by_id(space_id)

        for day in test_days:
            if day in booked_days:
                return 'already booked'
            
        return 'safe'

    def get_available_unbooked_spaces(self,start_date,end_date):
        available_spaces = []
        rows = self._connection.execute('SELECT * from spaces')
        for row in rows:
            space = Space(row['id'],
                        row['name'],
                        row['description'],
                        row['price_per_night'],
                        row['image_url'],
                        row['host_id'])
            if self.booking_check(space.id,start_date,end_date) == 'safe':
                available_spaces.append(space)
        
        return available_spaces