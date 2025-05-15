from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id, user_name, password, email, phone):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"User({self.id}, {self.user_name}, {self.password}, {self.email}, {self.phone})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__