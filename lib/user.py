class User:
    def __init__(self,id,username,password,email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.password}, {self.email})'
    
    def __eq__(self,other):
        return self.__dict__ == other.__dict__