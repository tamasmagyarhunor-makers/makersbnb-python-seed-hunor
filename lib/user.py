class User:
    def __init__(self, id, name, email, password, phone_number):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email}, {self.password}, {self.phone_number})"