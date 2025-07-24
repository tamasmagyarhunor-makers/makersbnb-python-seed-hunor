class Booking:
    def __init__(self, id, user_id, space_id, start_date, end_date):
        self.id = id
        self.user_id = user_id
        self.space_id = space_id
        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.id}, {self.user_id}, {self.space_id}, {self.start_date}, {self.end_date})"
