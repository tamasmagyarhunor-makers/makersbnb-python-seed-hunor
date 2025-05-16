from lib.availability_range import AvailabilityRange

class AvailabilityRangeRepository():
    def __init__(self,connection):
        self._connection = connection

    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * FROM availability_ranges WHERE id = %s',[id])
        row = rows[0]

        return AvailabilityRange(row['id'],row['start_date'],row['end_date'],row['space_id'])
    
    def find_by_space_id(self,space_id):
        rows = self._connection.execute('SELECT * FROM availability_ranges WHERE space_id = %s',[space_id])
        avail_ranges_list = []
        for row in rows:
            item = AvailabilityRange(row['id'],row['start_date'],row['end_date'],row['space_id'])
            avail_ranges_list.append(item)

        return avail_ranges_list
    
    def add_range(self,start_date,end_date,space_id):
        self._connection.execute('INSERT INTO availability_ranges (start_date,end_date,space_id) VALUES (%s,%s,%s)',
                                [start_date,
                                end_date,
                                space_id])
    
    