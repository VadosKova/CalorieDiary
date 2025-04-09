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

    def register_user(self):
        self.cursor.execute('INSERT INTO Users (Username, Email, Password, Gender, Age, Weight, Height, Goal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (self.username, self.email, self.password, self.gender, self.age, self.weight, self.height, self.goal))
        self.conn.commit()

    def check_login(self, input_password):
        self.cursor.execute('SELECT Password FROM Users WHERE Username = ?', (self.username,))
        result = self.cursor.fetchone()

        if not result:
            return False

        stored_password = result[0]
        return stored_password == input_password

    def check_username_exists(self):
        self.cursor.execute('SELECT * FROM Users WHERE Username = ?', (self.username,))
        return self.cursor.fetchone() is not None

    def add_meal(self, product_name, weight, caloric_value):
        self.cursor.execute('INSERT INTO Meals (UserId, ProductName, Weight, CaloricValue) VALUES ((SELECT UserId FROM Users WHERE Username = ?), ?, ?, ?)', (self.username, product_name, weight, caloric_value))
        self.conn.commit()

        self.cursor.execute('INSERT INTO History (UserId, Type, Date) VALUES ((SELECT UserId FROM Users WHERE Username = ?), ?, GETDATE())', (self.username, 'meal'))
        self.conn.commit()

    def add_activity(self, calories_burned, activity_date):
        self.cursor.execute('INSERT INTO Activity (UserId, CalorieIntake, ActivityDate) VALUES ((SELECT UserId FROM Users WHERE Username = ?), ?, ?)', (self.username, calories_burned, activity_date))
        self.conn.commit()

        self.cursor.execute('INSERT INTO History (UserId, Type, Date) VALUES ((SELECT UserId FROM Users WHERE Username = ?), ?, GETDATE())', (self.username, 'activity'))
        self.conn.commit()