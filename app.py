from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from login_page import LoginPage

from database import db_manager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Podgotovka")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        # Переменная для хранения ID выбранного пользователя
        self.selected_user_id = None
        # Словарь для хранения ссылок на фреймы (чтобы менять цвет)
        self.user_frames = {}

        self.show_login_page()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        crud_frame = Frame(self.root, bg="white")
        crud_frame.pack(pady=5, padx=5, fill="x")

        add_btn = ttk.Button(crud_frame, text="Добавить", command=lambda : self.show_add_user_window())
        add_btn.pack(pady=5, padx=5, side="left")

        del_btn = ttk.Button(crud_frame, text="Удалить", command=lambda :self.delete_user())
        del_btn.pack(pady=5, padx=5, side="left")

        edit_btn = ttk.Button(crud_frame, text="Редактировать", command=lambda : self.show_edit_user_window())
        edit_btn.pack(pady=5, padx=5, side="left")

        conn = db_manager.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * from users")
        users = cursor.fetchall()

        conn.close()

        users_frame = Frame(self.root, bg="white")
        users_frame.pack(pady=5, padx=5, fill="both", expand=True)

        # Очищаем словарь
        self.user_frames.clear()

        for user in users:
            user_frame = Frame(users_frame, bg="white",
                               borderwidth=1,
                               relief="solid",
                               cursor="hand2")
            user_frame.pack(anchor="center", fill="both", pady=10, padx=10, ipady=25)

            Label(user_frame, text=user[1],
                  foreground="black", font=("Arial", 12),
                  bg="white", cursor="hand2").pack(pady=5, padx=5, side="left")
            Label(user_frame, text=user[2],
                  foreground="black", font=("Arial", 12),
                  bg="white", cursor="hand2").pack(pady=5, padx=5, side="right")
            Label(user_frame, text=user[3],
                  foreground="black", font=("Arial", 12),
                  bg="white", cursor="hand2").pack(pady=5, padx=5, side="right")

            # Сохраняем фрейм в словарь
            self.user_frames[user[0]] = user_frame

            # При клике выделяем карточку
            click_action = lambda event, u_id=user[0]: self.select_card(u_id)
            user_frame.bind("<Button-1>", click_action)

            # Чтобы и лейблы реагировали на клик
            for child in user_frame.winfo_children():
                child.bind("<Button-1>", click_action)

    def select_card(self, u_id):
        # Сбрасываем выделение у всех
        for user_id, frame in self.user_frames.items():
            frame.config(bg="white", relief="solid")
            # Меняем фон у всех дочерних элементов
            for child in frame.winfo_children():
                child.config(bg="white")

        # Выделяем выбранную карточку
        if u_id in self.user_frames:
            frame = self.user_frames[u_id]
            frame.config(bg="lightblue")
            for child in frame.winfo_children():
                child.config(bg="lightblue")

            self.selected_user_id = u_id

    def delete_user(self):
        is_del = messagebox.askyesno("Удаление", "Удалить пользователя?")
        if is_del:
            u_id = self.selected_user_id

            conn = db_manager.connect()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM users WHERE id = %s", (u_id,))
            conn.commit()
            conn.close()

            self.create_widgets()
        else:
            return

    def show_add_user_window(self):
        self.AddWindow = Toplevel(self.root)
        self.AddWindow.geometry("500x400")
        self.AddWindow.resizable(False, False)
        self.AddWindow.title("Добавление пользователя")
        self.AddWindow.grab_set()

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) from users")

        new_id = cursor.fetchone()[0] + 1
        print(new_id)

        conn.close()

        Label(self.AddWindow, text="id:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.id_entry = Entry(self.AddWindow)
        self.id_entry.pack(pady=5, padx=5)
        self.id_entry.insert(0, new_id)
        self.id_entry.configure(state="disabled")

        Label(self.AddWindow, text="username:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.username_entry = Entry(self.AddWindow)
        self.username_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="phone:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.phone_entry = Entry(self.AddWindow)
        self.phone_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="age:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.age_entry = Entry(self.AddWindow)
        self.age_entry.pack(pady=5, padx=5)

        self.add_user_btn = ttk.Button(self.AddWindow, text="Добавить", command=lambda :self.add_user())
        self.add_user_btn.pack(pady=5, padx=5)

    def add_user(self):
        u_id = self.id_entry.get()
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, user_name, phone, age) VALUES (%s, %s, %s, %s)",(int(u_id), str(username), int(phone), int(age),))
        conn.commit()
        conn.close()

        self.create_widgets()

    def show_edit_user_window(self):
        self.AddWindow = Toplevel(self.root)
        self.AddWindow.geometry("500x400")
        self.AddWindow.resizable(False, False)
        self.AddWindow.title(f"Редактирование пользователя: {self.selected_user_id}")
        self.AddWindow.grab_set()

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from users WHERE id = %s", (self.selected_user_id,))
        user = cursor.fetchone()
        conn.close()

        Label(self.AddWindow, text="id:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.id_entry = Entry(self.AddWindow)
        self.id_entry.pack(pady=5, padx=5)
        self.id_entry.insert(0, self.selected_user_id)
        self.id_entry.configure(state="disabled")

        Label(self.AddWindow, text="username:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.username_entry = Entry(self.AddWindow)
        self.username_entry.pack(pady=5, padx=5)
        self.username_entry.insert(0, user[1])

        Label(self.AddWindow, text="phone:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.phone_entry = Entry(self.AddWindow)
        self.phone_entry.pack(pady=5, padx=5)
        self.phone_entry.insert(0, user[2])

        Label(self.AddWindow, text="age:", font=("Arial", 12)).pack(pady=5, padx=5)
        self.age_entry = Entry(self.AddWindow)
        self.age_entry.pack(pady=5, padx=5)
        self.age_entry.insert(0, user[3])

        self.add_user_btn = ttk.Button(self.AddWindow, text="Изменить", command=lambda: self.edit_user())
        self.add_user_btn.pack(pady=5, padx=5)

    def edit_user(self):
        username = self.username_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET user_name = %s, phone = %s, age = %s WHERE id = %s""",(username, phone, age, self.selected_user_id))
        conn.commit()
        conn.close()

        self.create_widgets()

    def show_login_page(self):
        login_page = LoginPage(self.root, self)
        login_page.create_widgets()




