from datetime import date

class Booking:
    def __init__(self, id, user_id, space_id, booking_date, status):
        self.id = id
        self.user_id = user_id
        self.space_id = space_id
        self.booking_date = booking_date
        self.status = status

    def __repr__(self):
        return f"Booking({self.id}, {self.user_id}, {self.space_id}, {str(self.booking_date)}, {self.status})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__