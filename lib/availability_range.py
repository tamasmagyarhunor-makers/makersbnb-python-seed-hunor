import datetime, timedelta

class AvailabilityRange:
    def __init__(self,id,start_date,end_date,space_id):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.space_id = space_id

    def __repr__(self):
        return f'AvailableRange({self.id}, {self.start_date}, {self.end_date}, {self.space_id})'
    
    def __eq__ (self,other):
        return self.__dict__ == other.__dict__
    
    def available_days(self):
        start_datetime = datetime.datetime.strptime(self.start_date,'%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(self.end_date,'%Y-%m-%d')

        current_datetime = start_datetime

        diff_days = (end_datetime-start_datetime).days

        dayslist = []

        while (diff_days+1) > 0:
            dayslist.append(current_datetime)
            current_datetime += datetime.timedelta(days=1)
            diff_days -= 1

        dayslist_string = []

        for day in dayslist:
            day_string = day.strftime('%Y-%m-%d')
            dayslist_string.append(day_string)

        return dayslist_string



