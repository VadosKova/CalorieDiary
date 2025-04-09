import socket
import jsonpickle
import pyodbc

class User:
    def __init__(self, username=None, email=None, password=None, gender=None, age=None, weight=None, height=None, goal=None, activity_level=None):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.goal = goal
        self.activity_level = activity_level

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

    def get_user_meals(self):
        self.cursor.execute('SELECT ProductName, Weight, CaloricValue FROM Meals WHERE UserId = (SELECT UserId FROM Users WHERE Username = ?)', (self.username,))
        return self.cursor.fetchall()

    def get_user_activities(self):
        self.cursor.execute('SELECT CalorieIntake, ActivityDate FROM Activity WHERE UserId = (SELECT UserId FROM Users WHERE Username = ?)', (self.username,))
        return self.cursor.fetchall()

    def get_user_history(self):
        self.cursor.execute('SELECT Type, Date FROM History WHERE UserId = (SELECT UserId FROM Users WHERE Username = ?) ORDER BY Date DESC', (self.username,))
        return self.cursor.fetchall()

    def get_user_data(self):
        self.cursor.execute('SELECT Gender, Age, Weight, Height FROM Users WHERE Username = ?', (self.username,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def calculate_bmr(self):
        user_data = self.get_user_data()

        if not user_data:
            return "User data not found"

        gender, age, weight, height = user_data

        if gender == 'M':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == 'F':
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            return "Error"

        activity_level = 'low'
        activity_factor = 1.2

        self.cursor.execute('SELECT ActivityLevel FROM Users WHERE Username = ?', (self.username,))
        activity_level_from_db = self.cursor.fetchone()

        if activity_level_from_db:
            activity_level = activity_level_from_db[0]
            if activity_level == 'low':
                activity_factor = 1.2
            elif activity_level == 'medium':
                activity_factor = 1.55
            elif activity_level == 'high':
                activity_factor = 1.9
            else:
                return "Error"

        total_calories = bmr * activity_factor

        self.cursor.execute('UPDATE Users SET ActivityLevel = ? WHERE Username = ?', (activity_level, self.username))
        self.conn.commit()

        return total_calories

    def close_connection(self):
        self.conn.close()


def client_request(client):
    req = client.recv(4096).decode('utf-8')
    data = jsonpickle.decode(req)

    if data['action'] == 'register':
        user = User(username=data['username'], email=data['email'], password=data['password'], gender=data['gender'], age=data['age'], weight=data['weight'], height=data['height'], goal=data['goal'])

        if user.check_username_exists():
            res = {"message": "Username already registered"}
        else:
            user.register_user()
            res = {"message": "Registration successful"}
    elif data['action'] == 'login':
        user = User(username=data['username'])
        if user.check_login(data['password']):
            res = {"message": "Login successful"}
        else:
            res = {"message": "Invalid credentials"}

    elif data['action'] == 'add_meal':
        user = User(username=data['username'])
        user.add_meal(data['product_name'], data['weight'], data['caloric_value'])
        res = {"message": "Meal added successfully"}

    elif data['action'] == 'add_activity':
        user = User(username=data['username'])
        user.add_activity(data['calories_burned'], data['activity_date'])
        res = {"message": "Activity added successfully"}

    elif data['action'] == 'get_user_meals':
        user = User(username=data['username'])
        meals = user.get_user_meals()
        res = {"meals": meals}

    elif data['action'] == 'get_user_activities':
        user = User(username=data['username'])
        activities = user.get_user_activities()
        res = {"activities": activities}

    elif data['action'] == 'get_user_history':
        user = User(username=data['username'])
        history = user.get_user_history()
        res = {"history": history}

    elif data['action'] == 'calculate_bmr':
        user = User(username=data['username'])
        total_calories = user.calculate_bmr()
        if isinstance(total_calories, str):  # ошибка
            res = {"error": total_calories}
        else:
            res = {"total_calories": total_calories}

    client.send(jsonpickle.encode(res).encode('utf-8'))
    client.close()


IP = '127.0.0.1'
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)
print("Сервер запущен...")

while True:
    client, addr = server.accept()
    print(f"Подключение от {addr}")
    client_request(client)