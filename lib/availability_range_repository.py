from lib.availability_range import AvailabilityRange

class AvailabilityRangeRepository():
    def __init__(self,connection):
        self._connection = connection

    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * FROM availability_ranges WHERE id = %s',[id])
        row = rows[0]

        return AvailabilityRange(row['id'],row['start_date'],row['end_date'],row['space_id'])