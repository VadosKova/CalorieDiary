from tkinter import *
from tkinter import messagebox
import socket
import jsonpickle

IP = '127.0.0.1'
PORT = 4000

class CalorieDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Diary")
        self.root.geometry("600x400")

        self.root.configure(bg='#f0f0f0')
        self.button_font = ('Arial', 10)
        self.label_font = ('Arial', 10)
        self.header_font = ('Arial', 14, 'bold')

        self.current_user = None

        self.start_screen()

    def start_screen(self):
        self.clear_widgets()

        Label(self.root, text="Calorie Diary", font=self.header_font, bg='#f0f0f0').pack(pady=20)

        Label(self.root, text="Username:", font=self.label_font, bg='#f0f0f0').pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        Label(self.root, text="Password:", font=self.label_font, bg='#f0f0f0').pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        Button(self.root, text="Login", font=self.button_font, command=self.login).pack(pady=10)
        Button(self.root, text="Register", font=self.button_font, command=self.register_screen).pack()

    def register_screen(self):
        self.clear_widgets()

        Label(self.root, text="Register New Account", font=self.header_font, bg='#f0f0f0').pack(pady=10)

        fields = [
            ("Username:", "reg_username"),
            ("Email:", "reg_email"),
            ("Password:", "reg_password"),
            ("Confirm Password:", "reg_confirm_password"),
            ("Gender (M/F):", "reg_gender"),
            ("Age:", "reg_age"),
            ("Weight (kg):", "reg_weight"),
            ("Height (cm):", "reg_height"),
            ("Goal:", "reg_goal")
        ]

        self.register_entries = {}

        for label, name in fields:
            Label(self.root, text=label, font=self.label_font, bg='#f0f0f0').pack()
            entry = Entry(self.root)
            if "password" in name:
                entry.config(show="*")
            entry.pack()
            self.register_entries[name] = entry

        Button(self.root, text="Register", font=self.button_font, command=self.register).pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.start_screen).pack()

    def main_menu(self):
        self.clear_widgets()

        Label(self.root, text=f"Welcome, {self.current_user}!", font=self.header_font, bg='#f0f0f0').pack(pady=20)

        buttons = [
            ("Add Meal", self.add_new_meal),
            ("Add Activity", self.add_new_activity),
            ("View Meals", self.show_meals),
            ("View Activities", self.show_activities),
            ("View History", self.show_history),
            ("Calculate Daily Calories", self.calculate_bmr),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            Button(self.root, text=text, font=self.button_font, command=command).pack(pady=5)

    def add_new_meal(self):
        self.clear_widgets()

        Label(self.root, text="Add New Meal", font=self.header_font, bg='#f0f0f0').pack(pady=10)

        Label(self.root, text="Product Name:", font=self.label_font, bg='#f0f0f0').pack()
        self.meal_name_entry = Entry(self.root)
        self.meal_name_entry.pack()

        Label(self.root, text="Weight (g):", font=self.label_font, bg='#f0f0f0').pack()
        self.meal_weight_entry = Entry(self.root)
        self.meal_weight_entry.pack()

        Label(self.root, text="Caloric Value (kcal):", font=self.label_font, bg='#f0f0f0').pack()
        self.meal_calories_entry = Entry(self.root)
        self.meal_calories_entry.pack()

        Button(self.root, text="Add Meal", font=self.button_font, command=self.add_meal).pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.main_menu).pack()

    def add_new_activity(self):
        self.clear_widgets()

        Label(self.root, text="Add New Activity", font=self.header_font, bg='#f0f0f0').pack(pady=10)

        Label(self.root, text="Calories Burned:", font=self.label_font, bg='#f0f0f0').pack()
        self.activity_calories_entry = Entry(self.root)
        self.activity_calories_entry.pack()

        Label(self.root, text="Date (YYYY-MM-DD):", font=self.label_font, bg='#f0f0f0').pack()
        self.activity_date_entry = Entry(self.root)
        self.activity_date_entry.pack()

        Button(self.root, text="Add Activity", font=self.button_font, command=self.add_activity).pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.main_menu).pack()

    def show_meals(self):
        self.clear_widgets()

        Label(self.root, text="Your Meals", font=self.header_font, bg='#f0f0f0').pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.main_menu).pack()

        response = self.send_request({
            "action": "get_user_meals",
            "username": self.current_user
        })

        if "meals" in response:
            for meal in response["meals"]:
                Label(self.root, text=f"{meal[0]}: {meal[1]}g, {meal[2]} kcal", font=self.label_font, bg='#f0f0f0').pack()
        else:
            Label(self.root, text="No meals found", font=self.label_font, bg='#f0f0f0').pack()

    def show_activities(self):
        self.clear_widgets()

        Label(self.root, text="Your Activities", font=self.header_font, bg='#f0f0f0').pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.main_menu).pack()

        response = self.send_request({
            "action": "get_user_activities",
            "username": self.current_user
        })

        if "activities" in response:
            for activity in response["activities"]:
                Label(self.root, text=f"{activity[1]}: {activity[0]} kcal burned", font=self.label_font, bg='#f0f0f0').pack()
        else:
            Label(self.root, text="No activities found", font=self.label_font, bg='#f0f0f0').pack()

    def show_history(self):
        self.clear_widgets()

        Label(self.root, text="Your History", font=self.header_font, bg='#f0f0f0').pack(pady=10)
        Button(self.root, text="Back", font=self.button_font, command=self.main_menu).pack()

        response = self.send_request({
            "action": "get_user_history",
            "username": self.current_user
        })

        if "history" in response:
            for item in response["history"]:
                Label(self.root, text=f"{item[1]}: {item[0]}", font=self.label_font, bg='#f0f0f0').pack()
        else:
            Label(self.root, text="No history found", font=self.label_font, bg='#f0f0f0').pack()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_request(self, data):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP, PORT))
            client.send(jsonpickle.encode(data).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            client.close()

            if response:
                return jsonpickle.decode(response)
            return {"error": "Empty response from server"}
        except ConnectionRefusedError:
            messagebox.showerror("Error", "No connection")
            return {"error": "Connection refused"}
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            return {"error": str(e)}

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return

        response = self.send_request({
            "action": "login",
            "username": username,
            "password": password
        })

        if response.get("message") == "Login successful":
            self.current_user = username
            self.main_menu()
        else:
            messagebox.showerror("Error", "Error")

    def register(self):
        data = {
            "action": "register",
            "username": self.register_entries["reg_username"].get(),
            "email": self.register_entries["reg_email"].get(),
            "password": self.register_entries["reg_password"].get(),
            "gender": self.register_entries["reg_gender"].get().upper(),
            "age": int(self.register_entries["reg_age"].get()),
            "weight": float(self.register_entries["reg_weight"].get()),
            "height": float(self.register_entries["reg_height"].get()),
            "goal": self.register_entries["reg_goal"].get()
        }

        if self.register_entries["reg_password"].get() != self.register_entries["reg_confirm_password"].get():
            messagebox.showerror("Error", "Passwords do not match")
            return

        if data["gender"] not in ["M", "F"]:
            messagebox.showerror("Error", "Gender must be 'M' or 'F'")
            return

        try:
            data["age"] = int(data["age"])
            data["weight"] = float(data["weight"])
            data["height"] = float(data["height"])
        except ValueError:
            messagebox.showerror("Error", "Age, weight and height must be numbers")
            return

        response = self.send_request(data)

        if response.get("message") == "Registration successful":
            messagebox.showinfo("Success", "Registration successful")
            self.start_screen()
        else:
            messagebox.showerror("Error", response.get("message", "Registration failed"))

    def add_meal(self):
        product_name = self.meal_name_entry.get()
        weight = self.meal_weight_entry.get()
        caloric_value = self.meal_calories_entry.get()

        if not product_name or not weight or not caloric_value:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            weight = float(weight)
            caloric_value = float(caloric_value)
        except ValueError:
            messagebox.showerror("Error", "Weight and caloric value must be numbers")
            return

        response = self.send_request({
            "action": "add_meal",
            "username": self.current_user,
            "product_name": product_name,
            "weight": weight,
            "caloric_value": caloric_value
        })

        if response and isinstance(response, dict):
            if response.get("message") == "Meal added successfully":
                messagebox.showinfo("Success", "Meal added successfully")
                self.main_menu()
            else:
                messagebox.showerror("Error", response.get("error", "Failed to add meal"))
        else:
            messagebox.showerror("Error", "Error")

    def add_activity(self):
        calories_burned = self.activity_calories_entry.get()
        activity_date = self.activity_date_entry.get()

        if not calories_burned or not activity_date:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            calories_burned = float(calories_burned)
        except ValueError:
            messagebox.showerror("Error", "Calories burned must be a number")
            return

        response = self.send_request({
            "action": "add_activity",
            "username": self.current_user,
            "calories_burned": calories_burned,
            "activity_date": activity_date
        })

        if response.get("message") == "Activity added successfully":
            messagebox.showinfo("Success", "Activity added successfully")
            self.main_menu()
        else:
            messagebox.showerror("Error", "Failed to add activity")