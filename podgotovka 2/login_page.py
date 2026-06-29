from tkinter import *
from tkinter import ttk

class LoginPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        style = ttk.Style()

        style.configure("Label.TLabel",
                        font="Arial, 14")

        style.configure("Button.TButton",
                        font="Arial, 14")

    def create_widgets(self):
        login_frame = Frame(self.root)
        login_frame.pack(fill="x", anchor="center", expand=True)

        ttk.Label(login_frame, text="EduCore",
                  style="Label.TLabel").pack(padx=5, pady=5, anchor="center")
        ttk.Button(login_frame, text="Войти",
                   style="Button.TButton",
                   command=lambda : self.login()).pack(padx=5, pady=5, anchor="center")

    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.create_widgets()


