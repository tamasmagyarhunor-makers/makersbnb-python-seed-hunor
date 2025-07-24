from datetime import date

class Availability:
    def __init__(self, id, space_id, available_from:date, available_to:date):
        if available_from > available_to:
            raise ValueError("available_from cannot be after available_to")
        self.id = id
        self.space_id = space_id
        self.available_from = available_from
        self.available_to = available_to
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Availability({self.id}, {self.space_id}, {self.available_from}, {self.available_to})"
    
    def is_valid(self):
        return self.space_id is not None and self.available_from is not None and self.available_to is not None
    
    def is_date_in_range(self, booking_start_date, booking_end_date):
        return self.available_from <= booking_start_date and self.available_to >= booking_end_date