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