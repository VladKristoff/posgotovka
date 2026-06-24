from tkinter import *
from tkinter import ttk, messagebox
from database import db_manager


class LoginPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        entry_frame = Frame(self.root)
        entry_frame.pack(anchor="center", expand=True, fill="x")

        Label(entry_frame, text="Login").pack(anchor="center")
        self.login_entry = ttk.Entry(entry_frame)
        self.login_entry.pack(pady=5, padx=5, anchor="center")

        Label(entry_frame, text="Password").pack(anchor="center")
        self.password_entry = ttk.Entry(entry_frame)
        self.password_entry.pack(pady=5, padx=5, anchor="center")

        login_bnt = ttk.Button(entry_frame, text="Login", command=lambda : self.login())
        login_bnt.pack(anchor="center", padx=5, pady=5)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror("Error", "Please enter your login and password.")
            return
        else:
            conn = db_manager.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT login, password FROM userprogramm WHERE login = %s", (login,))
            user = cursor.fetchone()
            conn.close()

            if user is None:
                messagebox.showerror("Error", "Пользователь не найден.")
                return
            elif password == user[1]:
                self.app.create_widgets()
                return
            else:
                messagebox.showerror("Error", "Неверный пароль")
                return




