class User:
    def __init__(self, id, name, email, password ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email})"
    
    
    # Leave for later for added complexity
    def is_valid(self):
        pass

    def generate_errors(self):
        pass