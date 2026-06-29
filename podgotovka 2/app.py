from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import db_manager

class MainApp:
    def __init__(self, root):
        from login_page import LoginPage
        self.root = root
        self.root.title("EduCore")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.selected_student_number = None
        self.student_frames = {}

        self.login_page = LoginPage(self.root, self)
        self.login_page.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        buttons_frame = Frame(self.root)
        buttons_frame.pack(fill="x", pady=5, padx=5, side="top")

        crud_frame = Frame(buttons_frame)
        crud_frame.pack(fill="x", expand=True, pady=5, padx=5, side="left")

        ttk.Button(crud_frame, text="Добавить", command=lambda : self.show_add_window()).pack(padx=5, pady=5, side="left")
        ttk.Button(crud_frame, text="Редактировать", command=lambda : self.show_edit_window()).pack(padx=5, pady=5, side="left")

        exit_frame = Frame(buttons_frame)
        exit_frame.pack(fill="x", expand=True, pady=5, padx=5, side="right")
        ttk.Button(exit_frame, text="Выйти", command=lambda : self.exit_window()).pack(padx=5, pady=5, side="right")

        conn = db_manager.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()

        students_frame = Frame(self.root)
        students_frame.pack(fill="both", expand=True, pady=10, padx=100)

        for student in students:
            student_frame = Frame(students_frame, relief="solid", bd=2, cursor="hand2")
            student_frame.pack(fill="x", expand=True, pady=10, padx=10)

            left_frame = Frame(student_frame)
            left_frame.pack(side="left", fill="both", expand=True)
            Label(left_frame, text=f"ФИО: {student[1]}").pack(pady=5, padx=5, anchor="w")
            Label(left_frame, text=f"Номер договора: {student[0]}").pack(pady=5, padx=5, anchor="w")
            Label(left_frame, text=f"Номер телефона: {student[2]}").pack(pady=5, padx=5, anchor="w")

            right_frame = Frame(student_frame)
            right_frame.pack(side="right", fill="both", expand=True)
            Label(right_frame, text=f"Баланс: {student[3]}").pack(pady=5, padx=5, anchor="e")
            Label(right_frame, text=f"Статус: {student[4]}").pack(pady=5, padx=5, anchor="e")

            self.student_frames[student[0]] = student_frame
            click_action = lambda event, s_num=student[0]: self.selected_student(s_num)

            student_frame.bind("<Button-1>", click_action)
            for lr_frame in student_frame.winfo_children():
                lr_frame.bind("<Button-1>", click_action)
                for widget in lr_frame.winfo_children():
                    widget.bind("<Button-1>", click_action)

    def selected_student(self, s_num):
        for student_id, frame in self.student_frames.items():
            frame.config(bg="white")
            for lr_frame in frame.winfo_children():
                lr_frame.config(bg="white")
                for widget in lr_frame.winfo_children():
                    widget.config(bg="white")

        selected_frame = self.student_frames[s_num]
        selected_frame.config(bg="lightblue")
        for lr_frame in selected_frame.winfo_children():
            lr_frame.config(bg="lightblue")
            for widget in lr_frame.winfo_children():
                widget.config(bg="lightblue")

        self.selected_student_number = s_num
        print(self.selected_student_number)

    def show_add_window(self):
        self.AddWindow = Toplevel()
        self.AddWindow.title("Добавление студента")
        self.AddWindow.geometry("500x500")
        self.AddWindow.resizable(False, False)

        Label(self.AddWindow, text="Номер договора").pack(pady=5, padx=5)
        self.dog_number_entry = Entry(self.AddWindow)
        self.dog_number_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="ФИО").pack(pady=5, padx=5)
        self.FIO_entry = Entry(self.AddWindow)
        self.FIO_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="Номер телефона").pack(pady=5, padx=5)
        self.phone_number_entry = Entry(self.AddWindow)
        self.phone_number_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="Баланс аккаунта").pack(pady=5, padx=5)
        self.balance_entry = Entry(self.AddWindow)
        self.balance_entry.pack(pady=5, padx=5)

        Label(self.AddWindow, text="Статус").pack(pady=5, padx=5)
        self.status_entry = Entry(self.AddWindow)
        self.status_entry.pack(pady=5, padx=5)

        add_bnt = ttk.Button(self.AddWindow, text="Добавить", command=lambda : self.add_student())
        add_bnt.pack(pady=5, padx=5)

    def add_student(self):
        dog_number = self.dog_number_entry.get()
        FIO = self.FIO_entry.get()
        phone_number = self.phone_number_entry.get()
        balance = self.balance_entry.get()
        status = self.status_entry.get()

        conn = db_manager.connect()
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO 
        students (contract_number, full_name, phone, account_balance, status)
        VALUES (%s, %s, %s, %s, %s)""", (str(dog_number), str(FIO), str(phone_number), float(balance), str(status),))
        conn.commit()
        conn.close()

        self.create_widgets()

    def show_edit_window(self):
        if not self.selected_student_number:
            messagebox.showerror("Внимание", "Выберите студента для редактирования")
            return

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE contract_number = %s", (self.selected_student_number,))
        student = cursor.fetchone()
        conn.close()

        self.EditWindow = Toplevel()
        self.EditWindow.title("Редактирование студента")
        self.EditWindow.geometry("500x500")
        self.EditWindow.resizable(False, False)

        Label(self.EditWindow, text="Номер договора").pack(pady=5, padx=5)
        self.dog_number_entry = Entry(self.EditWindow)
        self.dog_number_entry.insert(0, student[0])
        self.dog_number_entry.configure(state="disabled")
        self.dog_number_entry.pack(pady=5, padx=5)

        Label(self.EditWindow, text="ФИО").pack(pady=5, padx=5)
        self.FIO_entry = Entry(self.EditWindow)
        self.FIO_entry.insert(0, student[1])
        self.FIO_entry.pack(pady=5, padx=5)

        Label(self.EditWindow, text="Номер телефона").pack(pady=5, padx=5)
        self.phone_number_entry = Entry(self.EditWindow)
        self.phone_number_entry.insert(0, student[2])
        self.phone_number_entry.pack(pady=5, padx=5)

        Label(self.EditWindow, text="Баланс аккаунта").pack(pady=5, padx=5)
        self.balance_entry = Entry(self.EditWindow)
        self.balance_entry.insert(0, student[3])
        self.balance_entry.pack(pady=5, padx=5)

        Label(self.EditWindow, text="Статус").pack(pady=5, padx=5)
        self.status_entry = Entry(self.EditWindow)
        self.status_entry.insert(0, student[4])
        self.status_entry.pack(pady=5, padx=5)

        add_bnt = ttk.Button(self.EditWindow, text="Редактировать", command=lambda: self.edit_student())
        add_bnt.pack(pady=5, padx=5)

    def edit_student(self):
        dog_number = self.dog_number_entry.get()
        FIO = self.FIO_entry.get()
        phone_number = self.phone_number_entry.get()
        balance = self.balance_entry.get()
        status = self.status_entry.get()

        conn = db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET full_name = %s, phone = %s, account_balance = %s, status = %s WHERE contract_number = %s",
                       (FIO, phone_number, balance, status, dog_number))
        conn.commit()
        conn.close()

        self.create_widgets()

    def exit_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.login_page.create_widgets()









