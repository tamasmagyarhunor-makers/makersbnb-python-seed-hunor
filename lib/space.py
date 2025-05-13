class Space:
    def __init__(self, id, name, description, price_per_night, host_id, host_email=None):
        self.id = id
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.host_id = host_id
        self.host_email = host_email
    def __repr__(self):
        return f'Space({self.id}, {self.name}, {self.description}, \
            £{self.price_per_night}/night, {self.host_id}, {self.host_email})'

    def __eq__(self,other):
        return self.__dict__ == other.__dict__