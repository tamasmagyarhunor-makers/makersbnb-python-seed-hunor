class Space:
    def __init__(self, id, name, description, price_per_night, image_url, host_id):
        self.id = id
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.image_url = image_url
        self.host_id = host_id

    def __repr__(self):
        return f'Space({self.id}, {self.name}, {self.description}, £{self.price_per_night}/night, {self.image_url}, {self.host_id})'

    def __eq__(self,other):
        if not isinstance(other, Space):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            self.description == other.description and
            self.price_per_night == other.price_per_night and
            self.host_id == other.host_id
            )
    
    def is_valid(self):
        if self.name is None or self.name == "":
            return False
        if self.description is None or self.description == "":
            return False
        if self.price_per_night is None or self.price_per_night == "":
            return False
        if self.host_id is None or self.host_id == "":
            return False
        return True
    
    def generate_errors(self):
        errors = []
        if self.name is None or self.name == "":
            errors.append("Name can't be blank")
        if self.description is None or self.description == "":
            errors.append("Description can't be blank")
        if self.price_per_night is None or self.price_per_night == "":
            errors.append("Price can't be blank")
        if self.host_id is None or self.host_id == "":
            errors.append("Host ID can't be blank")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)