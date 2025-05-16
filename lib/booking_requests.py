class BookingRequest:
    def __init__(self,id,start_date,end_date,space_id,user_id):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.space_id = space_id
        self.user_id = user_id

    def __repr__(self):
        return f'Booking Request({self.id}, {self.start_date}, {self.end_date}, {self.space_id}, {self.user_id})'
    
    def __eq__ (self,other):
        return self.__dict__ == other.__dict__