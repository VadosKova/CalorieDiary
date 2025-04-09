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