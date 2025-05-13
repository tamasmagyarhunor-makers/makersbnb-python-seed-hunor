#password validator
#finding email, ect.
#handles connection between user and database

from lib.user import *
from lib.database_connection import *
from flask import Flask
from flask_bcrypt import Bcrypt


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all (self):
        rows = self._connection.execute("SELECT * FROM user_table")
        users = []
        for row in rows :
            person = User(
                row["id"], 
                row["name"], 
                row["email"], 
                row["password"],
                row["phone_number"])
            users.append(person)
        return users
    
    #create password here

    def create(self, user):
        self._connection.execute(
            'INSERT INTO user_table (name, email, password, phone_number) VALUES (%s, %s, %s, %s)',
            [user.name.title(), user.email.lower(), user.password, user.phone_number]
    )