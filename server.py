import socket
import jsonpickle
import pyodbc
from datetime import datetime

class User:
    def __init__(self, username=None, email=None, password=None, gender=None, age=None, weight=None, height=None, goal=None):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.goal = goal
        self.connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=CalorieDiary;Trusted_Connection=yes')
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()