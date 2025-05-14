class Booking:
    def __init__(self,id,start_date,end_date,user_id):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id

    def __repr__(self):
        return f'Booking({self.id}, {self.start_date}, {self.end_date}, {self.user_id})'
    
    def __eq__ (self,other):
        return self.__dict__ == other.__dict__